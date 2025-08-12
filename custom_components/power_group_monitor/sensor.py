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
from .sensors.power_standby_sensor import PowerStandbySensor
from .sensors.power_total_sensor import PowerTotalSensor
from .sensors.power_peak_total_sensor import PowerPeakTotalSensor
from .sensors.power_standby_total_sensor import PowerStandbyTotalSensor
from .sensors.energy_today_sensor import EnergyTodaySensor
from .sensors.energy_total_sensor import EnergyTotalSensor

from .sensors.energy_total_all_sensor import EnergyTotalAllSensor
from .sensors.energy_today_all_sensor import EnergyTodayAllSensor

from .const import CONF_GROUP_NAME, CONF_GROUP_ENTITIES, CONF_GROUP_STANDBY, \
                    CONF_GROUP_ID

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

    entity_list = []
    energy_total_list = []
    energy_today_list = []
    total_standby_threshold = float(0)

    for group in groups:
        group_id = group[CONF_GROUP_ID]
        group_name = group[CONF_GROUP_NAME]
        standby_threshold = group[CONF_GROUP_STANDBY]
        total_standby_threshold += float(standby_threshold)
        entities = group[CONF_GROUP_ENTITIES]

        power_sensor = PowerSensor(entry, group_id, group_name, entities)
        power_peak_sensor = PowerPeakSensor(entry, group_id, group_name, entities)

        standby_sensor = PowerStandbySensor(
            entry,
            group_id,
            group_name,
            power_sensor,  # ← auf den dynamischen ID-Zugriff achten
            standby_threshold=float(standby_threshold),  # konfigurierbarer Wert?
        )

        # Energie pro Gruppe heute
        energie_heute_gruppe = EnergyTodaySensor(hass, entry, group_id, group_name, power_sensor)
        # Energie pro Gruppe gesamt
        energie_gesamt_gruppe = EnergyTotalSensor(hass, entry, group_id,  group_name, power_sensor)

        entity_list.extend([power_sensor, power_peak_sensor, standby_sensor,
                            energie_heute_gruppe, energie_gesamt_gruppe])

        energy_total_list.extend([energie_gesamt_gruppe])
        energy_today_list.extend([energie_heute_gruppe])

    async_add_entities(entity_list, update_before_add=True)

    # Add - Gesamt über alle Gruppen
    power_total_sensor = PowerTotalSensor(entry)
    power_peak_total_sensor = PowerPeakTotalSensor(entry)

    # pylint: disable=line-too-long
    power_standby_total_sensor = PowerStandbyTotalSensor(entry, power_total_sensor, total_standby_threshold)

    all_energy_total = EnergyTotalAllSensor(entry, energy_total_list)
    all_energy_today = EnergyTodayAllSensor(entry, energy_today_list)

    async_add_entities(
        [
            power_total_sensor,
            power_peak_total_sensor,
            power_standby_total_sensor,
            all_energy_total,
            all_energy_today
        ]
    )
