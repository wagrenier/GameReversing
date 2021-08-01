import struct
import glob

img_hd = 'IMG_HD.BIN'
img_bd = 'IMG_BD.BIN'

# USA = 0x769, JP = 0x73A, EU = 0x879
num_file = 0x879

folder_jp = 'D:/DecompressFiles/Fatal Frame Undub/Japan'
folder_us = 'D:/DecompressFiles/Fatal Frame Undub/EUROPE'

iso_img_hd_bin_start_address = 0xA63000    # 0x20836000
iso_img_bd_bin_start_address = 0x384A7800  # 0x2083A000

img_iso_us = open(f'{folder_us}/ffeu.iso', 'rb+')

img_hd_file_us = open(f'{folder_us}/{img_hd}', 'rb')

img_hd_file_jp = open(f'{folder_jp}/{img_hd}', 'rb')
img_bd_file_jp = open(f'{folder_jp}/{img_bd}', 'rb')

file_id = 0

audio_start_index_us = 1622
audio_start_index_jp = 1303

audio_delta = audio_start_index_us - audio_start_index_jp

while file_id < num_file:
    if file_id == 1062:
        file_id_jp = 743
    elif file_id == 1063:
        file_id_jp = 744
    elif file_id == 1064:
        file_id_jp = 745
    elif file_id == 1065:
        file_id_jp = 746
    elif file_id == 1066:
        file_id_jp = 747
    elif file_id == 1067:
        file_id_jp = 748
    elif file_id < audio_start_index_us or file_id == num_file - 1:
        file_id += 1
        continue
    else:
        file_id_jp = file_id - audio_delta

    img_hd_file_us.seek(file_id * 0x8)
    file_lba_us = int.from_bytes(img_hd_file_us.read(0x4), byteorder='little', signed=False)
    file_size_us = int.from_bytes(img_hd_file_us.read(0x4), byteorder='little', signed=False)
    file_start_address_us = file_lba_us * 0x800

    img_hd_file_jp.seek(file_id_jp * 0x8)
    file_lba_jp = int.from_bytes(img_hd_file_jp.read(0x4), byteorder='little', signed=False)
    file_size_jp = int.from_bytes(img_hd_file_jp.read(0x4), byteorder='little', signed=False)
    file_start_address_jp = file_lba_jp * 0x800

    if file_size_us < file_size_jp:
        print(f'File {file_id} is too big')
        file_id += 1
        continue

    print(f'Undubbing file {file_id}')
    img_bd_file_jp.seek(file_start_address_jp)
    buffer = img_bd_file_jp.read(file_size_jp)
    img_iso_us.seek(iso_img_bd_bin_start_address + file_start_address_us)
    img_iso_us.write(buffer)

    if file_size_us > file_size_jp:
        img_iso_us.seek(iso_img_hd_bin_start_address + (8 * file_id) + 4)
        img_iso_us.write(struct.pack('<I', file_size_jp))

    file_id += 1

img_hd_file_us.close()
img_iso_us.close()

img_hd_file_jp.close()
img_bd_file_jp.close()
