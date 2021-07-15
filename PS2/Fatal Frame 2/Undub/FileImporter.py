# Import statement
# For now, only import files that are smaller in the japanese dub, and audio files

if __name__ == '__main__':
    img_bin_us = open('D:/DecompressFiles/Fatal Frame 2 Undub/UNDUB/Fatal Frame II - Crimson Butterfly.iso', 'rb+')
    #img_bin_jp = open('D:/DecompressFiles/IMG_BD_JP.BIN', 'rb')

    jp_file = open('D:/DecompressFiles/Zero2_JP/pss/3280_15.pss', 'rb')
    #us_file = open('D:/DecompressFiles/Zero2_US/pss/3280_15.pss', 'rb')

    file_size = 83623940

    jp_file_buffer = jp_file.read(file_size)

    file_id_to_replace = 0xCD0

    file_start_address = 518170624

    img_bin_us.seek(0x4FB6A800)

    img_bin_us.write(jp_file_buffer)

    img_bin_us.close()
    jp_file.close()
