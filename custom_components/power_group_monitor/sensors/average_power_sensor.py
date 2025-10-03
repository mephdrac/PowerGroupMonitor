import logging
from homeassistant.components import recorder
from datetime import timedelta, datetime, UTC
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfPower
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.recorder import history
from homeassistant.util import dt as dt_util


from .power_sensor import PowerSensor
from ..const import DEVICE_INFO, DOMAIN  # noqa: TID252

_LOGGER = logging.getLogger(__name__)


class AveragePowerSensor(SensorEntity):
    """Durchschnittliche Leistung über 15 Minuten."""

    _attr_translation_key = "AveragePowerSensor"
    _attr_has_entity_name = True

    def __init__(self, entry: ConfigEntry, group_name: str, source: PowerSensor):
        self._entry = entry
        self._group_name = group_name
        self._attr_translation_placeholders = {"index": self._group_name}
        self._source = source        
        self._attr_unique_id = f"{entry.entry_id}_{self._group_name}_avg_power"
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_suggested_display_precision = 3
        self._source_entity_id = source.entity_id
        self._statistics_sensor = None

    async def async_added_to_hass(self):
        """Wird aufgerufen, wenn die Entity zu HA hinzugefügt wird."""        

        source_entity_id = self._source.entity_id
        if source_entity_id is None:
            _LOGGER.warning("Sensor entity_id is None during avg setup!")
            return

        await super().async_added_to_hass()

    async def async_update(self):
        self._attr_native_value = await self.async_calculate_average()

    async def async_calculate_average(self):
        """Berechne den Durchschnitt der letzten 15 Minuten aus der History."""
        now = dt_util.utcnow()
        start = now - timedelta(minutes=15)

        def _fetch():
            return recorder.history.state_changes_during_period(
                self.hass,
                start_time=start,
                end_time=now,
                entity_id=self._source.entity_id,
                no_attributes=True,
            )

        instance = recorder.get_instance(self.hass)
        states = await instance.async_add_executor_job(_fetch)

        values = []
        for state in states.get(self._source.entity_id, []):
            try:
                values.append(float(state.state))
            except (ValueError, TypeError):
                continue

        if values:
            return sum(values) / len(values)
        return None

    @property
    def device_info(self):
        """Liefert die Geräteinformationen für diese Sensor-Entity."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.title,
            **DEVICE_INFO,
        }
