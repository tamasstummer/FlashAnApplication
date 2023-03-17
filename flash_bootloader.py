print("""\
  ____              _   _                 _             _               _            
 |  _ \            | | | |               | |           | |             | |           
 | |_) | ___   ___ | |_| | ___   __ _  __| | ___ _ __  | |__  _   _ ___| |_ ___ _ __ 
 |  _ < / _ \ / _ \| __| |/ _ \ / _` |/ _` |/ _ \ '__| | '_ \| | | / __| __/ _ \ '__|
 | |_) | (_) | (_) | |_| | (_) | (_| | (_| |  __/ |    | |_) | |_| \__ \ ||  __/ |   
 |____/ \___/ \___/ \__|_|\___/ \__,_|\__,_|\___|_|    |_.__/ \__,_|___/\__\___|_|   
                                                           
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

default_branch = "develop%252F23q2" # develop/23q2
default_build = "lastSuccessfulBuild"
default_type = "ota"

BOARDS = {
  "brd4200a": "ZGM130S",
  "brd4201a": "EFR32ZG14",
  "brd4202a": "ZGM130S",
  "brd4207a": "ZGM130S",
  "brd4208a": "EFR32ZG14",
  "brd4209a": "EFR32RZ13",
  "brd4204a" : "EFR32ZG23",
  "brd4204b" : "EFR32ZG23",
  "brd4204c" : "EFR32ZG23",
  "brd4204d" : "EFR32ZG23",
  "brd4205a" : "ZGM230S",
  "brd4205b" : "ZGM230S",
  "brd4210a" : "EFR32ZG23",
  "brd2603a" : "ZGM230S",
  "brd4000a" : "EFR32ZG28",
  "brd4000b" : "EFR32ZG28",
  "brd4401a" : "EFR32ZG28",
  "brd4401b" : "EFR32ZG28",
}  


#-----------------------------------------------------------------------------------------------
# Parse the inputs first
parser = argparse.ArgumentParser(description="Flash any sample application on any board")
parser.add_argument('--serialno',          type=str, help="JLink serial nmber of the board",                   nargs='?', default = "0") 
parser.add_argument('--type',              type=str, help="OTA or OTW, default is OTA",                        nargs='?', default = default_type)
parser.add_argument('--board',             type=str, help="Target board",                                                             )
parser.add_argument('--branch',            type=str, help="Name of a specific jenkins branch.",                nargs='?', default = default_branch)
parser.add_argument('--build',             type=str, help="Specifies the number of the build on jenkins",      nargs='?', default = default_build)

args = parser.parse_args()

# ---------------------------------------------------------------------------------------------
def download_bootloader_binary(branch_name, build_name, board_name, type) -> None:
    print("Download app binary...")

    check_if_board_existing(board_name)

    branch_name = branch_name.replace("/", "%2F")  # Jenkins needs this
    folder_name = type + "-" + BOARDS[board_name] + "_" + board_name.upper()
    print(folder_name)

    global name_of_bootloader
    name_of_bootloader = folder_name + "-crc.s37"

    url = "https://zwave-jenkins.silabs.com/job/zw/job/zwave_platform_build/job/" + branch_name + "/" + build_name + "/" + "artifact/protocol/z-wave/UCBootLoader/build/" + folder_name + "/" + name_of_bootloader
    print("This URL is the source of your hex file:\n" + url + "\n")

    os.system('wget ' + url)
    print("Flashing done")

def check_if_board_existing(board_name) -> str:
    if(board_name in BOARDS):
        return board_name
    else:
        print('The given board name is invalid')
        sys.exit(-1)
        return

def flash_bootloader_binary(serialno, board_name) -> None:
    print("----------------------------------------------")
    print("Flash the hex files")

    #Reset device
    os.system(commander + " device masserase -s " + str(serialno) + " -d " + BOARDS[board_name])
    
    os.system(commander + " device reset -s " + str(serialno) + " -d " + BOARDS[board_name])
    
    #Flash the downloaded hex file
    os.system(commander + " flash " + name_of_bootloader + " -s " + str(serialno) + " -d " + BOARDS[board_name])

def delete_downloaded_files() -> None:
    test = os.listdir('.')

    for item in test:
        if item.endswith(".s37"):
            os.remove(os.path.join('.', item))
            print("Remove *.s37 file")

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
    parse_config_values()
    check_serial_number(args.serialno)
    download_bootloader_binary(args.branch, args.build, args.board, args.type)
    flash_bootloader_binary(args.serialno, args.board)
    delete_downloaded_files()

if __name__ == "__main__":
  main()
