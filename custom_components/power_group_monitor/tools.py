"""Dieses Modul stellt verschiedene Hilfsfunktionen bereit, die in mehreren Klassen
oder Modulen verwendet werden können.

Das Modul ist so konzipiert, dass es unabhängig und wiederverwendbar in unterschiedlichen
Teilen der Anwendung eingebunden werden kann.
"""

import logging
import re

_LOGGER = logging.getLogger(__name__)


def clean_title(title: str) -> str:
    """Bereinigt einen Titel-String für die Verwendung als Entitäts-ID.

    Der Titel wird in Kleinbuchstaben umgewandelt, Sonderzeichen durch
    Unterstriche ersetzt, aufeinanderfolgende Unterstriche reduziert und
    führende bzw. abschließende Unterstriche entfernt.

    Args:
        title (str): Der ursprüngliche Titel, z.B. ein Geräte- oder Benutzername.

    Returns:
        str: Ein bereinigter, slug-artiger String, geeignet z.B. für `entity_id`s.

    """

    # alles klein machen
    title = title.lower()
    # alle Nicht-Buchstaben und Nicht-Zahlen durch Unterstriche ersetzen
    title = re.sub(r"[^a-z0-9]+", "_", title)
    # mehrere Unterstriche durch einen ersetzen
    title = re.sub(r"_+", "_", title)
    # führende und abschließende Unterstriche entfernen

    return title.strip("_")
