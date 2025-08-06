import logging
from datetime import timedelta
from homeassistant.components.statistics.sensor import StatisticsSensor
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfPower
from homeassistant.config_entries import ConfigEntry
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
        
        self._source_entity_id = source.entity_id
        self._statistics_sensor = None

    async def async_added_to_hass(self):
        """Wird aufgerufen, wenn die Entity zu HA hinzugefügt wird."""        

        source_entity_id = self._source.entity_id
        if source_entity_id is None:
            _LOGGER.warning("Sensor entity_id is None during avg setup!")
            return

        # Statistik-Sensor anlegen
        self._statistics_sensor = StatisticsSensor(
            hass=self.hass,
            name=f"{self.name} - avg",
            unique_id=f"{self._entry.entry_id}_{self._group_name}_avg_power_statistic",
            state_characteristic="mean",
            source_entity_id=source_entity_id,
            samples_max_buffer_size=None,
            samples_max_age=timedelta(minutes=15),
            samples_keep_last=True,
            precision=2,
            percentile=0
        )

        # Beide Entities registrieren – AveragePowerSensor ist bereits registriert
        if self.platform:  # platform ist nur in async_added_to_hass gesetzt
            self.platform.async_add_entities([self._statistics_sensor])

        await super().async_added_to_hass()

    async def async_update(self):
        """Wird periodisch aufgerufen, um den Durchschnittswert zu aktualisieren."""
        value = None

        # 1️⃣ Statistik-Sensor State lesen
        if self._statistics_sensor and self._statistics_sensor.entity_id:
            stats_state = self.hass.states.get(self._statistics_sensor.entity_id)
            if stats_state and stats_state.state not in (None, "unknown", "unavailable"):
                try:
                    value = float(stats_state.state)
                except ValueError:
                    _LOGGER.debug(
                        "Konnte Statistikwert nicht in float umwandeln: %s",
                        stats_state.state
                    )

        # # 2️⃣ Falls kein Statistikwert → Fallback: PowerSensor
        # if value is None:
        #     source_state = self.hass.states.get(self._source.entity_id)
        #     if source_state and source_state.state not in (None, "unknown", "unavailable"):
        #         try:
        #             value = float(source_state.state)
        #         except ValueError:
        #             _LOGGER.debug(
        #                 "Konnte PowerSensor-Wert nicht in float umwandeln: %s",
        #                 source_state.state
        #             )

        self._attr_native_value = value

    @property
    def device_info(self):
        """Liefert die Geräteinformationen für diese Sensor-Entity."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.title,
            **DEVICE_INFO,
        }
