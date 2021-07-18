# Import
import os
import struct
from io import BytesIO
from pathlib import Path

import pycdlib


# Start   End      Mode Fno Source
# 0        274      0.0  0   "ZERO3.ims"
# 300000   301257   0.0  0   "SLPS_255.44"
# 301258   301392   0.0  0   "IOPRP300.IMG"
# 301393   301393   0.0  0   "SYSTEM.CNF"
# 301394   301506   0.0  0   "ZEROIRX.DIL"
# 301507   301507   0.0  0   "ZEROIRX.HIL"
# 301508   301643   0.0  0   "ZERO3.FHD"
# 301644   1635268  0.0  0   "IMG_BD.BIN"


def recursive_create_folder(folder_path_to_create):
    Path(folder_path_to_create).mkdir(parents=True, exist_ok=True)


def auto_patch(img_name, IMS_NAME):
    _LBA_START = 0
    _LBA_END = 0
    _LBA_LENGTH = 0
    img_size = os.path.getsize(img_name)
    _LBA_LENGTH = img_size / 2048

    fp = open(IMS_NAME, "rb+")
    fp.seek(0x829D6)
    fp.write(struct.pack("I", int(_LBA_LENGTH) * 2048))
    fp.write(struct.pack(">I", int(_LBA_LENGTH) * 2048))
    #fp.seek(0x88038)
    #fp.write(struct.pack("I", int(_LBA_LENGTH) * 2048))
    #fp.write(struct.pack("I", 0))
    #fp.write(struct.pack("I", int(_LBA_LENGTH)))
    fp.close()


def patch_iml(folder):
    file_size = os.path.getsize(f'{folder}/img_bd.bin')
    new_size = str(int((file_size + 819200000) >> 0xb) - 1)
    fp = open(f'{folder}/ff2.iml', 'r+')
    fp.seek(0x2C3)
    fp.write(new_size)
    fp.close()


def extract_db_file_from_jp_iso(folder, file_name):
    iso = pycdlib.PyCdlib()
    iso.open(f'{folder}/{file_name}')
    recursive_create_folder(f'{folder}/JP')

    with iso.open_file_from_iso(iso_path=f'/IMG_BD.BIN;1') as infp:
        infp.seek(0)
        write_file = open(f'{folder}/JP/IMG_BD.BIN', 'wb+')
        write_file.write(infp.read())
        write_file.close()
    iso.close()


def extract_all_files_from_iso(folder, iso_file_name):
    iso = pycdlib.PyCdlib()
    iso.open(f'{folder}/{iso_file_name}')

    for child in iso.list_children(iso_path='/'):
        if child.file_identifier() == b'.' or child.file_identifier() == b'..':
            continue

        print(child.file_identifier().decode("utf-8"))
        with iso.open_file_from_iso(iso_path=f'/{child.file_identifier().decode("utf-8")}') as infp:
            infp.seek(0)
            write_file = open(f'{folder}/{child.file_identifier().decode("utf-8").split(";")[0].lower()}', 'wb+')
            write_file.write(infp.read())
            write_file.close()

    iso.close()


if __name__ == '__main__':
    extract_all_files_from_iso('D:/DecompressFiles/Fatal Frame 2 Undub', 'Fatal Frame II - Crimson Butterfly.iso')
