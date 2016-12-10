# custom_components/light/x10_tng.py
# NOTE part of custom_components/switch/x10_tng.py

import logging

from homeassistant.helpers.entity import ToggleEntity
from homeassistant.const import DEVICE_DEFAULT_NAME, CONF_HOST, CONF_PORT, CONF_FILENAME
from homeassistant.components.light import ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS, Light

from custom_components.switch.x10_tng import CONF_DEVICE, setup_x10, X10Switch  # WIP

REQUIREMENTS = ['x10_any>=0.0.6']

_LOGGER = logging.getLogger(__name__)


class X10Light(X10Switch):
    """Representation of an X10 lamp) module that supports dimming"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._brightness = 0

    @property
    def brightness(self):
        """Brightness of the light (an integer in the range 1-255)."""
        return self._brightness

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS

    def turn_on(self, **kwargs):
        """Turn the device on
        Optionally may set brightness level."""
        brightness = kwargs.get(ATTR_BRIGHTNESS, 255)  # (an integer in the range 1-255)
        if self._unit_number is None:
            state = 'all_lights_on'  # x10_any.LAMPS_ON
            brightness = 255  # doesn't matter what was passed in, dim is for single ids only, NOT for the entire house code
        else:
            state = 'ON'  # x10_any.ON
        if brightness != 255:
            # Assume in valid range 1-255
            state = 'xdim %d' % brightness
        self._device.x10_command(self._house_code, self._unit_number, state)
        # Now update state information
        self._state = True
        self._brightness = brightness
        self.update_ha_state()


def setup_platform(hass, config, add_devices, discovery_info=None):
    setup_x10(hass, config, add_devices, discovery_info=discovery_info, deviceclass=X10Light)
