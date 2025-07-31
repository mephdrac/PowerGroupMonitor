import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower
from homeassistant.helpers.event import async_track_state_change_event

from ..const import DOMAIN, DEVICE_INFO

_LOGGER = logging.getLogger(__name__)


class PowerStandbySensor(BinarySensorEntity):
    """Binärsensor zur Erkennung von Standby-Zuständen in einer Gruppe."""

    _attr_translation_key = "PowerStandbySensor"
    _attr_has_entity_name = True
    _attr_device_class = BinarySensorDeviceClass.POWER
    _attr_icon = "mdi:power-sleep"

    def __init__(self, entry, group_name, power_sensor, standby_threshold):
        self._entry = entry
        self._group_name = group_name
        self._power_sensor = power_sensor
        self._threshold = standby_threshold
        self._power_entity_id = None
        self._unsub = None

        self._attr_unique_id = f"{entry.entry_id}_{group_name}_standby_sensor"
        self._attr_translation_placeholders = {"index": group_name}
        self._attr_is_on = None

    async def async_added_to_hass(self):
        power_entity_id = self._power_sensor.entity_id
        if power_entity_id is None:
            _LOGGER.warning("Power sensor entity_id is None during standby setup!")
            return
        
        self._power_entity_id = power_entity_id 
        self._unsub = async_track_state_change_event(
            self.hass, [power_entity_id], self._async_power_changed
        )
        await self._async_update()

    async def async_will_remove_from_hass(self):
        if self._unsub:
            self._unsub()

    async def _async_power_changed(self, event):
        await self._async_update()

    async def _async_update(self):
        state = self.hass.states.get(self._power_entity_id)
        if state is None or state.state in ("unavailable", "unknown"):
            return

        try:
            value = float(state.state)
        except ValueError:
            return

        self._attr_is_on = value < self._threshold
        self.async_write_ha_state()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.title,
            **DEVICE_INFO,
        }
