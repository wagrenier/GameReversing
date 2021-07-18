import os

from Zero2TOC import Zero2TOC, create_us_db, create_jp_db
from ISOHandler import extract_db_file_from_jp_iso, extract_all_files_from_iso, patch_iml, auto_patch
import struct
import subprocess


# Constants
# toc location 0x1F40B8 in elf
# toc location 0x2F90B8 in iso
elf_toc_offset = 0x1F40B8
img_bin_start_address_in_iso_us = 0x30D40000


def write_file_new_address(us_elf_buffer, file_index, new_address, file_type):
    new_address_to_write = (int(new_address / 0x800) << 2) + file_type
    file_loc = elf_toc_offset + (file_index * 0xc)
    us_elf_buffer.seek(file_loc)
    us_elf_buffer.write(struct.pack('<I', new_address_to_write))


def write_file_new_size(us_elf_buffer, file_index, new_size):
    file_loc = elf_toc_offset + (file_index * 0xc) + 4
    us_elf_buffer.seek(file_loc)
    us_elf_buffer.write(struct.pack('<I', new_size))


def adjust_file_address_to_in_iso(address):
    return address + img_bin_start_address_in_iso_us


def extract_needed_things():
    extract_db_file_from_jp_iso(f'{data_folder}', jp_iso_file_name)
    extract_all_files_from_iso(f'{data_folder}', us_iso_file_name)

    img_bin_us = open(f'{data_folder}/img_bd.bin', 'rb+')
    us_elf = open(f'{data_folder}/slus_207.66', 'rb+')

    img_bin_jp = open(f'{data_folder}/JP/IMG_BD.BIN', 'rb')

    # Export only those files when the jp is either smaller or same size
    #   0xD: 'str',  # Sound effects
    #   0xE: 'str',  # Voices
    #   0xF: 'pss'

    us_file_db = create_us_db()
    jp_file_db = create_jp_db()

    for convert_file in jp_file_db.file_table:
        if convert_file['FileExtension'] == 'pss' or convert_file['FileExtension'] == 'str':
            curr_file_id = convert_file['Id']
            current_us_file = us_file_db.get_file_from_index(curr_file_id)

            if convert_file['Size'] <= current_us_file['Size']:
                print(f'Undubbing file {curr_file_id} of type {convert_file["FileExtension"]}')

                img_bin_jp.seek(convert_file['BinStartAddr'])
                jp_file_buffer = img_bin_jp.read(convert_file['Size'])

                file_start_address_iso = adjust_file_address_to_in_iso(convert_file['BinStartAddr'])

                img_bin_us.seek(file_start_address_iso)
                img_bin_us.write(jp_file_buffer)

                if convert_file['Size'] < current_us_file['Size']:
                    write_file_new_size(us_elf, curr_file_id, convert_file['Size'])

    img_bin_us.close()
    #mg_bin_us = open(f'{data_folder}/img_bd.bin', 'ab+')

    for convert_file in jp_file_db.file_table:
        if convert_file['FileExtension'] == 'pss' or convert_file['FileExtension'] == 'str':
            curr_file_id = convert_file['Id']
            current_us_file = us_file_db.get_file_from_index(curr_file_id)

            if convert_file['Size'] > current_us_file['Size']:
                print(f'Undubbing file {curr_file_id} of type {convert_file["FileExtension"]}')

                #img_bin_jp.seek(convert_file['BinStartAddr'])
                #jp_file_buffer = img_bin_jp.read(convert_file['Size'])

                #current_buffer_address = img_bin_us.tell()
                #img_bin_us.write(jp_file_buffer)

                #empty_bytes = 0x800 - (convert_file['Size'] % 0x800)
                #img_bin_us.write(bytearray(empty_bytes))
                #write_file_new_size(us_elf, curr_file_id, convert_file['Size'])
                #write_file_new_address(us_elf, curr_file_id, current_buffer_address, convert_file['Type'].value)

    img_bin_jp.close()
    #img_bin_us.close()
    us_elf.close()


# For now, only import files that are smaller or equal in the japanese dub, and audio files
if __name__ == '__main__':
    # Extracts required files from the ISOs
    data_folder = 'D:/DecompressFiles/Fatal Frame 2 Undub/full'
    us_iso_file_name = 'ff2_us.iso'
    jp_iso_file_name = 'ff2_jp.iso'

    #extract_needed_things()
    #patch_iml(f'{data_folder}')
    #auto_patch(f'{data_folder}/img_bd.bin', f'{data_folder}/ff2.ims')
    os.chdir(f'{data_folder}')
    subprocess.run([f'iml2iso.exe', f'ff2.iml', f'ff2.iso'])
