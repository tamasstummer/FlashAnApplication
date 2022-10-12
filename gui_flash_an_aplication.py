import tkinter as tk
from tkinter import ttk
import subprocess

Apps = ['zwave_soc_switch_on_off', 'zwave_soc_power_strip', 'zwave_soc_sensor_pir', 'zwave_soc_door_lock_keypad', 'zwave_soc_wall_controller', 'zwave_soc_led_bulb', 'zwave_ncp_serial_api', 'zwave_ncp_zniffer_pti']
NonCertifiableApps = ['zwave_soc_multilevel_sensor']


SERIES1_BOARDS= {
  "brd4200a": "ZGM130S",
  "brd4201a": "EFR32ZG14",
  "brd4202a": "ZGM130S",
  "brd4207a": "ZGM130S",
  "brd4208a": "EFR32ZG14",
  "brd4209a": "EFR32RZ13",
}

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

frequencies= {
  "REGION_EU"               : "0x00",
  "REGION_US"               : "0x01",
  "REGION_ANZ"              : "0x02",
  "REGION_HK"               : "0x03",
  "REGION_IN"               : "0x05",
  "REGION_IL"               : "0x06",
  "REGION_RU"               : "0x07",
  "REGION_CN"               : "0x08",
  "REGION_US_LR"            : "0x0A",
  "REGION_US_LR_BACKUP"     : "0x0B",
  "REGION_2CH_NUM"          : "0x0C",   #(REGION_US_LR_BACKUP - REGION_EU) + 1
  "REGION_JP"               : "0x20",
  "REGION_KR"               : "0x21",
  "REGION_3CH_NUM"          : "0x02",   #(REGION_KR - REGION_JP) + 1
  "REGION_US_LR_END_DEVICE" : "0x30",
  "EGION_LR_END_DEVICE_NUM" : "0x01",
  "REGION_UNDEFINED"        : "0xFE",
  "REGION_DEFAULT"          : "0xFF",
}


def flash_and_application_gui():
  window = tk.Tk()
  window.title('Flash an application')
  window.geometry('1024x512')

  ttk.Label(window, text='Welcome on FlashAnApplication GUI',
    font = ("Times New Roman", 10)).grid(column = 0, 
    row = 0)

  # Create a combobox with applications
  ttk.Label(window, text='Choose application: ',
    font = ("Times New Roman", 10)).grid(column = 0, 
    row = 5, padx = 10, pady = 25)

  i = tk.StringVar()

  app_list = []

  for app in Apps:
    app_list.append(app)
    
  for app in NonCertifiableApps:
    app_list.append(app)

  apps_combobox_values = ttk.Combobox(window, width=30, textvariable=i)
  apps_combobox_values['values'] = tuple(app_list)

  apps_combobox_values.grid(column=1, row=5)
  apps_combobox_values.current(0)


  # Create a combobox with boards
  ttk.Label(window, text='Choose board: ',
    font = ("Times New Roman", 10)).grid(column = 0, 
    row = 15, padx = 10, pady = 25)

  n = tk.StringVar()
  board_combobox_values = ttk.Combobox(window, width=30, textvariable=n)

  board_list = []

  for boards in SERIES1_BOARDS:
    board_list.append(boards)
    
  for boards in SERIES2_BOARDS:
    board_list.append(boards)

  board_combobox_values['values'] = tuple(board_list)

  board_combobox_values.grid(column=1, row=15)
  board_combobox_values.current(11)

  # Crete combobox with frequencies
  ttk.Label(window, text='Choose region: ',
    font = ("Times New Roman", 10)).grid(column = 0, 
    row = 16, padx = 10, pady = 25)

  m = tk.StringVar()
  frequency_combobox_values = ttk.Combobox(window, width=30, textvariable=m)

  region_list = []

  for frequency in frequencies:
    region_list.append(frequency)
    
  frequency_combobox_values['values'] = tuple(region_list)

  frequency_combobox_values.grid(column=1, row=16)
  frequency_combobox_values.current(0)

  def flash():
    subprocess.call(f'py flash_an_application.py --name {apps_combobox_values.get()} --freq {frequency_combobox_values.get()} --branch develop/22q4 --build lastSuccessfulBuild --board {board_combobox_values.get()}')

  # flash button
  ttk.Button(window, text='Flash', command=flash).grid(column = 0, row = 20, padx = 10, pady = 25)


  window.mainloop()

if __name__ == '__main__':
  flash_and_application_gui()
