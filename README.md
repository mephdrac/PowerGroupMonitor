![PowerGroupMonitor](images/logo.png)

# PowerGroupMonitor


**PowerGroupMonitor** ist eine Home Assistant Integration zur intelligenten Überwachung und Auswertung von Energie- und Leistungsdaten über mehrere Geräte hinweg. Mit PowerGroupMonitor kannst du Geräte in logische Gruppen zusammenfassen und deren Gesamtverbrauch sowie wichtige Kennzahlen (KPIs) komfortabel überwachen.

---

## ✅ Funktionen (geplant - noch nicht implementiert)

- Gerätegruppen anlegen: Definiere Gruppen (z. B. Küche, Büro, Wärmeerzeuger), die beliebige Energie- oder Leistungs-Sensoren enthalten.
- Aggregierte Verbrauchswerte: Erhalte Echtzeit-Daten zu Gesamtleistung (Watt) und Energieverbrauch (kWh) pro Gruppe.
- Tägliche und monatliche Statistik: Überblick über Verbrauchshistorie direkt in Home Assistant.
- KPIs & Analysen: Standby-Anteile, Spitzenlasten, Betriebsdauer und weitere nützliche Kennzahlen.
- Kompatibilität: Funktioniert herstellerunabhängig, z. B. mit Shelly, Tasmota, Zigbee, Tuya und anderen Geräten.
- Integration ins Energy Dashboard: Die gruppierten Sensoren lassen sich direkt im Home Assistant Energy Dashboard verwenden.

---

## ⚠️ Limitationen:
 **PowerGroupMonitor** ist noch nicht einsatzfähig. Diese Version ist nur die Intial-Version. Sie hat noch keinerlei Funktionalität.
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
