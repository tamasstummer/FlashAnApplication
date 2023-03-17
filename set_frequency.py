import argparse
import os
import sys
import list_usb_devices
from constants import Constants

constants = Constants()
SERIES2_BOARDS = constants.get_S2_boards()
frequencies = constants.get_frequencies()

commander = "./tools/commander/commander.exe"

def parse_args():
  parser = argparse.ArgumentParser(description="Flash any sample application on any board")
  parser.add_argument('--serialno',  type=str, help="JLink serial nmber of the board",  nargs='?', default = "0")
  parser.add_argument('--board',     type=str, help="Name of the board",                nargs='?', default = "0")
  parser.add_argument('--region',    type=str, help="Region name",                      nargs='?', default = "0x01") # default is US
  global args
  args = parser.parse_args()

def check_valid_region(region_name):
    if region_name not in frequencies:
        print("Invalid or missing region name!")
        print("Example: python set_frequency.py --region EU")
        sys.exit(-1)


def set_region(serialno, chip_name, region_name):
    check_valid_region(region_name)
    print(commander + " flash --tokengroup znet --token MFG_ZWAVE_COUNTRY_FREQ:" + str(region_name)  + " -s " + str(serialno) + " -d " + str(chip_name))
    print("----------------------------------------------")
    print("Reset the region")
    # Reset the mfg token
    os.system(commander + " flash --tokengroup znet --token MFG_ZWAVE_COUNTRY_FREQ:" + str(frequencies.get(region_name))  + " -s " + str(serialno) + " -d " + str(chip_name))

def set_frequency():
    args.region = "REGION_" + args.region
    if args.board != "0":
      set_region(args.serialno, SERIES2_BOARDS[args.board.lower()], args.region)
      sys.exit(0)
    else:
        # Get the serial number and board type of the device
        (numer_of_devices, serialno, board, chip) = list_usb_devices.list_devices()
        if numer_of_devices == 0:
            print("No devices found")
            sys.exit(-1)
        if numer_of_devices == 1:
            set_region(serialno[0], chip[0], args.region)
            print("\nRegion set to " + args.region[7:] + " - (" + frequencies[args.region] + ")")
        else:
            print("More than one device found. Please specify the device serial number and board type")
            print("Example: python set_frequency.py --serialno 12345678 --board brd4204a --region EU")
            list_usb_devices.list_devices_and_print()
            sys.exit(-1)



if __name__ == "__main__":
    parse_args()
    set_frequency()