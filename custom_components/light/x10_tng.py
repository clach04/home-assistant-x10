# custom_components/light/x10_tng.py
# NOTE part of custom_components/switch/x10_tng.py

import logging

from homeassistant.helpers.entity import ToggleEntity
from homeassistant.const import DEVICE_DEFAULT_NAME, CONF_HOST, CONF_PORT, CONF_FILENAME

from custom_components.switch.x10_tng import CONF_DEVICE, setup_x10, X10Switch  # WIP

REQUIREMENTS = ['x10_any>=0.0.6']

_LOGGER = logging.getLogger(__name__)


class X10Light(X10Switch):
    """Representation of an X10 lamp) module that WILL support dimming"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def setup_platform(hass, config, add_devices, discovery_info=None):
    setup_x10(hass, config, add_devices, discovery_info=discovery_info, deviceclass=X10Light)
