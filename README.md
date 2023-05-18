# FlashAnAplication

This tool can be used in the z-wave team to automaticly flash an application to a selected board

What can it do for you:
 - connect to the internal jenkins pipeline, and download the desired application binariy
 - reset the board via commander
 - flash the binary to the board
 - flash bootloader binary to board
 - set the right region to the right MFG Token

Command switches:
 - name - Name of the aplication (example --name LedBulb)
 - freq - region (example --freq US)
 - branch - you can add what branch do you want to use (example --branch develop/22q2)
 - build - you can also add a specific build number of the build, or just the last successful (example --build lastSuccessfulBuild)
 - node - the node with a specific serial number, and board number

Every parameter is optional except serial number.
Default values if not given:

 - default_application - SwitchOnOff
 - default_frquency - US
 - default_branch - develop/23q2
 - default_build - lastSuccessfulBuild

List of Apps:
 - zwave_soc_switch_on_off
 - zwave_soc_power_strip
 - zwave_soc_sensor_pir
 - zwave_soc_door_lock_keypad
 - zwave_soc_wall_controller
 - zwave_soc_led_bulb
 - zwave_ncp_serial_api_controller
 - zwave_ncp_serial_api_end_device
 - zwave_ncp_zniffer_pti
 - zwave_soc_multilevel_sensor

Example call:

# SLC App:
```python
python flash_an_application.py --name zwave_soc_switch_on_off --freq US --branch develop/23q2 --build lastSuccessfulBuild --node 1
```
or a shorter call
```python
python flash_an_application.py --name zwave_soc_switch_on_off --node 1
```
# Binary flash
Put the binary to the binary_folder, and give the extension with the --ext flag (hex or s37)
```python
python flash_a_binary.py --freq US --serialno 440262211 --board brd4205b --ext s37
```

# Bootloader flash:
```python
python flash_bootloader.py --serialno 440269148 --board brd2603a
```