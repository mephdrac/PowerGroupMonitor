"""Sensor für Gesamtenergie pro Gruppe.

Dieses Modul definiert eine benutzerdefinierte IntegrationSensor-Entität für Home Assistant,
die die gesamte Energie pro Gruppe berechnet, die über einen Zeitraum verbraucht oder erzeugt wurde.
Die Integration erfolgt über eine trapezförmige Methode mit automatischer Einheitenskalierung.
"""
from .total_integral_sensor import TotalIntegralSensor


class EnergyTotalSensor(TotalIntegralSensor):
    """Sensor zur Integration der Energie (kWh gesamt) über die Gruppe."""

    _attr_entity_registry_enabled_default = True
