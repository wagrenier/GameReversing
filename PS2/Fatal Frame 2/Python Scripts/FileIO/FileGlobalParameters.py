# Import statements
import json
from enum import Enum


class FileStatus(Enum):
    NO_FILE = 0
    FILE_NOT_COMPRESSED = 2
    FILE_COMPRESSED = 3
    UNKNOWN_FILE = 4


# Define global values
DEBUG = False
sector_size = 0x800  # 2048 bytes

# Number of files in the cddat
disp_file_data = 0x00404188  # Seems to be an 2D array with 2 elements of length 4
project_file_num = 0x106B
p_cd_dat = 0x002F30B8
p_ext_lbl = 0x002FF5C0
file_dat_tbl = [0x002b6b80, 0x002b6c28, 0x002b6cd0, 0x002b6d70, 0x002b6dd8]
cd_dat_tbl = {}
file_ext_dat = {}

# For Japanese version
#p_cd_dat = 0x002F25F8

debug_output = open('output.txt', 'w')

# Reading values from json file
with open('cd_dat_tbl.json') as f:
    cd_dat_tbl = json.load(f)

with open('file_ext_tbl.json') as f:
    file_ext_dat = json.load(f)


def open_file_ext_tbl():
    with open('file_ext_tbl.json') as f:
        file_ext_dat = json.load(f)

    return file_ext_dat

def open_cd_dat_tbl():
    with open('cd_dat_tbl.json') as f:
        cd_dat_tbl = json.load(f)

    return cd_dat_tbl
