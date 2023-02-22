import subprocess
import re

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

usb_detector = "./tools/inspect_emdll/inspect_emdll.exe"

def list_devices():
    print("Searching for connected Silabs devices...\n\n")

    pattern_serial_number = r"^device\((\d{9})\)"
    patter_board_name = r"\s*boardName\[\d+\]=([^\s]+) Rev"

    # list of serial numbers, board names and chip names
    global board_list
    global serial_number_list
    global chip_list
    global number_of_devices 

    board_list = []
    serial_number_list = []
    chip_list = []
    number_of_devices = 0

    #call the magic silabs tool
    command = usb_detector +  " -slist"
    cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    for line in cmd.stdout:
        ascii_line = line.decode('ascii')
        match = re.match(pattern_serial_number, ascii_line)
        if (match):
            serial_number_list.append(match.group(1))
            number_of_devices += 1
        match = re.match(patter_board_name, ascii_line)
        if (match) and (match.group(1) != "BRD4001A") and (match.group(1) != "BRD8029A"):
            for board_name, board_chip in SERIES2_BOARDS.items():
                if board_name == match.group(1).lower():
                    board_list.append(board_name)
                    chip_list.append(board_chip)
    return (number_of_devices, serial_number_list, board_list, chip_list)

def print_output():
    if number_of_devices != 0:
        print("Available devices:")
        for i in range(len(board_list)):
            print("Serial number: " + serial_number_list[i] + " Board: " + board_list[i] + " Chip: " + chip_list[i])
    else:
        print("No connected devices!")

if __name__ == "__main__":
    list_devices()
    print_output()