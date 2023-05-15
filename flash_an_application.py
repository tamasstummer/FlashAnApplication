print("""\
  _______ _            ______ _           _               
 |__   __| |          |  ____| |         | |              
    | |  | |__   ___  | |__  | | __ _ ___| |__   ___ _ __ 
    | |  | '_ \ / _ \ |  __| | |/ _` / __| '_ \ / _ \ '__|
    | |  | | | |  __/ | |    | | (_| \__ \ | | |  __/ |   
    |_|  |_| |_|\___| |_|    |_|\__,_|___/_| |_|\___|_|   
""")

import os
import shutil
import zipfile
import argparse
import glob
import sys

# Get the absolute path to the folder containing A.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Append the 'tools' folder to the sys.path
tools_path = os.path.join(current_dir, 'tools')
sys.path.append(tools_path)

# from tools.constants import Constants
from tools.inspector import Inspector
from tools.commander import Commander
from tools.device_handler import DeviceHandler

DEFBUG_PRINT_ENABLED = False

default_frquency = "US"
default_branch = "develop%252F23q2" # develop/23q2
default_build = "lastSuccessfulBuild"

#-----------------------------------------------------------------------------------------------
# Parse the inputs first
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Flash any sample application on any board")
    parser.add_argument('--name',              type=str, help="Name of the application, you want to flash.",                                                    )
    parser.add_argument('--freq',              type=str, help="Frequency of the binary",                                   nargs='?', default = default_frquency)
    parser.add_argument('--branch',            type=str, help="Name of a specific jenkins branch.",                        nargs='?', default = default_branch  )
    parser.add_argument('--build',             type=str, help="Specifies the number of the build on jenkins",              nargs='?', default = default_build   )
    parser.add_argument('--node',              type=str, help="Node number that hides the serial number and board type",                                        )
    return parser.parse_args()

def init_commander_class():
    return Commander(DEFBUG_PRINT_ENABLED)

def init_device_handler_class():
    return DeviceHandler(DEFBUG_PRINT_ENABLED)

# ---------------------------------------------------------------------------------------------
def download_application_binary(branch_name, build_name, app_name, node_id, device) -> None:
    print("Download app binary...")

    branch_name = branch_name.replace("/", "%252F")  # Jenkins needs this

    #Check every possible error at the begining
    app_chategory = device.constants.give_back_app_category(app_name)
    board_name = device.get_device_data(node_id)['board_name']

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

def unzip_downloaded_binary() -> None:
    print("----------------------------------------------")
    print("Unzip downloaded stuff...")
    with zipfile.ZipFile(name_of_zip, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())
    return

def flash_application_binary(app_name, region_name, node_id, commander, device_handler) -> None:
    print("----------------------------------------------")
    print("Flash the hex files")

    hex_files = glob.glob("./release/*.hex")
    if not hex_files:
        print("No hex files found")
        return

    hex_file_path = hex_files[0]
    hex_file_name = os.path.basename(hex_file_path)
    print("Hex file will be flashed: " + hex_file_name)

    constants = device_handler.constants

    device_data = device_handler.get_device_data(node_id)
    serial_number = device_data['serial_number']
    board_name = device_data['board_name']
    chip_name = constants.get_board_info(board_name)[0]
    series = constants.get_board_info(board_name)[1]
    frequency = constants.get_frequencies(region_name)

    # Reset device
    commander.reset_device(serial_number, chip_name)
    # Flash the downloaded hex file
    commander.flash_hex_file(hex_file_path, serial_number, chip_name)
    if series == "SERIES_2":
        commander.set_frequency(serial_number, chip_name, frequency)
        # Get the region mfg token's value just to be sure
        commander.read_frequency(serial_number, chip_name)

    # Read the DSK
    commander.read_dsk(serial_number, chip_name, app_name)


def delete_downloaded_files() -> None:
    current_dir = os.getcwd()

    for item in os.listdir(current_dir):
        item_path = os.path.join(current_dir, item)
        if item.endswith(".zip") and os.path.isfile(item_path):
            os.remove(item_path)

    release_dir = os.path.join(current_dir, 'release')
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)

def main() -> None:
    # Parse the input arguments
    args = parse_args()

    # Initialize the classes
    commander = init_commander_class()
    device_handler = init_device_handler_class()
    device_handler.refresh_devices()
    device_handler.print_devices()

    delete_downloaded_files()

    download_application_binary(args.branch, args.build, args.name, args.node, device_handler)
    unzip_downloaded_binary()
    flash_application_binary(args.name, args.freq, args.node, commander, device_handler)
    
    delete_downloaded_files()

if __name__ == "__main__":
  main()
