"""Oberklassen-Sensor für die Gesamtenergiezählung pro Gruppe.

Dieses Modul definiert eine benutzerdefinierte IntegrationSensor-Entität für Home Assistant,
die die gesamte Energie über die Zeit aufsummiert.

Die Energiemenge wird mittels der Trapezregel integriert und in Kilowattstunden dargestellt.

Classes:
    TotalIntegralSensor: Oberklassen-Sensorentität zur Anzeige der aufsummierten Energie
"""

from datetime import UTC, datetime, timedelta

import logging

from homeassistant.components.integration.sensor import (
    UNIT_PREFIXES,
    UNIT_TIME,
    IntegrationSensor,
    UnitOfTime,
    _IntegrationMethod,
    _IntegrationTrigger,
)
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from .power_sensor import PowerSensor

from ..const import DEVICE_INFO, DOMAIN  # noqa: TID252
from ..tools import clean_title

_LOGGER = logging.getLogger(__name__)


# pylint: disable=too-many-instance-attributes
class TotalIntegralSensor(IntegrationSensor):
    """Sensorentität zur Anzeige der gesamten Energie (kWh).

    Diese Entität summiert Energie über die Zeit auf, um
    die Insgesamtenergie zu berechnen. Sie nutzt dafür die Trapezregel
    zur Integration und stellt den Wert in Kilowattstunden dar.

    Attributes:
        _attr_entity_registry_enabled_default (bool): Gibt an, ob die Entität standardmäßig
           aktiviert ist.
        _entry (ConfigEntry): Die Konfigurationsdaten dieser Entität.
        _attr_icon (str): Das Symbol, das in der Benutzeroberfläche angezeigt wird.
        _attr_device_class (str): Gibt den Typ des Sensors an (hier: ENERGY).
        _attr_state_class (str): Gibt die Art des Sensorzustands an (TOTAL_INCREASING).
        _attr_native_unit_of_measurement (str): Die verwendete Energieeinheit (kWh).

    """

    _attr_has_entity_name = True

    # pylint: disable=super-init-not-called
    def __init__(self, hass: HomeAssistant, entry, group_id, group_name: str, source: PowerSensor) -> None:
        """Initialisiert die Sensorentität für die gesamte Energie.

        Args:
            hass (HomeAssistant): Die Home Assistant-Instanz.
            entry (ConfigEntry): Der Konfigurationseintrag mit den Einstellungen dieser Entität.
            source_entity_id (str): Die Quell-Entity-ID, die den Wert in Watt liefert.

        """
        self.hass = hass
        self._group_id = group_id
        self._group_name = group_name
        self._attr_translation_key = self.__class__.__name__
        self._attr_translation_placeholders = {"index": self._group_name}
        self._attr_unique_id = (
            f"{entry.entry_id}_{self._group_id}_{clean_title(self.__class__.__name__)}"
        )
        self._source = source
        self._source_entity = source.entity_id
        self._sensor_source_id = source.entity_id
        self._round_digits = 3
        self._state = None
        self._integration_method = self._method = _IntegrationMethod.from_name(
            "trapezoidal"
        )

        # self._attr_name = name if name is not None else f"{source_entity} integral"
        self._unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        self.unit_prefix = "k"
        self._unit_prefix_string = "" if self.unit_prefix is None else self.unit_prefix
        self._unit_of_measurement: str | None = None
        self._unit_prefix = UNIT_PREFIXES[self.unit_prefix]
        self.unit_time = UnitOfTime.HOURS
        self._unit_time = UNIT_TIME[self.unit_time]
        self._unit_time_str = self.unit_time
        self._last_valid_state = None
        # self._attr_device_info = device_info
        self._max_sub_interval = timedelta(seconds=120)
        self._last_integration_time = datetime.now(tz=UTC)
        self._last_integration_trigger = _IntegrationTrigger.StateEvent
        self._attr_suggested_display_precision = self._round_digits or 2
        # Zuweisung
        self._max_sub_interval_exceeded_callback = (
            self._handle_max_sub_interval_exceeded
        )

        # Setzte neue Attribute
        self._entry = entry
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self.my_icon = "mdi:counter"
        self._attr_icon = self.my_icon

        # Setze initialen Reset-Zeitpunkt auf heutige Mitternacht lokal
        self._unsub_time_reset = None
        local_midnight = dt_util.start_of_local_day()
        self._last_reset = dt_util.as_utc(local_midnight)

    def _handle_max_sub_interval_exceeded(self):
        _LOGGER.debug(
            "[%s] Kein neuer Wert innerhalb von %s empfangen – Integration pausiert",
            self.entity_id,
            self._max_sub_interval,
        )

    async def async_added_to_hass(self):
        """Wird aufgerufen, wenn die Entität zu Home Assistant hinzugefügt wird.

        Registriert einen täglichen Reset der Energiewerte um 0:00 Uhr lokale Zeit.
        """
        source_entity_id = self._source.entity_id

        if source_entity_id is None:
            _LOGGER.warning("Power sensor entity_id is None during standby setup!")
            return

        self._source_entity = self._source.entity_id
        self._sensor_source_id = self._source.entity_id

        _LOGGER.debug("Source.entity_id: %s", self._source.entity_id)

        await super().async_added_to_hass()

        if self._unsub_time_reset is not None:
            self.async_on_remove(self._unsub_time_reset)

    @property
    def icon(self):
        """Liefert das Icon der Entity"""
        return self.my_icon

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
