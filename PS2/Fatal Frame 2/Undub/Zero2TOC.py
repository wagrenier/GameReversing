# Import statement
import json
from enum import Enum

sector_size = 0x800
project_file_num_ = 0x106B
p_cd_dat_us = 0x002F30B8
p_cd_dat_jp = 0x002F25F8
p_ext_lbl = 0x002FF5C0
cd_dat_tbl_us = {}
cd_dat_tbl_jp = {}
file_ext_dat_a = []

with open('cd_dat_tbl.json') as f:
    cd_dat_tbl_us = json.load(f)

with open('cd_dat_tbl_jp.json') as f:
    cd_dat_tbl_jp = json.load(f)

with open('file_ext_tbl.json') as f:
    file_ext_dat_a = json.load(f)


class FileStatus(Enum):
    NO_FILE = 0
    FILE_NOT_COMPRESSED = 2
    FILE_COMPRESSED = 3
    UNKNOWN_FILE = 4


def create_jp_db():
    return Zero2TOC(project_file_num_, p_cd_dat_jp, p_ext_lbl, cd_dat_tbl_jp, file_ext_dat_a)


def create_us_db():
    return Zero2TOC(project_file_num_, p_cd_dat_us, p_ext_lbl, cd_dat_tbl_us, file_ext_dat_a)


def print_file_info(file):
    file_debug_string = 'Id:{},Type:{},StartSector:{},StartAddrLBA:{},FileEndLBA:{},Size:{},SizeCmp:{}\n'.format \
            (
            hex(file['Id']), file['Type'], hex(file['StartSector']), hex(file['BinStartAddr']),
            hex(file['BinEndAddr']),
            hex(file['Size']), hex(file['SizeCmp'])
        )

    print(file_debug_string)


def compute_img_bin_file_address(file):
    # Computes the lba for the file, rather than the address within the ISO
    return (file >> 2) * sector_size


class Zero2TOC:
    def __init__(self, project_file_num, p_cd_dat, p_ext_lbl, cd_dat_tbl, file_ext_dat):
        self.project_file_num = project_file_num
        self.file_table = []
        self.p_cd_dat = p_cd_dat
        self.p_ext_lbl = p_ext_lbl
        self.cd_dat_tbl = cd_dat_tbl
        self.file_ext_dat = file_ext_dat
        self.build_file_db()

    def get_file_from_index(self, file_index):
        return self.file_table[file_index]

    def smart_file_type_finder(self, file_id):
        file_extension = self.file_ext_dat[file_id]

        switcher = {
            0x0: 'out',
            0x1: 'out',
            0x2: 'LESS',
            0x3: 'out',
            0x4: 'out',
            0x5: 'out',
            0x6: 'mdl',
            0x7: 'anm',
            0x8: 'out',
            0x9: 'out',
            0xA: 'out',
            0xB: 'out',
            0xC: 'DXH',
            0xD: 'str',  # Sound effects
            0xE: 'str',  # Voices
            0xF: 'pss'
        }

        return switcher.get(file_extension, "out")

    def GetFile(self, file_index):
        return self.p_cd_dat + file_index * 0xc

    def GetFileSize(self, file_index):
        return self.GetFile(file_index) + 4

    def GetFileCmpSize(self, file_index):
        return self.GetFile(file_index) + 8

    def GetFileSectorSize(self, file_index):
        curr_file_size = self.GetFileSize(file_index)
        return curr_file_size + 0x7ff >> 0xb

    def GetFileStartSector(self, file_index):
        return (self.p_cd_dat + file_index * 0xc) >> 2

    def cddatIsFile(self, file_index):
        file_status = self.cd_dat_tbl[hex(self.GetFile(file_index))] & 0b00000011

        if file_status == 0b00:
            return FileStatus.NO_FILE
        elif file_status == 0b10:
            return FileStatus.FILE_NOT_COMPRESSED
        elif file_status == 0b11:
            return FileStatus.FILE_COMPRESSED

        return FileStatus.UNKNOWN_FILE

    def extract_file(self, file_index):
        """
        For each file:
        * 4 byte - LBA
        * 4 byte - unpack file size
        * 4 byte - file size in archive
        """
        file = self.cd_dat_tbl[hex(self.GetFile(file_index))]

        file_status = self.cddatIsFile(file_index)

        file_size = self.cd_dat_tbl[hex(self.GetFileSize(file_index))]

        file_size_cmp = self.cd_dat_tbl[hex(self.GetFileCmpSize(file_index))]

        file_bd_addr = compute_img_bin_file_address(file)

        file_start_sector = self.GetFileStartSector(file_index)

        if file_status == FileStatus.FILE_COMPRESSED:
            file_end = file_bd_addr + file_size_cmp
        elif file_status == FileStatus.NO_FILE:
            if file_size > file_size_cmp:
                file_end = file_bd_addr + file_size
            else:
                file_end = file_bd_addr + file_size_cmp
        else:
            file_end = file_bd_addr + file_size

        file_extension = self.smart_file_type_finder(file_index)

        return \
            {
                'Id': file_index,
                'CdStartAddr': file,
                'StartSector': file_start_sector,
                'Type': file_status,
                'BinStartAddr': file_bd_addr,
                'BinEndAddr': file_end,
                'Size': file_size,
                'SizeCmp': file_size_cmp,
                'FileExtension': file_extension
            }

    def build_file_db(self):
        files_id = range(0, self.project_file_num)

        for curr_file in files_id:
            self.file_table.append(self.extract_file(curr_file))


if __name__ == '__main__':
    us_file_db = Zero2TOC(project_file_num_, p_cd_dat_us, p_ext_lbl, cd_dat_tbl_us, file_ext_dat_a)
    jp_file_db = Zero2TOC(project_file_num_, p_cd_dat_jp, p_ext_lbl, cd_dat_tbl_jp, file_ext_dat_a)

    for a_file in jp_file_db.file_table:
        print_file_info(a_file)
