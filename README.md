# FlashAnAplication

This tool can be used in the z-wave team to automaticly flash an application to a selected board

What can it do for you:
 - connect to the internal jenkins pipeline, and download the desired application binariy
 - reset the board via commander
 - flash the binary to the board
 - flash bootloader binary to board
 - set the right region to the right MFG Token

What steps are needed before first run:
 - get python3
 - get cygwin or WSL (or wget with Chocolatey and it will work from PS)
 - in ~/config/config_parameters.yaml update the paths accordingly

Command switches:
 - serialno -  Jlink serial number. If not privided, the program automaticly list all the connected serial numbers (example --serialno 440262211)
 - name - Name of the aplication (example --name LedBulb)
 - freq - region (example --freq US)
 - board - board name (example --board brd4205b)
 - branch - you can add what branch do you want to use (example --branch develop/22q2)
 - build - you can also add a specific build number of the build, or just the last successful (example --build lastSuccessfulBuild)

Every parameter is optional except serial number.
Default values if not given:

 - default_application - SwitchOnOff
 - default_board - brd4205b
 - default_frquency - US
 - default_branch - develop/22q4
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
```
SLC App:
python3 flash_an_application.py --name zwave_soc_switch_on_off --freq US --branch develop/22q4 --build lastSuccessfulBuild --serialno 440262211 --board brd4205b

SLC Workspace:
python3 flash_a_workspace.py --name zwave_soc_switch_on_off --branch feature/gekoczia/SWPROT-7368_introduce_SLC_workspaces --build lastSuccessfulBuild --serialno 440262211 --board brd4205b --freq US

Binary flash:
Put the binary to the binary_folder, and give the extension with the --ext flag (hex or s37)
python3 flash_a_binary --freq US --serialno 440262211 --board brd4205b --ext s37

Bootloader flash:
python3 flash_bootloader.py --serialno 440269148 --board brd2603a

```

# FlashAnApplication GUI

To start the basic GUI simply start the `.\FlashAnApplication.bat`. Choose the application, board and frequency.

## Limitations (under develop)

- If two or more devices are connected to the host this won't work.
- You can't choose, which build to flash, because this script will always choose the lastSuccessfulBuild.