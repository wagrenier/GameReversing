# Import statements
from FileHandlers import *


def PrintFileInfo(file):
    if DEBUG:
        file_debug_string = 'Id:{},Type:{},StartSector:{},StartAddrLBA:{},FileEndLBA:{},Size:{},SizeCmp:{}\n'.format \
                (
                hex(file['Id']), file['Type'], hex(file['StartSector']), hex(file['BinStartAddr']),
                hex(file['BinEndAddr']),
                hex(file['Size']), hex(file['SizeCmp'])
            )

        print(file_debug_string)
        debug_output.write(file_debug_string)


"""
For each file:
* 4 byte - LBA
* 4 byte - unpack file size
* 4 byte - file size in archive
"""


def extract_file(file_index):
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
            'CanExtract': True,
            'BinStartAddr': file_bd_addr,
            'BinEndAddr': file_end,
            'Size': file_size,
            'SizeCmp': file_size_cmp
        }


def remove_empty_files(file_list):
    return list(filter(lambda x: x['Type'] != FileStatus.NO_FILE, file_list))


def combine_duplicate_file(file_list):
    combined_file_list = []

    for file in file_list:
        if len(list(
                filter(lambda x: x['BinStartAddr'] == file['BinStartAddr'], combined_file_list))) > 0:
            continue

        files_to_combine = list(filter(
            lambda x: x['BinStartAddr'] == file['BinStartAddr'] and x['Id'] != file['Id'] and x['Id'] > file['Id'],
            file_list))

        if len(files_to_combine) > 0:
            for file_not_extract in files_to_combine:
                file_not_extract['CanExtract'] = False

            filtered_list = files_to_combine
            files_to_combine.append(file)
            true_file_end = file

            while len(filtered_list) > 0:
                filtered_list = list(filter(lambda x: x['BinEndAddr'] > true_file_end['BinEndAddr'], filtered_list))

                if len(filtered_list) == 0:
                    break
                else:
                    true_file_end = filtered_list[0]

            true_file_end['CanExtract'] = True
            combined_file_list.append(true_file_end)

    return combined_file_list


def build_file_db():
    files_id = range(0, project_file_num)
    file_db = []

    for curr_file in files_id:
        file_db.append(extract_file(curr_file))

    filtered_file_db = remove_empty_files(file_db)
    combined_files = combine_duplicate_file(file_db)

#or len(list(filter(lambda x: x['BinStartAddr'] >= file['BinStartAddr'] and x['BinEndAddr'] <= file['BinEndAddr'],file_db))) > 0

    for file in file_db:
        if file['CanExtract'] == False:
            continue

        combined_files.append(file)

    for file in combined_files:
        PrintFileInfo(file)

    return combined_files


def compute_img_bin_file_address(file):
    # Computes the lba for the file, rather than the address within the ISO
    return (file >> 2) * sector_size


if __name__ == '__main__':
    build_file_db()
