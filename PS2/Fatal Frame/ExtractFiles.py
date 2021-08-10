import struct

from StandardFileOperations.PathOperations import write_buffer_to_file


def find_file_type(buff):
    if buff.find(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') >= 0:
        return 'str'

    buf_size = len(buff)
    x = 0
    while x < buf_size:
        if x == 1 and buff[x] != 0:
            x += 1
            continue
        elif buff[x] != 0:
            return 'out'
        x += 1

    return 'str'


img_hd = 'IMG_HD.BIN'
img_bd = 'IMG_BD.BIN'

# USA = 0x769, JP = 0x73A, EU = 0x879
num_file = 0x743

folder = 'D:/DecompressFiles/Fatal Frame Undub/Demo'

img_hd_file = open(f'{folder}/{img_hd}', 'rb')
img_bd_file = open(f'{folder}/{img_bd}', 'rb')

file_id = 0

audio_start_index_us = 1350
audio_start_index_jp = 1303

file_start_address_find = 0x278FD0

while file_id < num_file:
    file_lba = int.from_bytes(img_hd_file.read(0x4), byteorder='little', signed=False)
    file_size = int.from_bytes(img_hd_file.read(0x4), byteorder='little', signed=False)
    file_start_address = file_lba * 0x800
    #file_end_address = file_start_address + file_size

    #print(f'File ID: {file_id}, File LBA: {file_lba}, File Size: {file_size}, File Start: {file_start_address}, File End: {file_end_address}')
    img_bd_file.seek(file_start_address)
    header_buffer = img_bd_file.read(0xF)

    img_bd_file.seek(file_start_address)
    full_buffer = img_bd_file.read(file_size)

    extension = find_file_type(header_buffer)

    write_buffer_to_file(full_buffer, f'{folder}/extract', f'{file_id}.{extension}')

    file_id += 1

img_hd_file.close()
img_bd_file.close()



