"""Konstanten für die PowerGroupMonitor Integration.

Attributes:
    DOMAIN (str): Der Domain-Name der Integration, wird als eindeutiger Namespace
        in Home Assistant verwendet.
"""

DOMAIN = "power_group_monitor"

CONF_GROUPS = "groups"
CONF_GROUP_ENTITIES = "entities"
CONF_GROUP_NAME = "group_name"
CONF_NEXT_STEP = "next_step"


DEVICE_INFO = {
    "manufacturer": "mephdrac",
    "model": "Power - Monitor",
}
