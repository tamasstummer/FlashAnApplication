import subprocess
import re
from constants import Constants
import os

class Inspector:
    def __init__(self, print_enabled = True):
        self.__pattern_serial_number = r"^device\((\d{9})\)"
        self.__pattern_board_name = r"\s*boardName\[\d+\]=([^\s]+) Rev"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.__inspector_path = os.path.join(script_dir, "inspect_emdll", "inspect_emdll.exe")
        self.__print_enabled = print_enabled

        self.__board_list = []
        self.__serial_number_list = []
        self.__number_of_devices = 0

    def list_devices(self):
        print("Searching for connected Silabs devices...\n\n")

        #call the magic Silabs tool
        command = self.__inspector_path +  " -slist"
        cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        
        # Loop through the output of the tool and extract the serial number and board name
        for line in cmd.stdout:
            ascii_line = line.decode('ascii')
            match = re.match(self.__pattern_serial_number, ascii_line)
            if (match):
                self.__serial_number_list.append(match.group(1))
                self.__number_of_devices += 1
                # self.__DPRINT("Found device with serial number: " + match.group(1))
            match = re.match(self.__pattern_board_name, ascii_line)
            if (match) and (match.group(1) != "BRD4001A") and (match.group(1) != "BRD4002A") and (match.group(1) != "BRD8029A"):
                    self.__board_list.append(match.group(1))
                    # self.__DPRINT("Found device with board name: " + match.group(1))

    def print_output(self):
        if self.__number_of_devices != 0:
            self.__DPRINT("Available devices:")
            for i in range(len(self.__board_list)):
                self.__DPRINT("Serial number: " + self.__serial_number_list[i] + " Board: " + self.__board_list[i])
        else:
            self.__DPRINT("No connected devices!")
    
    def __DPRINT(self, message):
        if not self.__print_enabled:
            return
        prefix = "Inspector CLASS: "
        formatted_message = "{prefix:20}{message}".format(prefix=prefix, message=message)
        print(formatted_message)

def main():
    inspector = Inspector()
    inspector.list_devices()
    inspector.print_output()
if __name__ == "__main__":
    main()
