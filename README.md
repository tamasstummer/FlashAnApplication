# FlashAnAplication

This tool can be used in the z-wave team to automaticly flash an application to a selected board

What can it do for you:
 - connect to the internal jenkins pipeline, and download the desired application binariy
 - reset the board via commander
 - flash the binary to the board
 - set the right region to the right MFG Token

What steps are needed before first run:
 - get python3
 - get cygwin or WSL
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
 - default_build - lastsuccessful
 - default_branch - develop/22q2
 - default_build - lastSuccessfulBuild

List of Apps:
 - zwave_soc_switch_on_off
 - zwave_soc_power_strip
 - zwave_soc_sensor_pir
 - zwave_soc_door_lock_keypad
 - zwave_soc_wall_controller
 - zwave_soc_led_bulb
 - zwave_ncp_serial_api
 - zwave_ncp_zniffer_pti
 - zwave_soc_multilevel_sensor

Example call:
```
python3 flash_an_application.py --name zwave_soc_switch_on_off --freq US --branch develop/22q4 --build lastSuccessfulBuild --serialno 440262211 --board brd4205d
```