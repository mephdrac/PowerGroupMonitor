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
from homeassistant.config_entries import ConfigSubentryFlow
from homeassistant.config_entries import ConfigEntry
from homeassistant.config_entries import SubentryFlowResult
from homeassistant.core import callback
from typing import Any

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
    reconfigure_supported = False  # <- Aktiviert den Reconfigure-Flow    
    config_name = None

    def __init__(self):
        self.config_name = None
        self.groups = []

    @classmethod
    @callback
    def async_get_supported_subentry_types(
        cls, config_entry: ConfigEntry
    ) -> dict[str, type[ConfigSubentryFlow]]:
        """Return subentries supported by this integration."""
        return {"location": LocationSubentryFlowHandler}
    
    async def async_step_user(self, user_input=None):
        """Erster Schritt des Setup-Flows, der die Nutzereingaben abfragt.

        Args:
            user_input (dict | None): Vom Benutzer eingegebene Konfigurationsdaten.

        Returns:
            FlowResult: Nächster Schritt oder Abschluss des Flows mit neuem Eintrag.

        """

        if user_input is not None:
            self.config_name = user_input["name"]
            return self.async_create_entry(
                title=self.config_name,
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str
            })
        )

    def is_matching(self, other: config_entries.ConfigFlow) -> bool:
        """Vergleicht, ob dieser Flow einem bestehenden Flow entspricht."""
        if not isinstance(other, PowerGroupMonitorConfigFlow):
            return False
        return self.config_name == other.config_name


class LocationSubentryFlowHandler(ConfigSubentryFlow):
    """Handle subentry flow for adding and modifying a location."""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> SubentryFlowResult:
        """User flow to add a new location."""

        if user_input is not None:
            return self.async_create_entry(
                title=user_input["location_name"],
                data=user_input,
            )

        # Beispiel-Formular mit einem Feld für den Standortnamen
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("location_name"): str,
            })
        )
