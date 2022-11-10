print("""\
 ______  _________ _        _______  _______             _______  _______  _______  _______           _______  _______ 
(  ___ \ \__   __/( (    /|(  ___  )(  ____ )|\     /|  (  ____ \(       )(  ___  )(  ____ \|\     /|(  ____ \(  ____ )
| (   ) )   ) (   |  \  ( || (   ) || (    )|( \   / )  | (    \/| () () || (   ) || (    \/| )   ( || (    \/| (    )|
| (__/ /    | |   |   \ | || (___) || (____)| \ (_) /   | (_____ | || || || (___) || (_____ | (___) || (__    | (____)|
|  __ (     | |   | (\ \) ||  ___  ||     __)  \   /    (_____  )| |(_)| ||  ___  |(_____  )|  ___  ||  __)   |     __)
| (  \ \    | |   | | \   || (   ) || (\ (      ) (           ) || |   | || (   ) |      ) || (   ) || (      | (\ (   
| )___) )___) (___| )  \  || )   ( || ) \ \__   | |     /\____) || )   ( || )   ( |/\____) || )   ( || (____/\| ) \ \__
|/ \___/ \_______/|/    )_)|/     \||/   \__/   \_/     \_______)|/     \||/     \|\_______)|/     \|(_______/|/   \__/
                                                                                                                       
""")

import os
import platform
import zipfile
import argparse
import sys
import glob
import yaml
import list_usb_devices
import subprocess

default_frquency = "US"
default_binary_extension = ".hex"

#Apps_before_22q2 and board definitions
#-----------------------------------------------------------------------------------------------
Apps_before_22q2 = ['SwitchOnOff', 'PowerStrip', 'SensorPIR', 'DoorLockKeyPad', 'WallController', 'LEDBulb', 'SerialAPI', 'ZnifferPTI']
NonCertifiableApps_before_22q2 = ['MultilevelSensor']

Apps = ['zwave_soc_switch_on_off', 'zwave_soc_power_strip', 'zwave_soc_sensor_pir', 'zwave_soc_door_lock_keypad', 'zwave_soc_wall_controller', 'zwave_soc_led_bulb', 'zwave_ncp_serial_api', 'zwave_ncp_zniffer_pti']
NonCertifiableApps = ['zwave_soc_multilevel_sensor']
TestApps = ['UL_testtool']


SERIES1_BOARDS= {
  "brd4200a": "ZGM130S",
  "brd4201a": "EFR32ZG14",
  "brd4202a": "ZGM130S",
  "brd4207a": "ZGM130S",
  "brd4208a": "EFR32ZG14",
  "brd4209a": "EFR32RZ13",
}

SERIES2_BOARDS= {
  "brd4204a" : "EFR32ZG23",
  "brd4204b" : "EFR32ZG23",
  "brd4204c" : "EFR32ZG23",
  "brd4204d" : "EFR32ZG23",
  "brd4205a" : "ZGM230S",
  "brd4205b" : "ZGM230S",
  "brd4210a" : "EFR32ZG23",
  "brd2603a" : "ZGM230S",
}

frequencies= {
  "REGION_EU"               : "0x00",
  "REGION_US"               : "0x01",
  "REGION_ANZ"              : "0x02",
  "REGION_HK"               : "0x03",
  "REGION_IN"               : "0x05",
  "REGION_IL"               : "0x06",
  "REGION_RU"               : "0x07",
  "REGION_CN"               : "0x08",
  "REGION_US_LR"            : "0x0A",
  "REGION_US_LR_BACKUP"     : "0x0B",
  "REGION_2CH_NUM"          : "0x0C",   #(REGION_US_LR_BACKUP - REGION_EU) + 1
  "REGION_JP"               : "0x20",
  "REGION_KR"               : "0x21",
  "REGION_3CH_NUM"          : "0x02",   #(REGION_KR - REGION_JP) + 1
  "REGION_US_LR_END_DEVICE" : "0x30",
  "EGION_LR_END_DEVICE_NUM" : "0x01",
  "REGION_UNDEFINED"        : "0xFE",
  "REGION_DEFAULT"          : "0xFF",
}

#-----------------------------------------------------------------------------------------------
# Parse the inputs first
parser = argparse.ArgumentParser(description="Flash any sample application on any board")
parser.add_argument('--serialno',          type=str, help="JLink serial nmber of the board",                   nargs='?', default = "0") 
parser.add_argument('--freq',              type=str, help="Frequency of the binary",                           nargs='?', default = default_frquency)
parser.add_argument('--board',             type=str, help="Target board.",                                                             )
parser.add_argument('--ext',         type=str, help="extension of the binary.",                          nargs='?', default = default_binary_extension)

