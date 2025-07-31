"""Dieses Modul initialisiert und registriert die Sensor-Entitäten für die
MaxxiChargeConnect-Integration in Home Assistant.

Es verwaltet die Sensoren über den BatterySensorManager pro ConfigEntry
und fügt alle relevanten Sensoren
beim Setup hinzu. Sensoren umfassen unter anderem Geräte-ID, Batteriestatus,
PV-Leistung, Netzbezug/-einspeisung
und zugehörige Energie-Statistiken.

Module-Level Variable:
    SENSOR_MANAGER (dict): Verwaltung der BatterySensorManager Instanzen, keyed nach entry_id.

"""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .sensors.power_sensor import PowerSensor
from .sensors.power_peak_sensor import PowerPeakSensor

from .const import CONF_GROUP_NAME, CONF_GROUP_ENTITIES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(  # pylint: disable=too-many-locals, too-many-statements, unused-argument
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Setzt die Sensoren für einen ConfigEntry asynchron auf.

    Args:
        hass (HomeAssistant): Die Home Assistant Instanz.
        entry (ConfigEntry): Die Konfigurationseintrag, für den die Sensoren erstellt werden.
        async_add_entities (AddEntitiesCallback): Callback-Funktion zum Hinzufügen von
          Entities in HA.

    Returns:
        None

    """

    data = entry.data
    groups = data.get("groups", [])

    power_sensors = []
    power_peak_sensors = []

    for group in groups:
        group_name = group[CONF_GROUP_NAME]
        entities = group[CONF_GROUP_ENTITIES]
        power_sensors.append(PowerSensor(entry, group_name, entities))
        power_peak_sensors.append(PowerPeakSensor(entry, group_name, entities))

    async_add_entities(power_sensors, update_before_add=True)
    async_add_entities(power_peak_sensors, update_before_add=True)
