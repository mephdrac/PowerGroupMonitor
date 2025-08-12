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

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.helpers.selector import selector

from .const import (
    CONF_GROUPS,
    CONF_GROUP_ENTITIES,
    CONF_GROUP_NAME,
    CONF_GROUP_STANDBY,
    CONF_NEXT_STEP,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class PowerGroupMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Konfigurations-Flow für die PowerGroupMonitor Integration."""

    VERSION = 1
    MINOR_VERSION = 2
    reconfigure_supported = True  # Aktiviert den Reconfigure-Flow

    def __init__(self):
        self._name = None
        self._groups = []
        self._reconfigure = False
        self._edit_group_original_name = None  # Merkt die zu bearbeitende Gruppe

    # ---------- Setup-Flow ----------
    async def async_step_user(self, user_input=None):
        """Erster Schritt des Setup-Flows."""
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
        """Gruppe hinzufügen (wird für Setup und Reconfigure genutzt)."""
        if user_input is not None:
            self._groups.append({
                CONF_GROUP_NAME: user_input[CONF_GROUP_NAME],
                CONF_GROUP_STANDBY: user_input[CONF_GROUP_STANDBY],
                CONF_GROUP_ENTITIES: user_input[CONF_GROUP_ENTITIES],
            })
            if self._reconfigure:
                return await self.async_step_reconfigure_menu()
            else:
                return await self.async_step_group_menu()

        return self.async_show_form(
            step_id="add_group",
            data_schema=vol.Schema({
                vol.Required(CONF_GROUP_NAME): str,
                vol.Required(CONF_GROUP_STANDBY): str,
                vol.Required(CONF_GROUP_ENTITIES): selector({
                    "entity": {
                        "multiple": True,
                        "filter": [
                            {"domain": "sensor"},
                            {"domain": "switch"},
                            {"domain": "light"}
                        ],
                        "device_class": ["power", "energy"]
                    }
                }),
            }),
        )

    async def async_step_group_menu(self, user_input=None):
        """Fragemenü im Setup-Flow."""
        options = {
            "add_another": "Weitere Gruppe hinzufügen",
            "finish": "Fertig"
        }

        if user_input is not None:
            if user_input[CONF_NEXT_STEP] == "add_another":
                return await self.async_step_add_group()
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
                vol.Required(CONF_NEXT_STEP, default="add_another"): vol.In(options)
            })
        )

    # ---------- Reconfigure-Flow ----------
    async def async_step_reconfigure(self, user_input=None):
        """Startet den Reconfigure-Flow."""
        entry = self._get_reconfigure_entry()
        self._name = entry.data.get(CONF_NAME)
        self._groups = entry.data.get(CONF_GROUPS, []).copy()
        self._reconfigure = True
        return await self.async_step_reconfigure_menu()

    async def async_step_reconfigure_menu(self, user_input=None):
        """Menü für den Reconfigure-Flow."""
        options = {
            "add": "Neue Gruppe hinzufügen",
            "edit": "Bestehende Gruppe bearbeiten",
            "delete": "Gruppe löschen",
            "finish": "Fertigstellen"
        }

        if user_input is not None:
            choice = user_input[CONF_NEXT_STEP]
            if choice == "add":
                return await self.async_step_add_group()
            elif choice == "edit":
                return await self.async_step_select_group_to_edit()
            elif choice == "delete":
                return await self.async_step_select_group_to_delete()
            elif choice == "finish":
                entry = self._get_reconfigure_entry()
                return self.async_update_reload_and_abort(
                    entry,
                    data_updates={
                        CONF_NAME: self._name,
                        CONF_GROUPS: self._groups
                    }
                )

        # Neue Darstellung: Name + Entity-Anzahl
        group_list_str = "\n".join(
            [
                f"{idx+1}. {g[CONF_GROUP_NAME]} ({len(g.get(CONF_GROUP_ENTITIES, []))} Entitäten)"
                for idx, g in enumerate(self._groups)
            ]
        ) or "Keine Gruppen vorhanden"

        return self.async_show_form(
            step_id="reconfigure_menu",
            data_schema=vol.Schema({
                vol.Required(CONF_NEXT_STEP, default="add"): vol.In(options)
            }),
            description_placeholders={"groups": group_list_str}
        )


    async def async_step_select_group_to_edit(self, user_input=None):
        """Gruppe zum Bearbeiten auswählen."""
        if user_input is not None:
            self._edit_group_original_name = user_input["group_name"]  # speichern
            return await self.async_step_edit_group()

        choices = {g[CONF_GROUP_NAME]: g[CONF_GROUP_NAME] for g in self._groups}
        return self.async_show_form(
            step_id="select_group_to_edit",
            data_schema=vol.Schema({
                vol.Required("group_name"): vol.In(choices)
            })
        )

    async def async_step_select_group_to_delete(self, user_input=None):
        """Gruppe zum Löschen auswählen."""
        if user_input is not None:
            index = int(user_input["group_index"])
            del self._groups[index]
            return await self.async_step_reconfigure_menu()

        choices = {str(i): g[CONF_GROUP_NAME] for i, g in enumerate(self._groups)}
        return self.async_show_form(
            step_id="select_group_to_delete",
            data_schema=vol.Schema({
                vol.Required("group_index"): vol.In(choices)
            })
        )

    async def async_step_edit_group(self, user_input=None):
        """Gruppe bearbeiten."""
        # Suche die Gruppe mit dem gespeicherten Originalnamen
        index = next((i for i, g in enumerate(self._groups)
                      if g[CONF_GROUP_NAME] == self._edit_group_original_name), None)
        if index is None:
            _LOGGER.error("Gruppe '%s' nicht gefunden", self._edit_group_original_name)
            return await self.async_step_reconfigure_menu()

        if user_input is not None:
            self._groups[index] = {
                CONF_GROUP_NAME: user_input[CONF_GROUP_NAME],
                CONF_GROUP_STANDBY: user_input[CONF_GROUP_STANDBY],
                CONF_GROUP_ENTITIES: user_input[CONF_GROUP_ENTITIES],
            }
            self._edit_group_original_name = None  # zurücksetzen
            return await self.async_step_reconfigure_menu()

        group = self._groups[index]
        return self.async_show_form(
            step_id="edit_group",
            data_schema=vol.Schema({
                vol.Required(CONF_GROUP_NAME, default=group[CONF_GROUP_NAME]): str,
                vol.Required(CONF_GROUP_STANDBY, default=group[CONF_GROUP_STANDBY]): str,
                vol.Required(CONF_GROUP_ENTITIES, default=group.get(CONF_GROUP_ENTITIES, [])): selector({
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
            })
        )

    def is_matching(self, other: config_entries.ConfigFlow) -> bool:
        """Vergleicht, ob dieser Flow einem bestehenden Flow entspricht."""
        return isinstance(other, PowerGroupMonitorConfigFlow)