args = parser.parse_args()

# ---------------------------------------------------------------------------------------------

def give_back_application_cathegory(application_name) -> str:
    if(application_name in Apps_before_22q2 or application_name in Apps):
        return "Apps"
    elif(application_name in NonCertifiableApps_before_22q2 or application_name in NonCertifiableApps):
        return "NonCertifiableApps"
    elif(application_name in TestApps):
        return "TestApps"
    else:
        print('The given application chategory is invalid')
        sys.exit(-1)
    return
def check_if_board_existing(board_name) -> str:
    if(board_name in SERIES1_BOARDS or board_name in SERIES2_BOARDS):
        return board_name
    else:
        print('The given board name is invalid')
        sys.exit(-1)
        return

def check_region(region_name) -> str:
    region_name = "REGION_" + region_name
    if(region_name in frequencies):
        return region_name
    else:
        print('The given frequency name is invalid')
        sys.exit(-1)
        return

def give_back_series(board_name) ->str:
    if(SERIES1_BOARDS.get(board_name) is not None):
        return ["SERIES1", SERIES1_BOARDS.get(board_name)]
    if(SERIES2_BOARDS.get(board_name) is not None):
        return ["SERIES2", SERIES2_BOARDS.get(board_name)]
    else:
        return [None, None]

def flash_application_binary(serialno, board_name, region_name, binary_extension) -> None:
    print("----------------------------------------------")
    print("Flash the hex files")

    hex_file_name = ""
    os.chdir("./binary_folder")
    for file in glob.glob("*." + binary_extension):
        print("Found hex file will be flashed: " + file)
        hex_file_name = file
        hex_file_path = "./binary_folder/" + file
        os.chdir("./..")
    [series, board] = give_back_series(board_name)
    if hex_file_name:
        #Reset device
        os.system(commander + " device masserase -s " + str(serialno) + " -d " + board)
        os.system(commander + " device reset -s " + str(serialno) + " -d " + board)
        if series is "SERIES2":
            region_name = check_region(region_name)

            # Reset the mfg token
            os.system(commander + " flash --tokengroup znet --token MFG_ZWAVE_COUNTRY_FREQ:" + frequencies.get(region_name)  + " -s " + str(serialno) + " -d " + board)

            #Flash the downloaded hex file
        os.system(commander + " flash " + hex_file_path + " -s " + str(serialno) + " -d " + board)
        if series is "SERIES2":
            #Get the region mfg token's value just for sure
            os.system(commander + " tokendump --tokengroup znet --token MFG_ZWAVE_COUNTRY_FREQ -s " + str(serialno) + " -d " + board)
        #Read the DSK
        print_out_dsk(serialno, board)

def print_out_dsk(serialno, board):
        cmd = commander + " tokendump --tokengroup znet --token MFG_ZW_QR_CODE -s " + str(serialno) + " -d " + board
        proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        # decode the binary output
        output = out.decode('UTF-8')
        print(output)
        # The QR code always starts with the 90 value
        sdk_position_in_string = output.find('90')
        # the SDK starts in from the 13th position in the qr code, and 40 caracters long
        sdk = output[sdk_position_in_string + 12 : sdk_position_in_string + 12 + 40]
        print("DSK value: ", end = "")
        for x in range(40):
            print(sdk[x], end = "")
            if (x + 1) % 5 == 0 and x > 0 and (x + 1) < 40:
                print("-", end = "")

def parse_config_values() -> None:
    global commander
    with open("config/config_parameters.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    for val in find_in_yaml(data_loaded, 'studio_location'):
        current_platform = sys.platform
        if current_platform == 'cygwin':
            val = str(val).replace('\\', '/')
        commander = val + "/developer/adapter_packs/commander/commander.exe"

def find_in_yaml(d, tag):
    if tag in d:
        yield d[tag]
    for k, v in d.items():
        if isinstance(v, dict):
            for i in find_in_yaml(v, tag):
                yield i

def check_serial_number(serialno) -> None:
    if serialno == "0":   # if no serialnumber is given from commandline
        myDevice = list_usb_devices.main()
        if myDevice[0] != "0":
            args.serialno = myDevice[0]
            args.board = myDevice[1].lower()
        else:
            print("Please use --serialno flag\n")
            sys.exit(-1)



def main() -> None:
    print("Flash any sample application on any board")
    parse_config_values()
    check_serial_number(args.serialno)
    flash_application_binary(args.serialno, args.board, args.freq, args.ext)

if __name__ == "__main__":
  main()
