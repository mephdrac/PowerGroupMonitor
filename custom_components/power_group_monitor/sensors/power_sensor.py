"""Sensor-Entity zur Anzeige der aktuellen CCU-Leistung in Home Assistant.

Dieses Modul definiert die `CcuPower`-Klasse, die einen Sensor zur Messung der Leistung
(Pccu-Wert) einer CCU (Central Control Unit) bereitstellt. Die Daten werden per Webhook empfangen
und regelmäßig aktualisiert.

Die Klasse nutzt Home Assistants Dispatcher-System, um auf neue Sensordaten zu reagieren.
"""

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower
from homeassistant.helpers.event import async_track_state_change_event

from ..const import DEVICE_INFO, DOMAIN  # noqa: TID252


_LOGGER = logging.getLogger(__name__)


class PowerSensor(SensorEntity):
    """SensorEntity für die aktuelle CCU-Leistung (Pccu-Wert).

    Diese Entität zeigt die aktuell gemessene Leistung in Watt an,
    wenn die empfangenen Daten als gültig eingestuft werden.
    """

    _attr_translation_key = "PowerSensor"
    _attr_has_entity_name = True

    def __init__(self, entry: ConfigEntry, name, entities) -> None:
        """Initialisiert den CCU-Leistungssensor.

        Args:
            entry (ConfigEntry): Die Konfigurationseintrag-Instanz für diese Integration.

        """
        self._attr_suggested_display_precision = 2
        self._entry = entry
        self._attr_name = name
        self._group_name = name
        self._entities = entities
        self._unsub = None

        self._attr_unique_id = f"{entry.entry_id}_power_sensor"
        self._attr_icon = "mdi:flash"
        self._attr_native_value = None
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT

    async def async_added_to_hass(self):
        """Wird beim Hinzufügen zur Home Assistant-Instanz aufgerufen.

        Verbindet den Sensor mit dem Dispatcher-Signal zur Aktualisierung
        der Messwerte per Webhook.
        """
        self._unsub = async_track_state_change_event(
            self.hass, self._entities, self._async_state_changed
        )
        
        await self._async_update_value()    

    async def _async_state_changed(self, event):
        # Wird aufgerufen, wenn sich eine Entity im Set ändert        
        await self._async_update_value()

    async def _async_update_value(self):
        total_power = 0.0
        for entity_id in self._entities:
            state = self.hass.states.get(entity_id)            
            if state is None:                
                continue
            try:
                value = float(state.state)
                total_power += value
            except ValueError:
                continue
        # self._state = round(total_power, 2)
        self._attr_native_value = round(total_power, 2)
        self.async_write_ha_state()

    @property
    def device_info(self):
        """Liefert die Geräteinformationen für diese Sensor-Entity.

        Returns:
            dict: Ein Dictionary mit Informationen zur Identifikation
                  des Geräts in Home Assistant, einschließlich:
                  - identifiers: Eindeutige Identifikatoren (Domain und Entry ID)
                  - name: Anzeigename des Geräts
                  - manufacturer: Herstellername
                  - model: Modellbezeichnung

        """

        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.title,
            **DEVICE_INFO,
        }
