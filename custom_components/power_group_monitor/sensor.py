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
from .const import CONF_GROUP_NAME, CONF_GROUP_ENTITIES

#from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(  # pylint: disable=too-many-locals, too-many-statements
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

    sensors = []
    for group in groups:
        group_name = group[CONF_GROUP_NAME]        
        entities = group[CONF_GROUP_ENTITIES]
        sensors.append(PowerSensor(entry, group_name, entities))

    async_add_entities(sensors, update_before_add=True)
   
    


    # power_sensor = PowerSensor(entry)

    # async_add_entities(
    #     [
    #        power_sensor,
    #     ]
    # )
#    await asyncio.sleep(0)
