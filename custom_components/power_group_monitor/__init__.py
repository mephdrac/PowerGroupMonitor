"""Initialisierung der MaxxiChargeConnect-Integration in Home Assistant.

Dieses Modul registriert beim Setup den Webhook und leitet den Konfigurations-Flow
an die zuständigen Plattformen (z. B. Sensor) weiter.

Funktionen:
- async_setup: Wird einmal beim Start von Home Assistant aufgerufen.
- async_setup_entry: Initialisiert eine neue Instanz bei Hinzufügen der Integration.
- async_unload_entry: Entfernt die Instanz und deregistriert den Webhook.
- async_migrate_entry: Platzhalter für zukünftige Migrationslogik.
"""

import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):  # pylint: disable=unused-argument
    """Wird beim Start von Home Assistant einmalig aufgerufen.

    Aktuell keine Initialisierung notwendig.

    Args:
        hass: Die Home Assistant-Instanz.
        config: Die Konfigurationsdaten (z.B. aus configuration.yaml).

    Returns:
        True: Setup erfolgreich.

    """
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Initialisiert eine neue Instanz der Integration beim Hinzufügen über die UI.

    Registriert den Webhook und lädt die Sensor-Plattform.

    Args:
        hass: Die Home Assistant-Instanz.
        entry: Die Konfigurationseintragsinstanz.

    Returns:
        True: Setup erfolgreich.

    """

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


# pylint: disable=too-many-statements
async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migration eines Config-Eintrags von Version 1 auf Version 2.

    Args:
        hass (HomeAssistant): Home Assistant Instanz.
        config_entry (ConfigEntry): Zu migrierender Konfiguration^seintrag.

    Returns:
        bool: True, falls Migration durchgeführt wurde, sonst False.

    """
    version = config_entry.version
    minor_version = config_entry.minor_version

    _LOGGER.info("Prüfe Migration: Aktuelle Version: %s.%s", version, minor_version)

    # if version < 2:
    #     _LOGGER.info("Migration MaxxiChargeConnect v1 → v2 gestartet")
    #     new_data = {**config_entry.data}
    #     version = 2
    #     hass.config_entries.async_update_entry(
    #         config_entry, data=new_data, version=version
    #     )

    version = 1
    hass.config_entries.async_update_entry(config_entry, version=version)
    _LOGGER.info("Migration auf Version 1 abgeschlossen")

    return True

# async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
#     # pylint: disable=unused-argument
#     """Migrationsfunktion für künftige Änderungen an gespeicherten ConfigEntries.

#     Derzeit wird keine Migration benötigt. Es wird lediglich ein Debug-Log ausgegeben.

#     Args:
#         hass: Die Home Assistant-Instanz.
#         config_entry: Der zu migrierende Konfigurationseintrag.

#     Returns:
#         True: Migration (falls nötig) erfolgreich abgeschlossen.

#     """

#     _LOGGER.warning("Migration called for entry: %s", config_entry.entry_id)
#     return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Entlädt die Integration vollständig und deregistriert den Webhook.

    Args:
        hass: Die Home Assistant-Instanz.
        entry: Der zu entladende Konfigurationseintrag.

    Returns:
        True, wenn das Entladen erfolgreich war.

    """
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in ("sensor")
            ]
        )
    )

    # unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    # if unload_ok:
    #     hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
