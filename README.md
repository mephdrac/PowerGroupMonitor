![PowerGroupMonitor](images/logo.png)

# PowerGroupMonitor

[![GitHub Release][releases-shield]][releases]
[![hacs][hacsbadge]][hacs]
[![License][license-shield]][license]
[![Issues][issue-shield]][issues]
[![GitHub Activity][commits-shield]][commits]
[![HacsStats][stats-shield]][ha-analytics]

[Maxxisun-CCUs]: https://maxxisun.de/
[maxxisun-ha]: https://github.com/mephdrac/PowerGroupMonitor
[commits-shield]: https://img.shields.io/github/commit-activity/y/mephdrac/PowerGroupMonitor
[commits]: https://github.com/mephdrac/PowerGroupMonitor/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg
[license-shield]: https://img.shields.io/github/license/mephdrac/PowerGroupMonitor.svg
[issue-shield]: https://img.shields.io/github/issues/mephdrac/PowerGroupMonitor.svg
[releases-shield]: https://img.shields.io/github/release/mephdrac/PowerGroupMonitor.svg
[releases]: https://github.com/mephdrac/PowerGroupMonitor/releases
[stats-shield]: https://img.shields.io/badge/dynamic/json?color=41BDF5&logo=home-assistant&label=integration%20usage&suffix=%20installs&cacheSeconds=15600&url=https://analytics.home-assistant.io/custom_integrations.json&query=$.PowerGroupMonitor.total
[ha-analytics]: https://analytics.home-assistant.io/
[issues]: https://github.com/mephdrac/PowerGroupMonitor/issues
[license]: https://github.com/mephdrac/PowerGroupMonitor/blob/main/LICENSE



**PowerGroupMonitor** ist eine Home Assistant Integration zur intelligenten Überwachung und Auswertung von Energie- und Leistungsdaten über mehrere Geräte hinweg. Mit PowerGroupMonitor kannst du Geräte in logische Gruppen zusammenfassen und deren Gesamtverbrauch sowie wichtige Kennzahlen (KPIs) komfortabel überwachen.

---

## ✅ Funktionen

- Gerätegruppen anlegen: Definiere Gruppen (z. B. Küche, Büro, Wärmeerzeuger), die beliebige Energie- oder Leistungs-Sensoren enthalten.
- Aggregierte Verbrauchswerte: Erhalte Echtzeit-Daten zu Gesamtleistung (Watt) pro Gruppe
- Kompatibilität: Funktioniert herstellerunabhängig, z. B. mit Shelly, Tasmota, Zigbee, Tuya und anderen Geräten.
- Spitzenlast heute pro Gruppe.
- Standby-Sensor
- Aggregierte Verbrauchswerte: Erhalte den Energieverbrauch (kWh) pro Gruppe.
- Integration ins Energy Dashboard: Die gruppierten Sensoren lassen sich direkt im Home Assistant Energy Dashboard verwenden.

## ⚠️  Funktionen (geplant - noch nicht implementiert)
- Tägliche und monatliche Statistik: Überblick über Verbrauchshistorie direkt in Home Assistant.
- KPIs & Analysen: Standby-Anteile, Spitzenlasten, Betriebsdauer und weitere nützliche Kennzahlen.

---
## Beschreibung: Standby - Sensor

Ein Sensor, der:

- den aktuellen Gesamtverbrauch der Gruppe beobachtet (PowerSensor),
- prüft, ob er unter einem konfigurierten Schwellenwert liegt,
- on bedeutet: alles im Standby,
- off bedeutet: mindestens ein Gerät verbraucht mehr als nur Standby.
---

## ⚠️ Limitationen:
 
---

## Warum PowerGroupMonitor?
Viele Home Assistant Nutzer haben zahlreiche smarte Geräte verschiedener Marken im Einsatz. PowerGroupMonitor vereinfacht die Überwachung, indem es Geräte nach deinen Bedürfnissen gruppiert und aggregierte Verbrauchswerte sowie aussagekräftige Statistiken liefert – ohne großen Aufwand.

---

## Installation
PowerGroupMonitor ist als Custom Integration verfügbar und kann einfach über HACS installiert werden. Alternativ kannst du die Integration manuell unter custom_components/power_group_monitor installieren.

---

# Konfiguration
Die Konfiguration erfolgt bequem über die Home Assistant Benutzeroberfläche (Config Flow) oder per YAML. Du legst Gruppen mit frei wählbaren Namen an und weist ihnen Sensoren zu, die überwacht werden sollen.

---

## 🚫 Haftungsausschluss
Diese Software wird ohne jegliche Gewährleistung bereitgestellt.
Die Nutzung erfolgt auf eigene Gefahr. Ich übernehme keine Haftung für:

Schäden an Hardware oder Software

Datenverluste

fehlerhafte oder veraltete Messwerte

Kompatibilitätsprobleme mit zukünftigen Home Assistant-Versionen

---


## 🙌 Mitwirken
Pull Requests, Fehlerberichte und Vorschläge sind willkommen!
Bitte eröffne ein Issue, wenn du etwas beitragen oder melden möchtest.

---

## 📄 Lizenz
Veröffentlicht unter der MIT-Lizenz.
