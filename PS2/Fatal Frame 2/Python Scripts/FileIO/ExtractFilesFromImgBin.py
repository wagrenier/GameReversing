# Import statements
from ExtractFilesTOC import *


def check_file_type(line_header):
    if line_header.find(b'TIM2') >= 0:
        return 'tm2'
    if line_header.find(b'DXH') >= 0:
        return 'DXH'
    elif line_header.find(b'LESS') >= 0:
        return 'LESS'
    elif line_header.find(b'\x00\x00\x01\xBA\x44') >= 0 or line_header.find(b'\x6D\xC4\x3B\x4A') >= 0:
        return 'pss'
    elif line_header.find(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') >= 0:
        return 'str'
    elif line_header.find(b'\x3F\x63\x3F\x75') >= 0:
        # 3F 63 3F 75 3F 87 3F 99 3F AB 3F BD 3F CF 3F 00
        return 'weirdheader'
    else:
        return 'out'


if __name__ == '__main__':
    file_list = build_file_db()

    img_bin = open('D:/DecompressFiles/IMG_BD_US.BIN', 'rb')

    for file_extract in file_list:
        read_size = file_extract['BinEndAddr'] - file_extract['BinStartAddr']

        if read_size <= 0:
            continue

        img_bin.seek(file_extract['BinStartAddr'])

        file_type = check_file_type(img_bin.read(0x10))

        img_bin.seek(file_extract['BinStartAddr'])

        full_buffer = img_bin.read(read_size)

        file_full_name = f'D:/DecompressFiles/PythonExtract/{file_extract["Id"]}.{file_type}'
        output_file = open(file_full_name, 'wb')

        output_file.write(full_buffer)
        output_file.close()

        #.\quickbms -. -F "{}.LESS" scripts/deless.bms D:\DecompressFiles\PythonExtract D:\DecompressFiles\PythonExtract\compressed
        #.\quickbms -l "D:\Programming\Git\Github\GameReversing\PS2\Fatal Frame 2\QuickBmsScripts\project_zero.bms" "D:\Reverse\Fatal Frame II\Files\SLUS_207.66" "D:\DecompressFiles\bms\output"
