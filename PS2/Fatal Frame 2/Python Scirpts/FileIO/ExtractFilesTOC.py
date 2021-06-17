# Import statements
from FileHandlers import *


def PrintFileInfo(file):
    if DEBUG:
        file_debug_string = 'FileID:{},FileStatus:{},StartAddrLBA:{},FileEndLBA:{},FileSize:{},FileSizeCmp:{}\n'.format\
                (
                    hex(file['FileID']), file['FileStatus'], hex(file['FileBDAddr']), hex(file['FileBDEndAddr']),
                    hex(file['FileSize']), hex(file['FileSizeCmp'])
                )

        print(file_debug_string)
        debug_output.write(file_debug_string)


def GetFileEndAddress(file_start_addr, file_size):
    print(file_start_addr + file_size)


"""
For each file:
* 4 byte - LBA
* 4 byte - unpack file size
* 4 byte - file size in archive
"""


def ExtractFile(file_index):
    file = cd_dat_tbl[hex(GetFile(file_index))]
    file_status = cddatIsFile(file_index)
    file_size = cd_dat_tbl[hex(GetFileSize(file_index))]
    file_size_cmp = cd_dat_tbl[hex(GetFileCmpSize(file_index))]
    file_bd_addr = Compute_IMG_BIN_File_Address(file)
    file_end = file_bd_addr + file_size_cmp

    return \
        {
            'FileID': file_index,
            'File': file,
            'FileStatus': file_status,
            'FileBDAddr': file_bd_addr,
            'FileBDEndAddr': file_end,
            'FileSize': file_size,
            'FileSizeCmp': file_size_cmp
        }


def extract_addr(json_element):
    try:
        return json_element['FileID']
    except KeyError:
        return 0


def BuildFileDb():
    files_id = range(0, project_file_num - 1)
    file_db = []

    for curr_file in files_id:
        extracted_file = ExtractFile(curr_file)

        file_db.append(extracted_file)

    file_db.sort(key=extract_addr)

    for my_file in file_db:
        PrintFileInfo(my_file)


def Compute_IMG_BIN_File_Address(file):
    file_lba = (file >> 2) * sector_size
    return file_lba


if __name__ == '__main__':
    BuildFileDb()
