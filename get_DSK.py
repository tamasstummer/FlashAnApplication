
import subprocess
import re
import os
import argparse
import list_usb_devices
import sys
import list_usb_devices

commander = "./tools/commander/commander.exe"

# TODO move this to a separate file
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

parser = argparse.ArgumentParser(description="Flash any sample application on any board")
parser.add_argument('--serialno',  type=str, help="JLink serial nmber of the board",  nargs='?', default = "0")
parser.add_argument('--board',     type=str, help="Name of the board",                nargs='?', default = "0")
args = parser.parse_args()

#regex patter for extact the DSK from the output of the commander
pattern = r'MFG_ZW_QR_CODE: "(\d+)"'


def print_out_dsk(serialno, board):
        cmd = commander + " tokendump --tokengroup znet --token MFG_ZW_QR_CODE -s " + str(serialno) + " -d " + board
        proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        # decode the binary output
        output = out.decode('UTF-8')
        # The QR code always starts with the 90 value
        match = re.search(pattern, output)
        if match:
            number = match.group(1)
            key = number[11:51]  # extract the key from the 12th place of the big number
            sections = [key[i:i+5] for i in range(0, len(key), 5)]  # split the key into 5 long sections of 5 digits each
            formatted_key = '-'.join(sections)  # join the sections with dashes
            print("DSK: " + formatted_key)
        else:
            print("No DSK found with " + board + " and serial number " + str(serialno) + ". Please check the serial number and board type.")


if __name__ == "__main__":

    if args.board != "0":
        print_out_dsk(args.serialno, SERIES2_BOARDS[args.board.lower()])
        sys.exit(0)
    else:
        # Get the serial number and board type of the device
        (numer_of_devices, serialno, board, chip) = list_usb_devices.list_devices()
        if numer_of_devices == 0:
            print("No devices found")
            sys.exit(-1)
        if numer_of_devices == 1:
            print_out_dsk(serialno[0], chip[0])
        else:
            print("More than one device found. Please specify the device serial number and board type")
            print("Example: python get_DSK.py --serialno 123456789 --board brd4204a")
            sys.exit(-1)