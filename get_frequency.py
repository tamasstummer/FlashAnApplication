import argparse
import os
import sys
import subprocess
import list_usb_devices
import re
from constants import Constants

constants = Constants()
SERIES1_BOARDS = constants.get_S1_boards()
SERIES2_BOARDS = constants.get_S2_boards()
frequencies = constants.get_frequencies()

commander = "./tools/commander/commander.exe"

pattern = r'MFG_ZWAVE_COUNTRY_FREQ:\s+(0x[0-9A-Fa-f]+)'

def parse_args():
  parser = argparse.ArgumentParser(description="Flash any sample application on any board")
  parser.add_argument('--serialno',  type=str, help="JLink serial nmber of the board",  nargs='?', default = "0")
  parser.add_argument('--board',     type=str, help="Name of the board",                nargs='?', default = "0")
  global args
  args = parser.parse_args()


def get_region(serialno, chip_name):
  cmd = commander + " tokendump --tokengroup znet --token MFG_ZWAVE_COUNTRY_FREQ -s " + str(serialno) + " -d " + chip_name
  proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
  (out, err) = proc.communicate()
  # decode the binary output
  output = out.decode('UTF-8')
  print(output)
  match = re.search(pattern, output)
  if match:
    number = match.group(1)
    # get the key from the value in the frequencies dictionary
    print("The frequency is: " + [key for key, value in frequencies.items() if value == number][0] + " - (" + number + ")" )

def get_frequency():
    if args.board != "0":
      get_region(args.serialno, SERIES2_BOARDS[args.board.lower()])
      sys.exit(0)
    else:
        # Get the serial number and board type of the device
        (numer_of_devices, serialno, board, chip) = list_usb_devices.list_devices()
        if numer_of_devices == 0:
            print("No devices found")
            sys.exit(-1)
        if numer_of_devices == 1:
            get_region(serialno[0], chip[0])
        else:
            print("More than one device found. Please specify the device serial number and board type")
            print("Example: python get_frequency.py --serialno 12345678 --board brd4204a")
            list_usb_devices.list_devices_and_print()
            sys.exit(-1)

if __name__ == "__main__":
    parse_args()
    get_frequency()