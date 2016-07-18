# custom_components/switch/x10.py

import logging

from homeassistant.helpers.entity import ToggleEntity
from homeassistant.const import DEVICE_DEFAULT_NAME, CONF_HOST, CONF_PORT, CONF_FILENAME

REQUIREMENTS = ['x10_any>=0.0.5']

_LOGGER = logging.getLogger(__name__)

"""
switch:
  - platform: x10
    switches:
      C6: Small Moon Lamp
"""

CONF_DEVICE = 'device'  # Matches zigbee component

def setup_platform(hass, config, add_devices, discovery_info=None):
    import x10_any

    device_config = config.get(CONF_DEVICE, 'mochad')
    if device_config == 'mochad':
        mochad_host = config.get(CONF_HOST, 'localhost')
        mochad_port = config.get(CONF_PORT, 1099)

        _LOGGER.info('Using network MochadDriver %r:%r', mochad_host, mochad_port)
        dev = x10_any.MochadDriver((mochad_host, mochad_port))
        # TODO extra config: default_type (rf|pl)
    elif device_config == 'cm17a':
        serial_port = config.get(CONF_FILENAME, None)  # Matches components, acer_projector.py

        # If serial_port is None, FirecrackerDriver will attempt to auto detect
        _LOGGER.info('Using serial FirecrackerDriver %r', serial_port)
        dev = x10_any.FirecrackerDriver(serial_port)
    else:
        _LOGGER.error('Invalid config. Valid values for %s, are `mochad` and `cm17a`', CONF_DEVICE)

    switches_config = config.get('switches')  # is there a predefined constant for this in homeassistant.const?
    switches = []
    for house_and_unit, name in switches_config.items():
        house_code, unit_number = house_and_unit[0], house_and_unit[1:]

        # should house_code, unit_number be validated here?
        # Validation will take place when attempting to switch on/off
        switches.append(X10Switch(dev, name, house_code, unit_number))
    add_devices(switches)


class X10Switch(ToggleEntity):
    """Representation of an X10 (switch/lamp) module"""

    def __init__(self, device, name, house_code, unit_number):
        self._device = device
        self._name = name or DEVICE_DEFAULT_NAME
        self._house_code = house_code
        self._unit_number = unit_number
        self._state = False

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state

    def turn_on(self):
        """Turn the device on."""
        #self._device.x10_command(self._house_code, self._unit_number, x10_any.ON)
        self._device.x10_command(self._house_code, self._unit_number, 'ON')
        # TODO success check?
        self._state = True
        self.update_ha_state()

    def turn_off(self):
        """Turn the device off."""
        #self._device.x10_command(self._house_code, self._unit_number, x10_any.OFF)
        self._device.x10_command(self._house_code, self._unit_number, 'OFF')
        # TODO success check?
        self._state = False
        self.update_ha_state()