import yaml
import os
import subprocess

usb_monitor = ""

def find_in_yaml(d, tag):
    if tag in d:
        yield d[tag]
    for k, v in d.items():
        if isinstance(v, dict):
            for i in find(v, tag):
                yield i


def main():

    with open("config/config_parameters.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    for val in find_in_yaml(data_loaded, 'studio_location'):
        usb_detector = val + "developer/adapter_packs/inspect_emdll/inspect_emdll.exe"

    print("Searching for connected Silabs devices...\n\n")
    print("Available devices:")
    command = usb_detector +  " -slist"
    cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    found_board_string = ""
    number_of_found_board = 0
    found_serial_number = ""
    found_board_name = ""
    for line in cmd.stdout:
        #print(line)
        if b"(440" in line:
            serial_number = line[7:-5].decode("utf-8")
        if b"boardName[0]=BRD2603A" in line or b"boardName[1]=BRD42" in line:
            found_board_string = serial_number + " --- " + line[15:].decode("utf-8")
            print(found_board_string)
            number_of_found_board = number_of_found_board + 1
            found_serial_number = serial_number
            found_board_name = line[15:23].decode("utf-8")
    if number_of_found_board == 0:
        print("No connected devices!")
        return "0", "0"
    elif number_of_found_board == 1:
        return found_serial_number, found_board_name
    else:
        return "0", "0"

if __name__ == "__main__":
  main()