# Import statements
from ExtractFilesTOC import *
import subprocess
from pathlib import Path
import glob
import shutil

quickbms_path = '../../../../quickbms/quickbms.exe'
quickbms_script_path = '../../QuickBmsScripts'

uncompressed_folder_path = '/uncompressed'
extraction_folder_path = 'D:/DecompressFiles/Zero2_TOC_Extract'


def check_file_type(line_header, is_large_header=False):
    # Add line by line read to check file type
    if not is_large_header and line_header.find(b'TIM2') >= 0:
        return 'tm2'
    elif is_large_header and line_header.find(b'MOTN') >= 0:
        return 'anm'
    elif not is_large_header and line_header.find(b'DXH') >= 0:
        return 'DXH'
    elif not is_large_header and line_header.find(b'LESS') >= 0:
        return 'LESS'
    elif is_large_header and line_header.find(b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') >= 0:
        return 'mdl'
    elif not is_large_header and (line_header.find(b'\x00\x00\x01\xBA\x44') >= 0 or line_header.find(b'\x6D\xC4\x3B\x4A') >= 0):
        return 'pss'
    elif not is_large_header and line_header.find(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') >= 0:
        return 'str'
    elif not is_large_header and line_header.find(b'\x3F\x63\x3F\x75') >= 0:
        # 3F 63 3F 75 3F 87 3F 99 3F AB 3F BD 3F CF 3F 00
        return 'weirdheader'
    else:
        return 'out'


def extract_file_output(file_to_extract):
    read_size = file_to_extract['BinEndAddr'] - file_to_extract['BinStartAddr']

    if read_size <= 0:
        return

    img_bin.seek(file_to_extract['BinStartAddr'])

    file_type = check_file_type(img_bin.read(0x10))

    img_bin.seek(file_to_extract['BinStartAddr'])

    full_buffer = img_bin.read(read_size)

    Path(f'{extraction_folder_path}/{file_type}').mkdir(parents=True, exist_ok=True)
    file_full_name = f'{extraction_folder_path}/{file_type}/{file_to_extract["Id"]}.{file_type}'
    output_file = open(file_full_name, 'wb')

    output_file.write(full_buffer)
    output_file.close()


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

        Path(f'{extraction_folder_path}/{file_type}').mkdir(parents=True, exist_ok=True)
        target_path_and_name = f'{extraction_folder_path}/{file_type}/{Path(file).name}_DECOMPRESSED.{file_type}'

        shutil.move(file, target_path_and_name)


def decompress_files():
    # Command to list the TOC files included within the ELF
    # .\quickbms -l "D:\Programming\Git\Github\GameReversing\PS2\Fatal Frame 2\QuickBmsScripts\project_zero.bms" "D:\Reverse\Fatal Frame II\Files\SLUS_207.66" "D:\DecompressFiles\bms\output"

    # Uncompressed files folder
    print('Decompress archived files...')
    Path(f'{extraction_folder_path}{uncompressed_folder_path}').mkdir(parents=True, exist_ok=True)
    subprocess.run([quickbms_path, "-.", "-F", "{}.LESS", f'{quickbms_script_path}/deless.bms',
                    f'{extraction_folder_path}/LESS', f'{extraction_folder_path}{uncompressed_folder_path}'])

    # tim2 extraction from unarchived files
    print('Extracting tim2 files from archived files...')
    Path(f'{extraction_folder_path}/tm2').mkdir(parents=True, exist_ok=True)
    subprocess.run([quickbms_path, "-.", "-F", "{}.LED", f'{quickbms_script_path}/tim2.bms',
                    f'{extraction_folder_path}{uncompressed_folder_path}',
                    f'{extraction_folder_path}/tm2'])

    # tim2 extraction from archived files
    print('Extracting tim2 files from uncompressed...')
    Path(f'{extraction_folder_path}/tm2/raw').mkdir(parents=True, exist_ok=True)
    subprocess.run([quickbms_path, "-.", "-F", "{}.out", f'{quickbms_script_path}/tim2.bms',
                    f'{extraction_folder_path}/out',
                    f'{extraction_folder_path}/tm2/raw'])


if __name__ == '__main__':
    print('Building file database...')
    file_list = build_file_db()

    img_bin = open('D:/DecompressFiles/IMG_BD_US.BIN', 'rb')

    print('Extracting files...')
    for file_extract in file_list:
        extract_file_output(file_extract)

    decompress_files()
    move_decompressed_files()
