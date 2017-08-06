# custom_components/switch/x10_tng.py
"""
Support for X10 modules via Mochad or CM17a FireCracker.
Both modules/switches and lights are supported (brightness for
lamps not implemented).

For more information and documentation see
https://github.com/clach04/home-assistant-x10
"""

import logging

from homeassistant.helpers.entity import ToggleEntity
from homeassistant.const import DEVICE_DEFAULT_NAME, CONF_DEVICES, CONF_HOST, CONF_ID, CONF_NAME, CONF_PORT, CONF_FILENAME

REQUIREMENTS = ['x10_any>=0.0.6']

_LOGGER = logging.getLogger(__name__)

"""
switch:
  - platform: x10
    switches:
      C6: Small Moon Lamp
"""

CONF_DEVICE = 'device'  # Matches zigbee component


class X10Switch(ToggleEntity):
    """Representation of an X10 (switch/lamp) module"""

    def __init__(self, device, name, house_code, unit_number):
        self._device = device
        self._name = name or DEVICE_DEFAULT_NAME
        self._house_code = house_code
        self._unit_number = unit_number
        self._state = False  # on (True) or off (False)?

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
        # returns cached state
        return self._state

    def turn_on(self):
        """Turn the device on."""
        if self._unit_number is None:
            state = 'all_lights_on'  # x10_any.LAMPS_ON
        else:
            state = 'ON'  # x10_any.ON
        self._device.x10_command(self._house_code, self._unit_number, state)
        # TODO success check?
        self._state = True
        if (MAJOR_VERSION, MINOR_VERSION) >= (0, 39):
            self.schedule_update_ha_state()
        else:
            # TODO remove this!
            self.update_ha_state()

    def turn_off(self):
        """Turn the device off."""
        if self._unit_number is None:
            state = 'all_units_off'  # x10_any.ALL_OFF
        else:
            state = 'OFF'  # x10_any.OFF
        self._device.x10_command(self._house_code, self._unit_number, state)
        # TODO success check?
        self._state = False
        if (MAJOR_VERSION, MINOR_VERSION) >= (0, 39):
            self.schedule_update_ha_state()
        else:
            # TODO remove this!
            self.update_ha_state()

    '''
    def update(self):
        """Fetch new state data for this switch.

        This is the only method that should fetch new data for Home Assistant.
        """
        # (Probably) called every 30 seconds
        # is_on() should then return that state
        _LOGGER.info('update() called')
    '''


def setup_x10(hass, config, add_devices, discovery_info=None, deviceclass=X10Switch):
    """Same API as setup_platform but with an additional parameter, the Class to use
    setup_platform() will essentially be currying this function.
    """
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
    if switches_config:
        for house_and_unit, name in switches_config.items():
            house_code, unit_number = house_and_unit[0], house_and_unit[1:]
            if unit_number == '':
                # Assume this is for the whole house
                unit_number = None

            # should house_code, unit_number be validated here?
            # Validation will take place when attempting to switch on/off
            _LOGGER.info('Adding switch %s%r', deviceclass.__name__, (dev, name, house_code, unit_number))
            switches.append(deviceclass(dev, name, house_code, unit_number))

    # Config/settings compatibility with https://home-assistant.io/components/light.x10/
    config_devices = config.get(CONF_DEVICES, [])
    for x10_device in config_devices:
        house_and_unit = x10_device[CONF_ID]
        name = x10_device.get(CONF_NAME, house_and_unit)

        house_code, unit_number = house_and_unit[0], house_and_unit[1:]
        if unit_number == '':
            # Assume this is for the whole house
            unit_number = None

        # should house_code, unit_number be validated here?
        # Validation will take place when attempting to switch on/off
        _LOGGER.info('Adding x10_device %s%r', deviceclass.__name__, (dev, name, house_code, unit_number))
        # TODO Add lamp/light support with dimming feature
        switches.append(deviceclass(dev, name, house_code, unit_number))

    add_devices(switches)


def setup_platform(hass, config, add_devices, discovery_info=None):
    setup_x10(hass, config, add_devices, discovery_info=discovery_info, deviceclass=X10Switch)
