import argparse
import sys

BOARDS = {
    "brd4200a": {"board_type": "ZGM130S",   "series": "SERIES_1"},
    "brd4201a": {"board_type": "EFR32ZG14", "series": "SERIES_1"},
    "brd4202a": {"board_type": "ZGM130S",   "series": "SERIES_1"},
    "brd4207a": {"board_type": "ZGM130S",   "series": "SERIES_1"},
    "brd4208a": {"board_type": "EFR32ZG14", "series": "SERIES_1"},
    "brd4209a": {"board_type": "EFR32RZ13", "series": "SERIES_1"},
    "brd4204a": {"board_type": "EFR32ZG23", "series": "SERIES_2"},
    "brd4204b": {"board_type": "EFR32ZG23", "series": "SERIES_2"},
    "brd4204c": {"board_type": "EFR32ZG23", "series": "SERIES_2"},
    "brd4204d": {"board_type": "EFR32ZG23", "series": "SERIES_2"},
    "brd4205a": {"board_type": "ZGM230S",   "series": "SERIES_2"},
    "brd4205b": {"board_type": "ZGM230S",   "series": "SERIES_2"},
    "brd4210a": {"board_type": "EFR32ZG23", "series": "SERIES_2"},
    "brd2603a": {"board_type": "ZGM230S",   "series": "SERIES_2"},
}

frequencies= {
  "EU"       : "0x00",
  "US"       : "0x01",
  "ANZ"      : "0x02",
  "HK"       : "0x03",
  "IN"       : "0x05",
  "IL"       : "0x06",
  "RU"       : "0x07",
  "CN"       : "0x08",
  "US_LR"    : "0x0A"
}

Apps = {"zwave_soc_switch_on_off" :         "Apps",
        "zwave_soc_power_strip" :           "Apps",
        "zwave_soc_sensor_pir" :            "Apps",
        "zwave_soc_door_lock_keypad" :      "Apps",
        "zwave_soc_wall_controller" :       "Apps",
        "zwave_soc_led_bulb" :              "Apps",
        "zwave_ncp_serial_api_controller" : "Apps",
        "zwave_ncp_serial_api_end_device" : "Apps",
        "zwave_ncp_zniffer_pti" :           "Apps",
        "zwave_soc_multilevel_sensor" :     "NonCertifiableApps",
        "zwave_soc_key_fob" :               "NonCertifiableApps",
        "UL_testtool" :                     "TestApps"}

class Constants:
  def __init__(self, print_enabled = True):
    self.BOARDS = BOARDS
    self.frequencies = frequencies
    self.print_enabled = print_enabled
  # function that returns a frequency dictionary

  def get_frequencies(self, key):
    if key in frequencies:
      return self.frequencies[key]
    else:
      self.DPRINT("The given frequency name is invalid")
      sys.exit(-1)
  
  # function that returns a board dictionary
  def get_board_info(self, key):
      if key in self.BOARDS:
          return self.BOARDS[key]["board_type"], self.BOARDS[key]["series"]
      else:
          self.DPRINT("The given board name is invalid")
          sys.exit(-1)

  def give_back_app_category(self, app_name):
    if app_name in Apps:
      return Apps[app_name]
    else:
      self.DPRINT("The given application name is invalid")
      sys.exit(-1)

  def DPRINT(self, message):
    if not self.print_enabled:
      return
    prefix = "Constants CLASS: "
    formatted_message = "{prefix:20}{message}".format(prefix=prefix, message=message)
    print(formatted_message)

