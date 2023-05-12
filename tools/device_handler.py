import os
import yaml
from inspector import Inspector
from constants import Constants

class DeviceHandler:
    def __init__(self, print_enabled = True):
        self.yaml_file = self._get_yaml_file()
        self.inspector = Inspector(print_enabled=False)
        self.constants = Constants(print_enabled=False)
        self.print_enabled = print_enabled

    def _get_yaml_file(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_file = os.path.join(script_dir, "devices.yaml")
        print(yaml_file)
        return yaml_file

    def get_device_data(self, device_id):
        with open(self.yaml_file, "r") as file:
            devices = yaml.safe_load(file)

            for device in devices:
                if device.get("id") == device_id:
                    return device

        return None  # Return None if device ID is not found in the yaml file

    def refresh_devices(self):
        # Load existing devices from the yaml file with 'id' as the main property
        devices = self._load_devices_from_yaml()

        # Create a set of existing serial numbers
        existing_serial_numbers = set(device["serial_number"] for device in devices)

        # Get the current list of devices
        current_devices = self.inspector.list_devices()
        # Iterate through the current devices and check for new serial numbers
        for device in current_devices:
            serial_number = device["serial_number"]
            board_name = device["board_name"]

            # Check if a device with the same serial number already exists
            if serial_number in existing_serial_numbers:
                self.DPRINT(f"Device with serial number {serial_number} already exists. Skipping...")
                continue

            # Ask the user to input a new ID for the device
            new_device_id = input(f"Enter the ID for the new device with serial number {serial_number}: ")
            board_info = self.constants.get_board_info(board_name.lower())

            # Create a new device entry with the provided serial number and ID
            new_device = {
                "id": int(new_device_id),
                "serial_number": serial_number,
                "board_name": board_name.lower(),
                "chip_name": board_info[0],
                "series": board_info[1]
            }

            # Append the new device entry to the existing devices list
            devices.append(new_device)
            print(f"New device with ID {new_device_id} and serial number {serial_number} added successfully.")

        # Save the updated devices list to the yaml file
        with open(self.yaml_file, "w") as file:
            yaml.dump(devices, file, Dumper=yaml.SafeDumper, sort_keys=False)


    def _load_devices_from_yaml(self):
        if os.path.isfile(self.yaml_file):
            with open(self.yaml_file, "r") as file:
                devices = yaml.safe_load(file) or []
        else:
            devices = []
        return devices
    def print_devices(self):
        devices = self._load_devices_from_yaml()

        print("Devices:")
        for device in devices:
            print("-" * 30)
            for key, value in device.items():
                print(f"{key}: {value}")
        print("-" * 30)
        print("End of devices")

    def DPRINT(self, message):
        if not self.print_enabled:
            return
        prefix = "Device handler CLASS: "
        formatted_message = "{prefix:20}{message}".format(prefix=prefix, message=message)
        print(formatted_message)

def main():
    handler = DeviceHandler()
    # device_id = 1
    # device_data = handler.get_device_data(device_id)

    # if device_data:
    #     print(f"Device ID: {device_id}")
    #     print(f"Serial Number: {device_data['serial_number']}")
    #     print(f"Board Name: {device_data['board_name']}")
    #     chip_name = handler.constants.get_board_info(device_data['board_name'])
    #     print(f"Chip Name: {chip_name[0]}")
    #     print(f"Series: {chip_name[1]}")
    # else:
    #     print(f"Device ID {device_id} not found.")

    # Call the refresh_devices() function
    handler.refresh_devices()

    handler.print_devices()

if __name__ == "__main__":
    main()
