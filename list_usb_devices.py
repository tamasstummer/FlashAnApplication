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


def main() -> None:

    with open("config/config_parameters.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    for val in find_in_yaml(data_loaded, 'studio_location'):
        usb_detector = val + "developer/adapter_packs/inspect_emdll/inspect_emdll.exe"

    print("Searching for connected Silabs devices...\n\n")
    print("Available devices:")
    command = usb_detector +  " -slist"
    cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    found_board = ""
    for line in cmd.stdout:
        if b"(440" in line:
            serial_number = line[7:-5].decode("utf-8")
        if b"adapterName" in line:
            found_board = serial_number + " --- " + line[14:].decode("utf-8")
            print(found_board)
    if found_board == "":
        print("No connected devices!")

if __name__ == "__main__":
  main()