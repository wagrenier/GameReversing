from Zero2TOC import Zero2TOC, create_us_db, create_jp_db

# For now, only import files that are smaller in the japanese dub, and audio files
# Sector 1476500 seems to be containing a fmv
if __name__ == '__main__':
    us_iso = open('D:/DecompressFiles/Fatal Frame 2 Undub/UNDUB/Fatal Frame II - Crimson Butterfly.iso', 'rb+')
    # img_bin_jp = open('D:/DecompressFiles/IMG_BD_JP.BIN', 'rb')

    #jp_file = open('D:/DecompressFiles/Zero2_JP/pss/3280_15.pss', 'rb')
    img_bin_jp = open('D:/DecompressFiles/Fatal Frame 2 Undub/JAPAN/IMG_BD.BIN', 'rb')
    # us_file = open('D:/DecompressFiles/Zero2_US/pss/3280_15.pss', 'rb')

    # Export only those files when the jp is either smaller or same size
    #   0xD: 'str',  # Sound effects
    #   0xE: 'str',  # Voices
    #   0xF: 'pss'

    img_bin_start_address_in_iso_us = 0x30D40000

    us_file_db = create_us_db()
    jp_file_db = create_jp_db()

    for convert_file in jp_file_db.file_table:
        if convert_file['FileExtension'] == 'pss' or convert_file['FileExtension'] == 'str':
            curr_file_id = convert_file['Id']
            if convert_file['Size'] == us_file_db.get_file_from_index(curr_file_id)['Size']:
                print(f'File {curr_file_id} will be undubbed')

                img_bin_jp.seek(convert_file['BinStartAddr'])
                jp_file_buffer = img_bin_jp.read(convert_file['Size'])

                us_iso.seek(us_file_db.get_file_from_index(curr_file_id)['BinStartAddr'] + img_bin_start_address_in_iso_us)
                us_iso.write(jp_file_buffer)

    img_bin_jp.close()
    us_iso.close()
    #file_id_to_replace = 0xCD0
    #file_start_address = 518170624
    #file_size_ = 83623940

    #jp_file_buffer = jp_file.read(file_size_)

    # file_start_iso = img_bin_start_address_in_iso + a_file['BinStartAddr']
    # file_end_iso = img_bin_start_address_in_iso + a_file['BinEndAddr']
    # us_iso.seek(file_start_iso)

    #us_iso.seek(0x4FB6A800)

    #us_iso.write(jp_file_buffer)

    #us_iso.close()
    #jp_file.close()
