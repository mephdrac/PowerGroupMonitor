"""Sensor-Entity zur Anzeige der max. Leistung (Spitzenlast) einer Gruppe in Home Assistant.

Dieses Modul definiert die `PowerPeakSensor`-Klasse, die einen Sensor zur Messung der Max. Leistung
einer Gruppe pro Tag bereitstellt.
"""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower
from homeassistant.helpers.event import async_track_state_change_event, async_track_time_change

from ..const import DOMAIN, DEVICE_INFO


class PowerPeakSensor(SensorEntity):
    """Sensor zur Anzeige der heutigen Spitzenlast (maximale Leistung in W)."""

    _attr_translation_key = "PowerPeakSensor"

    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.POWER
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:flash-alert"

    def __init__(self, entry: ConfigEntry, group_name: str, entities: list[str]):
        self._entry = entry
        self._group_name = group_name
        self._entities = entities
        self._unsub = None
        self._reset_job = None

        self._attr_unique_id = f"{entry.entry_id}_{group_name}_peak_power_sensor"
        self._attr_translation_placeholders = {"index": group_name}
        self._attr_native_value = 0.0

    async def async_added_to_hass(self):
        self._unsub = async_track_state_change_event(
            self.hass, self._entities, self._async_state_changed
        )

        # Täglicher Reset um 00:00 Uhr
        self._reset_job = async_track_time_change(
            self.hass, self._reset_peak, hour=0, minute=0, second=0
        )

        await self._async_update_peak()

    async def async_will_remove_from_hass(self):
        if self._unsub:
            self._unsub()
        if self._reset_job:
            self._reset_job()

    # pylint: disable=unused-argument
    async def _async_state_changed(self, event):
        await self._async_update_peak()

    async def _async_update_peak(self):
        total_power = 0.0
        for entity_id in self._entities:
            state = self.hass.states.get(entity_id)
            if state is None or state.state in ("unknown", "unavailable"):
                continue

            try:
                value = float(state.state)
                unit = state.attributes.get("unit_of_measurement")
                if unit == UnitOfPower.KILO_WATT:
                    value *= 1000
                elif unit != UnitOfPower.WATT:
                    continue
                total_power += value
            except ValueError:
                continue

        # Nur aktualisieren, wenn neue Spitzenleistung erreicht
        if total_power > (self._attr_native_value or 0.0):
            self._attr_native_value = round(total_power, 2)
            self.async_write_ha_state()

    # pylint: disable=unused-argument
    async def _reset_peak(self, now=None):
        """Setzt den Spitzenwert um Mitternacht zurück."""
        self._attr_native_value = 0.0
        self.async_write_ha_state()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.title,
            **DEVICE_INFO,
        }
