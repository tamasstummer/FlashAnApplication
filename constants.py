

DICT_SERIES1_BOARDS= {
  "brd4200a": "ZGM130S",
  "brd4201a": "EFR32ZG14",
  "brd4202a": "ZGM130S",
  "brd4207a": "ZGM130S",
  "brd4208a": "EFR32ZG14",
  "brd4209a": "EFR32RZ13",
}

DICT_SERIES2_BOARDS= {
  "brd4204a" : "EFR32ZG23",
  "brd4204b" : "EFR32ZG23",
  "brd4204c" : "EFR32ZG23",
  "brd4204d" : "EFR32ZG23",
  "brd4205a" : "ZGM230S",
  "brd4205b" : "ZGM230S",
  "brd4210a" : "EFR32ZG23",
  "brd2603a" : "ZGM230S",
}

DICT_frequencies= {
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

class Constants:
    def __init__(self):
        self.DICT_SERIES1_BOARDS = DICT_SERIES1_BOARDS
        self.DICT_SERIES2_BOARDS = DICT_SERIES2_BOARDS
        self.DICT_frequencies = DICT_frequencies
    # function that returns a frequency dictionary
    def get_frequencies(self):
        return self.DICT_frequencies
    # function that returns a board dictionary
    def get_S1_boards(self):
        return self.DICT_SERIES1_BOARDS
    # function that returns a board dictionary
    def get_S2_boards(self):
        return self.DICT_SERIES2_BOARDS