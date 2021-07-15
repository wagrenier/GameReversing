# Import statements
from ExtractFilesTOC import *
from pathlib import Path
import glob
from StandardFileOperations.PathOperations import move_and_rename_file, write_buffer_to_file
from quickbms.quickbms_handler import *

# Global variables
img_bin_file_path = 'D:/DecompressFiles/IMG_BD_US.BIN'

extraction_folder_path = 'D:/DecompressFiles/Zero2_US'
uncompressed_folder_path = '/uncompressed'


def check_file_type(line_header, is_large_header=False):
    # Add line by line read to check file type
    if not is_large_header and line_header.find(b'TIM2') >= 0:
        return 'tm2'
    elif not is_large_header and line_header.find(b'PK4') >= 0:
        return 'pk4'
    elif not is_large_header and line_header.find(b'phf') >= 0:
        return 'phf'
    elif is_large_header and line_header.find(b'MOTN') >= 0:
        return 'anm'
    elif not is_large_header and line_header.find(b'DXH') >= 0:
        return 'DXH'
    elif not is_large_header and line_header.find(b'LESS') >= 0:
        return 'LESS'
    elif is_large_header and line_header.find(b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') >= 0:
        return 'mdl'
    elif not is_large_header and (
            line_header.find(b'\x00\x00\x01\xBA\x44') >= 0 or line_header.find(b'\x6D\xC4\x3B\x4A') >= 0):
        return 'pss'
    elif not is_large_header and line_header.find(
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') >= 0:
        return 'str'
    else:
        return 'out'


def smart_file_type_finder(file_id):
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

    return switcher.get(file_id, "out")


def extract_file_output(file_to_extract, img_bin):
    read_size = file_to_extract['BinEndAddr'] - file_to_extract['BinStartAddr']

    if read_size <= 0:
        return

    img_bin.seek(file_to_extract['BinStartAddr'])

    file_type = check_file_type(img_bin.read(0x10))
    # file_type = smart_file_type_finder(file_ext_dat[file_to_extract["Id"]])

    img_bin.seek(file_to_extract['BinStartAddr'])

    full_buffer = img_bin.read(read_size)

    write_buffer_to_file(full_buffer, f'{extraction_folder_path}/{file_type}',
                         f'{file_to_extract["Id"]}_{file_ext_dat[file_to_extract["Id"]]}.{file_type}')


def move_decompressed_files():
    # mdl, motn extraction from archived files
    print('Moving decompressed files to their folders...')
    for file in glob.glob(f'{extraction_folder_path}{uncompressed_folder_path}/*.LED'):
        uncompressed_file = open(file, 'rb')
        file_type = check_file_type(uncompressed_file.read(0x50), True)
        uncompressed_file.close()

        if file_type == 'out':
            # Do not move the file if it is unknown
            continue

        recursive_create_folder(f'{extraction_folder_path}/{file_type}')
        target_path_and_name = f'{extraction_folder_path}/{file_type}/{Path(file).name}_DECOMPRESSED.{file_type}'

        move_and_rename_file(file, target_path_and_name)


def decompress_files():
    # Uncompressed files folder
    print('Decompress archived files...')
    launch_quickbms_script(deless_script, f'{extraction_folder_path}/LESS',
                           f'{extraction_folder_path}{uncompressed_folder_path}', 'LESS', '{}')

    # tim2 extraction from unarchived files
    print('Extracting tim2 files from archived files...')
    launch_quickbms_script(tim2_script, f'{extraction_folder_path}{uncompressed_folder_path}',
                           f'{extraction_folder_path}/tm2', 'LED', '{}')

    # tim2 extraction from unarchived files
    print('Extracting tim2 files from archived files...')
    launch_quickbms_script(tim2_script, f'{extraction_folder_path}/LESS',
                           f'{extraction_folder_path}/tm2/LESS', 'LESS', '{}')

    # tim2 extraction from archived files
    print('Extracting tim2 files from uncompressed...')
    launch_quickbms_script(tim2_script, f'{extraction_folder_path}/out',
                           f'{extraction_folder_path}/tm2/raw', 'out', '{}')


def run():
    print('Building file database...')
    file_list = build_file_db()

    print('Opening IMG_BIN file...')
    img_bin = open(img_bin_file_path, 'rb')

    print('Extracting files...')
    file_list_size = len(file_list)
    current_file_index = 0

    for file_extract in file_list:
        print(f'Extracting file {current_file_index} out of {file_list_size}')
        extract_file_output(file_extract, img_bin)
        current_file_index += 1

    img_bin.close()

    decompress_files()
    move_decompressed_files()


if __name__ == '__main__':
    run()
