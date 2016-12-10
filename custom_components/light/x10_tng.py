# custom_components/light/x10_tng.py
# NOTE part of custom_components/switch/x10_tng.py

import logging

from homeassistant.helpers.entity import ToggleEntity
from homeassistant.const import DEVICE_DEFAULT_NAME, CONF_HOST, CONF_PORT, CONF_FILENAME

from custom_components.switch.x10_tng import CONF_DEVICE, setup_platform, X10Switch  # WIP

REQUIREMENTS = ['x10_any>=0.0.6']

_LOGGER = logging.getLogger(__name__)
