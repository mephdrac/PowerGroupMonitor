"""Sensor für Gesamtenergie pro Gruppe.

Dieses Modul definiert einen Sensor für Home Assistant,
der die gesamte Energie gruppenübergreifent berechnet.
Dazu werden einfach die Gruppensensoren addiert.
"""
import logging

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfEnergy
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.event import async_track_state_change_event

from ..const import DEVICE_INFO, DOMAIN

_LOGGER = logging.getLogger(__name__)


class EnergyTotalAllSensor(SensorEntity):
    """Addiert alle Gruppen-Gesamtsummen"""
    _attr_translation_key = "EnergyTotalAllSensor"
    _attr_has_entity_name = True

    def __init__(self, entry: ConfigEntry, obj_entities) -> None:
        """Initialisiert den Sensor.

        Args:
            entry (ConfigEntry): Die Konfigurationseintrag-Instanz für diese Integration.

        """
        self._attr_suggested_display_precision = 3
        self._entry = entry
        self._obj_entities = obj_entities
        self._entities = [entity.entity_id for entity in self._obj_entities]
        self._unsub = None

        self._attr_unique_id = f"{entry.entry_id}_energy_total_all_sensor"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

        self.my_icon = "mdi:counter"
        self._attr_native_value = None

    async def async_added_to_hass(self):
        """Wird beim Hinzufügen zur Home Assistant-Instanz aufgerufen."""

        for entity in self._obj_entities:

            if entity.entity_id is None:
                _LOGGER.warning("Sensor entity_id is None during standby setup!")
                return

        self._entities = [entity.entity_id for entity in self._obj_entities]
        self._unsub = async_track_state_change_event(self.hass, self._entities, 
                                                     self._async_state_changed)

        await self._async_update_value()

    # pylint: disable=unused-argument
    async def _async_state_changed(self, event):        
        # Wird aufgerufen, wenn sich eine Entity im Set ändert
        await self._async_update_value()

    async def _async_update_value(self):
        total = 0.0
        for entity_id in self._entities:
            state = self.hass.states.get(entity_id)
            if state is None:
                continue
            try:
                value = float(state.state)

                total += value
            except ValueError:
                continue        
        self._attr_native_value = round(total, 3)
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

