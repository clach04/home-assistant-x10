# x10 component for Home Assistant

Custom component https://home-assistant.io


### Table of Contents
* [Information](#information)
* [Notes](#notes)


## Information

Initial focus is supporting:
  * Mochad (or compatible) servers
  * CM17A serial Firecracker X10 unit

## Getting Started

The source code is a single file `x10.py` this needs to be placed
`<config_dir>/custom_components/switch` (i.e. under Windows,
`%APPDATA%\.homeassistant\custom_components\switch`, under Linux,
`~/.homeassistant/custom_components/switch`). Then edit `configuration.yaml`
(i.e. `%APPDATA%\.homeassistant\configuration.yaml` or
`~/.homeassistant/configuration.yaml`) and add a new switch:

    switch:
      - platform: x10
        device: cm17a
        filename: COM11              # (optional)
        #device: mochad
        #host: 192.168.11.22          # (optional)
        #port: 1099                   # (optional)
        switches:
          C1: Hallway Lamp
          C2: Rocket Launcher
          D: All D
        lights:
          - name: Living Room Lamp
            id: a2
          - name: Bedroom Lamp
            id: a3
          - id: a5

NOTE

  * `device` is the X10 controller device type. `mochad` or `cm17a` are the only valid options. If omitted defaults to `mochad`.
  * `filename` is the serial port device name, if omitted the device name is guessed.
      * Windows: COM3
      * Linux: /dev/ttyS0

  * `Mocad` specific settings:
          * `host` is the mochad server address. If ommited defaults to localhost.
          * `port` port.  If omitted defaults to 1099.
  * if a house number is omitted, the entire house is used. ON == all lamps on, OFF = all (lamp+switches) on

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
