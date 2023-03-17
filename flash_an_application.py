print("""\
  _______ _            ______ _           _               
 |__   __| |          |  ____| |         | |              
    | |  | |__   ___  | |__  | | __ _ ___| |__   ___ _ __ 
    | |  | '_ \ / _ \ |  __| | |/ _` / __| '_ \ / _ \ '__|
    | |  | | | |  __/ | |    | | (_| \__ \ | | |  __/ |   
    |_|  |_| |_|\___| |_|    |_|\__,_|___/_| |_|\___|_|   
""")

import os
import platform
import zipfile
import argparse
import sys
import glob
import yaml
import list_usb_devices
from constants import Constants
from get_DSK import print_out_dsk
# from get_frequency import get_frequency
# from set_frequency import set_frequency

default_frquency = "US"
default_branch = "develop%252F23q2" # develop/23q2
default_build = "lastSuccessfulBuild"

#Apps_before_22q2 and board definitions
#-----------------------------------------------------------------------------------------------
Apps_before_22q2 = ['SwitchOnOff', 'PowerStrip', 'SensorPIR', 'DoorLockKeyPad', 'WallController', 'LEDBulb', 'SerialAPI', 'ZnifferPTI']
NonCertifiableApps_before_22q2 = ['MultilevelSensor']

Apps = ['zwave_soc_switch_on_off', 'zwave_soc_power_strip', 'zwave_soc_sensor_pir', 'zwave_soc_door_lock_keypad', 'zwave_soc_wall_controller', 'zwave_soc_led_bulb', 'zwave_ncp_serial_api_controller', 'zwave_ncp_serial_api_end_device', 'zwave_ncp_zniffer_pti']
NonCertifiableApps = ['zwave_soc_multilevel_sensor']
TestApps = ['UL_testtool']

constants = Constants()
SERIES1_BOARDS = constants.get_S1_boards()
SERIES2_BOARDS = constants.get_S2_boards()
frequencies = constants.get_frequencies()

#-----------------------------------------------------------------------------------------------
# Parse the inputs first
def parse_args():
    parser = argparse.ArgumentParser(description="Flash any sample application on any board")
    parser.add_argument('--serialno',          type=str, help="JLink serial nmber of the board",                   nargs='?', default = "0") 
    parser.add_argument('--name',              type=str, help="Name of the application, you want to flash.",                               )
    parser.add_argument('--freq',              type=str, help="Frequency of the binary",                           nargs='?', default = default_frquency)
    parser.add_argument('--board',             type=str, help="Target board.",                                                             )
    parser.add_argument('--branch',            type=str, help="Name of a specific jenkins branch.",                nargs='?', default = default_branch)
    parser.add_argument('--build',             type=str, help="Specifies the number of the build on jenkins",      nargs='?', default = default_build)

    global args
    args = parser.parse_args()

# ---------------------------------------------------------------------------------------------
def download_application_binary(branch_name, build_name, app_name, board_name) -> None:
    print("Download app binary...")

    branch_name = branch_name.replace("/", "%252F")  # Jenkins needs this

    #Check every possible error at the begining
    app_chategory = give_back_application_cathegory(app_name)
    board_name = check_if_board_existing(board_name)
    extra_path_element = ""  # in case of the SerialAPI, we need a "Controller" element in the path
    if(app_name == "zwave_ncp_serial_api_controller"):
        extra_path_element = "controller/"
        app_name = "zwave_ncp_serial_api"
    if(app_name == "zwave_ncp_serial_api_end_device"):
        extra_path_element = "end_device/"
        app_name = "zwave_ncp_serial_api"
    global name_of_zip
    name_of_zip = app_name + ".zip"
    url = "https://zwave-jenkins.silabs.com/job/zw-zwave/job/" + branch_name + "/" + build_name + "/artifact/" + app_chategory + "/" + app_name + "/out/" + extra_path_element + board_name + "_" + "REGION_US_LR" + "/build/release/*zip*/" + name_of_zip
    print("This URL is the source of your hex file: " + url)

    os.system('wget ' + url)
    print("Done")

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
    if 'REGION' not in region_name:
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

def unzip_downloaded_binary() -> None:
    print("----------------------------------------------")
    print("Unzip downloaded stuff...")
    with zipfile.ZipFile(name_of_zip, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())
    return
    print("Done")

def flash_application_binary(serialno, board_name, region_name) -> None:
    print("----------------------------------------------")
    print("Flash the hex files")

    hex_file_name = ""
    os.chdir("./release")
    for file in glob.glob("*.hex"):
        print("Found hex file will be flashed: " + file)
        hex_file_name = file
        hex_file_path = "./release/" + file
        os.chdir("./..")
    [series, board] = give_back_series(board_name)
    if hex_file_name:
        #Reset device
        os.system(commander + " device masserase -s " + str(serialno) + " -d " + board)
        os.system(commander + " device reset -s " + str(serialno) + " -d " + board)
        if series == "SERIES2":
            region_name = check_region(region_name)

            # Reset the mfg token
            os.system(commander + " flash --tokengroup znet --token MFG_ZWAVE_COUNTRY_FREQ:" + frequencies.get(region_name)  + " -s " + str(serialno) + " -d " + board)

        # TODO we should use the new get_frequency/set_frequency commands here 
        #Flash the downloaded hex file
        os.system(commander + " flash " + hex_file_path + " -s " + str(serialno) + " -d " + board)
        if series == "SERIES2":
            #Get the region mfg token's value just for sure
            os.system(commander + " tokendump --tokengroup znet --token MFG_ZWAVE_COUNTRY_FREQ -s " + str(serialno) + " -d " + board)
        #Read the DSK
        print_out_dsk(serialno, board)

def delete_downloaded_files() -> None:
    test = os.listdir('.')

    for item in test:
        if item.endswith(".zip"):
            os.remove(os.path.join('.', item))
    if 'Windows' == platform.system():
        os.system('rmdir .\\release /s /q')
    else:     
        os.system("rm -rf release")

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
        # Get the serial number and board type of the device
        (numer_of_devices, serialno, board, chip) = list_usb_devices.list_devices()
        if numer_of_devices == 0:
            print("No devices found")
            sys.exit(-1)
        if numer_of_devices == 1:
            args.serialno = serialno[0]
            args.board = board[0]
            print("Found device with serial number: " + str(args.serialno) + " and board type: " + args.board + "\n")
        else:
            print("More than one device found. Please specify the device serial number and board type")
            print("Example: python3 flash_an_application.py --name zwave_soc_switch_on_off --freq US --branch develop/22q4 --build lastSuccessfulBuild --serialno 440262211 --board brd4205b")
            list_usb_devices.list_devices_and_print()
            sys.exit(-1)

def main() -> None:
    parse_args()
    parse_config_values()
    check_serial_number(args.serialno)
    delete_downloaded_files()
    download_application_binary(args.branch, args.build, args.name, args.board)
    unzip_downloaded_binary()
    flash_application_binary(args.serialno, args.board, args.freq)
    delete_downloaded_files()

if __name__ == "__main__":
  main()
