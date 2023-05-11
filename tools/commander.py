import os
import re
import subprocess

class Commander:
    def __init__(self, print_enabled = True):
        # Parse the commander path next to the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.commander_path = os.path.join(script_dir, "commander", "commander.exe")
        #regex patter for extact the DSK from the output of the commander
        self.DSK_pattern = r'MFG_ZW_QR_CODE: "(\d+)"'
        self.__print_enabled = print_enabled

    def reset_device(self, serialno, chip_name):
        #Reset device
        os.system(self.commander_path + " device masserase -s " + str(serialno) + " -d " + chip_name)
        os.system(self.commander_path + " device reset -s " + str(serialno) + " -d " + chip_name)
        self.__DPRINT("Device with serial number " + str(serialno) + " and chip name " + chip_name + " has been reset")

    def set_frequency(self, serialno, chip_name, frequency):
         os.system(self.commander_path + " flash --tokengroup znet --token MFG_ZWAVE_COUNTRY_FREQ:" + frequency  + " -s " + str(serialno) + " -d " + chip_name)
         self.__DPRINT("Frequency set to " + frequency + " with chip name " + chip_name + " and serial number " + str(serialno))
    
    def read_frequency(self, serialno, chip_name):
        #Get the region mfg token's value just for sure
        os.system(self.commander_path + " tokendump --tokengroup znet --token MFG_ZWAVE_COUNTRY_FREQ -s " + str(serialno) + " -d " + chip_name)

    def flash_hex_file(self, hex_file_path, serialno, chip_name):
        os.system(self.commander_path + " flash " + hex_file_path + " -s " + str(serialno) + " -d " + chip_name)
        self.__DPRINT("Hex file flashed with chip name " + chip_name + " and serial number " + str(serialno))

    def read_dsk(self, serialno, chip_name, app_name):
        if app_name == "zwave_ncp_serial_api_controller":
            self.__DPRINT("No DSK for the serial API controller")
            return
        cmd = self.commander_path + " tokendump --tokengroup znet --token MFG_ZW_QR_CODE -s " + str(serialno) + " -d " + chip_name
        proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        # decode the binary output
        output = out.decode('UTF-8')
        # The QR code always starts with the 90 value
        match = re.search(self.DSK_pattern, output)
        if match:
            number = match.group(1)
            key = number[12:52]  # extract the key from the 13th place of the big number
            sections = [key[i:i+5] for i in range(0, len(key), 5)]  # split the key into 5 long sections of 5 digits each
            formatted_key = '-'.join(sections)  # join the sections with dashes
            self.__DPRINT("DSK: " + formatted_key)
        else:
            self.__DPRINT("No DSK found with " + chip_name + " and serial number " + str(serialno) + ". Please check the serial number and board type.")

    def __DPRINT(self, message):
        if not self.__print_enabled:
            return
        prefix = "Commander CLASS: "
        formatted_message = "{prefix:20}{message}".format(prefix=prefix, message=message)
        print(formatted_message)

def main():
    commander = Commander()
    commander.reset_device(440265308, "ZGM230")
    commander.set_frequency(440265308, "ZGM230", "0x00")
    commander.read_frequency(440265308, "ZGM230")

    commander.read_dsk(440265308, "ZGM230", "asd")
if __name__ == "__main__":
    main()
