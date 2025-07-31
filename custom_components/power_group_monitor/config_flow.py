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
from homeassistant.const import CONF_NAME, CONF_ENTITIES
from homeassistant.helpers.selector import selector

# from homeassistant.helpers.selector import selector

from .const import DOMAIN

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

    async def async_step_user(self, user_input=None):
        """Erster Schritt des Setup-Flows, der die Nutzereingaben abfragt.

        Args:
            user_input (dict | None): Vom Benutzer eingegebene Konfigurationsdaten.

        Returns:
            FlowResult: Nächster Schritt oder Abschluss des Flows mit neuem Eintrag.

        """
        if user_input is not None:
            self._name = user_input[CONF_NAME]
            self._entities = user_input[CONF_ENTITIES]

            return self.async_create_entry(
                title=self._name,
                data={
                    CONF_NAME: self._name,
                    CONF_ENTITIES: self._entities
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_ENTITIES): selector({
                    "entity": {
                        "multiple": True,
                        "filter": [
                            {"domain": "switch"},
                            {"domain": "sensor"},
                            {"domain": "light"}
                        ],
                        "device_class": "power"  # optional: filter auf power-sensoren
                    }
                })
            }),
            last_step=True
        )

    def is_matching(self, other: config_entries.ConfigFlow) -> bool:
        """Vergleicht, ob dieser Flow einem bestehenden Flow entspricht."""
        if not isinstance(other, PowerGroupMonitorConfigFlow):
            return False
        return self._name == other._name