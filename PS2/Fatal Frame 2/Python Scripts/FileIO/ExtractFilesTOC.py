# Import statements
from FileHandlers import *


def print_file_info(file):
    if DEBUG:
        file_debug_string = 'Id:{},Type:{},StartSector:{},StartAddrLBA:{},FileEndLBA:{},Size:{},SizeCmp:{}\n'.format \
                (
                hex(file['Id']), file['Type'], hex(file['StartSector']), hex(file['BinStartAddr']),
                hex(file['BinEndAddr']),
                hex(file['Size']), hex(file['SizeCmp'])
            )

        print(file_debug_string)
        debug_output.write(file_debug_string)


def extract_file(file_index):
    """
    For each file:
    * 4 byte - LBA
    * 4 byte - unpack file size
    * 4 byte - file size in archive
    """
    file = cd_dat_tbl[hex(GetFile(file_index))]

    file_status = cddatIsFile(file_index)

    file_size = cd_dat_tbl[hex(GetFileSize(file_index))]

    file_size_cmp = cd_dat_tbl[hex(GetFileCmpSize(file_index))]

    file_bd_addr = compute_img_bin_file_address(file)

    file_start_sector = GetFileStartSector(file_index)

    if file_status == FileStatus.FILE_COMPRESSED:
        file_end = file_bd_addr + file_size_cmp
    elif file_status == FileStatus.NO_FILE:
        if file_size > file_size_cmp:
            file_end = file_bd_addr + file_size
        else:
            file_end = file_bd_addr + file_size_cmp
    else:
        file_end = file_bd_addr + file_size

    return \
        {
            'Id': file_index,
            'CdStartAddr': file,
            'StartSector': file_start_sector,
            'Type': file_status,
            'BinStartAddr': file_bd_addr,
            'BinEndAddr': file_end,
            'Size': file_size,
            'SizeCmp': file_size_cmp
        }


def build_file_db():
    files_id = range(0, project_file_num)
    file_db = []

    for curr_file in files_id:
        file_db.append(extract_file(curr_file))

    return file_db


def compute_img_bin_file_address(file):
    # Computes the lba for the file, rather than the address within the ISO
    return (file >> 2) * sector_size


if __name__ == '__main__':
    #extract_file(0x1064)
    a = extract_file(0xCD0)
    # build_file_db()
