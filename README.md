# x10 component for Home Assistant

Custom component https://home-assistant.io


### Table of Contents
* [Information](#information)
* [Notes](#notes)


## Information

Initial focus is supporting:
  * Mochad (or compatible) servers
  * CM17A serial or CM19A USB Firecracker X10 unit

## Getting Started

The source code is in two files `x10_tng.py` from the `light` and `switch` directories
these needs to be placed
`<config_dir>/custom_components/switch` and `<config_dir>/custom_components/light`
(i.e. under Windows,
`%APPDATA%\.homeassistant\custom_components\switch`, under Linux,
`~/.homeassistant/custom_components/switch`), etc.. Then edit `configuration.yaml`
(i.e. `%APPDATA%\.homeassistant\configuration.yaml` or
`~/.homeassistant/configuration.yaml`) and add a new switch:

TODO what to do about `switches` section?

    switch:
      - platform: x10_tng
        device: cm17a
        filename: COM11
        switches:
          C1: Hallway Lamp
          C2: Rocket Launcher
          D: All D
        devices:
          - id: b2
            name: B Living Room Lamp
          - id: b3
            name: B Bedroom Lamp
          - id: b5
    light:
      - platform: x10_tng
        device: cm17a
        filename: COM11
        switches:
          C1: LAMP Hallway Lamp
          C2: LAMP Rocket Launcher
          D: LAMP All D
        devices:
          - id: a2
            name: Living Room Lamp
          - id: a3
            name: Bedroom Lamp
          - id: a5

    # Define input_slider for brightness control demo
    # Based on https://home-assistant.io/components/input_slider/
    # NOTE slider does not get updated if lamp is switched off, this is mostly to see if you light/module supports dimming
    input_slider:
      bedroom_brightness:
        name: Brightness
        initial: 254
        min: 0
        max: 254
        step: 1

    automation:
      - alias: Bedroom Light - Adjust Brightness
        trigger:
          platform: state
          entity_id: input_slider.bedroom_brightness
        action:
          - service: light.turn_on
    # Note the use of 'data_template:' below rather than the normal 'data:' if you weren't using an input variable
            data_template:
              entity_id: light.bedroom_lamp
              brightness: '{{ trigger.to_state.state | int }}'

NOTE

  * `device` is the X10 controller device type. `mochad` or `cm17a` are the only valid options. If omitted defaults to `mochad`.
      * `mochad` specific settings:
          * `host` and `port` is the mochad server address. If omitted defaults to localhost:1099
      * `cm17a` specific settings (NOTE use this for cm19a device):
          * `filename` is the serial port device name, if omitted the device name is guessed.
  * if a house number is omitted, the entire house is used. ON == all lamps on, OFF = all (lamp+switches) on
  * `devices` is the same format that https://home-assistant.io/components/light.x10/ uses. Both `devices` and `switches` can be used or only one.

HA should auto install dependencies but in case it does not issue:

    pip install x10_any

### Serial Port Permissions under Linux

Under Linux most users do not have serial port permissions,
either:

  * give user permission (e.g. add to group "dialout") - RECOMMENDED
  * run this demo as root - NOT recommended!

Giver user dialout (serial port) access:

    # NOTE requires logout/login to take effect
    sudo usermod -a -G dialout $USER

## Notes

  * Does NOT implement state checks, it assumes the current state is the last state controlled via HA. Defaults to OFF on start up
    * Mochad status is not implemented
    * This means if a device is already ON when HA is started, two state changes are needed to really turn it off
  * No control over Mochad command type (yet), currently uses x10_any default of 'rf'
