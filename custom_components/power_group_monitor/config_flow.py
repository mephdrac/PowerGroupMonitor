"""Konfigurations-Flow für die PowerGroupMonitor Integration.

Dieses Modul implementiert den Konfigurations-Flow für die Home Assistant Integration
"PowerGroupMonitor". Es ermöglicht die Einrichtung und Neukonfiguration eines
ConfigEntry, inklusive:

- Abfrage von Name, Webhook-ID, IP-Adresse und IP-Whitelist-Option im Setup-Dialog.
- Unterstützung eines Reconfigure-Flows zur Änderung bestehender Einträge.
- Migration von Version 1 zu Version 2 der Konfigurationseinträge.

Der Flow validiert keine Eingaben, sondern speichert sie zur weiteren Nutzung
in der Integration.

Typischerweise wird dieser Flow vom Home Assistant Framework automatisch
aufgerufen, wenn der Nutzer die Integration hinzufügt oder neu konfiguriert.

"""
import logging
import voluptuous as vol
from typing import Any

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.helpers.selector import selector

# from homeassistant.helpers.selector import selector

from .const import CONF_GROUPS, CONF_GROUP_ENTITIES, CONF_GROUP_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)


# pylint: disable=W0237
class PowerGroupMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Konfigurations-Flow für die PowerGroupMonitor Integration.

    Unterstützt den Standard-Setup-Flow sowie einen Reconfigure-Flow,
    um bestehende Einträge zu ändern.

    Attributes:
        VERSION (int): Versionsnummer der Config-Flow-Datenstruktur.
        reconfigure_supported (bool): Ob der Reconfigure-Flow aktiviert ist.

    """

    VERSION = 1
    MINOR_VERSION = 1
    reconfigure_supported = True  # <- Aktiviert den Reconfigure-Flow

    def __init__(self):
        self._name = None
        self._entities = None
        self._groups = []

    async def async_step_user(self, user_input=None):
        """Erster Schritt des Setup-Flows, der die Nutzereingaben abfragt.

        Args:
            user_input (dict | None): Vom Benutzer eingegebene Konfigurationsdaten.

        Returns:
            FlowResult: Nächster Schritt oder Abschluss des Flows mit neuem Eintrag.

        """
        if user_input is not None:
            self._name = user_input[CONF_NAME]
            self._groups = []
            return await self.async_step_add_group()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME): str,
            })
        )

    async def async_step_add_group(self, user_input=None):
        if user_input is not None:
            group_name = user_input[CONF_GROUP_NAME]
            entities = user_input[CONF_GROUP_ENTITIES]
            self._groups.append({
                CONF_GROUP_NAME: group_name,
                CONF_GROUP_ENTITIES: entities,
            })
            return await self.async_step_group_menu()

        return self.async_show_form(
            step_id="add_group",
            data_schema=vol.Schema({
                vol.Required(CONF_GROUP_NAME): str,
                vol.Required(CONF_GROUP_ENTITIES): selector({
                    "entity": {
                        "multiple": True,
                        "filter": [
                            {"domain": "sensor"},
                            {"domain": "switch"},
                            {"domain": "light"}
                        ],
                        "device_class": "power"
                    }
                }),
            }),
        )
    
    async def async_step_group_menu(self, user_input=None):
        options = {
            "add_another": "Weitere Gruppe hinzufügen",
            "finish": "Fertig"
        }

        if user_input is not None:
            if user_input["next_step"] == "add_another":
                return await self.async_step_add_group()
            else:
                return self.async_create_entry(
                    title=self._name,
                    data={
                        CONF_NAME: self._name,
                        CONF_GROUPS: self._groups,
                    },
                )

        return self.async_show_form(
            step_id="group_menu",
            data_schema=vol.Schema({
                vol.Required("next_step", default="add_another"): vol.In(options)
            })
        )
    
    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        """Flow-Schritt für die Neukonfiguration eines bestehenden Eintrags."""
        entry = self._get_reconfigure_entry()
        current_groups = entry.data.get(CONF_GROUPS, [])

        if user_input is not None:
            # Update speichern
            new_groups = []
            for i in range(len(current_groups)):
                name = user_input.get(f"{CONF_GROUP_NAME}_{i}")
                entities = user_input.get(f"group_{CONF_GROUP_ENTITIES}_{i}", [])
                new_groups.append({CONF_GROUP_NAME: name, CONF_GROUP_ENTITIES: entities})

            return self.async_update_reload_and_abort(
                entry,
                data_updates={CONF_GROUPS: new_groups}
            )

        # Dynamisches Schema aus bestehender Gruppenanzahl aufbauen
        schema_fields = {}
        for i, group in enumerate(current_groups):
            schema_fields[vol.Required(f"{CONF_GROUP_NAME}_{i}", default=group[CONF_GROUP_NAME])] = str
            schema_fields[vol.Required(
                f"group_{CONF_GROUP_ENTITIES}_{i}",
                default=group.get(CONF_GROUP_ENTITIES, []),
            )] = selector({
                "entity": {
                    "multiple": True,
                    "filter": [
                        {"domain": "switch"},
                        {"domain": "sensor"},
                        {"domain": "light"}
                    ],
                    "device_class": ["power", "energy"]
                }
            })

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(schema_fields)
        )

    def is_matching(self, other: config_entries.ConfigFlow) -> bool:
        """Vergleicht, ob dieser Flow einem bestehenden Flow entspricht."""
        return isinstance(other, PowerGroupMonitorConfigFlow)
