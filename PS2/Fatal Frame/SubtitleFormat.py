import json

file_id = 40
subtitle_index_offset = 0x1EA13
iso_name = 'ffeu.iso'
folder = 'D:/DecompressFiles/Fatal Frame Undub/EUROPE'
iso_img_hd_bin_start_address = 0xA63000    # 0x20836000
iso_img_bd_bin_start_address = 0x384A7800


def convert_characters(character):
    switcher = {
        0x00: b' ',
        0x01: b'A',
        0x02: b'B',
        0x03: b'C',
        0x04: b'D',
        0x05: b'E',
        0x06: b'F',
        0x07: b'G',
        0x08: b'H',
        0x09: b'I',
        0x0A: b'J',
        0x0B: b'K',
        0x0C: b'L',
        0x0D: b'M',
        0x0E: b'N',
        0x0F: b'O',
        0x10: b'P',
        0x11: b'Q',
        0x12: b'R',
        0x13: b'S',
        0x14: b'T',
        0x15: b'U',
        0x16: b'V',
        0x17: b'W',
        0x18: b'X',
        0x19: b'Y',
        0x1A: b'Z',
        0x1B: b'a',
        0x1C: b'b',
        0x1D: b'c',
        0x1E: b'd',
        0x1F: b'e',
        0x20: b'f',
        0x21: b'g',
        0x22: b'h',
        0x23: b'i',
        0x24: b'j',
        0x25: b'k',
        0x26: b'l',
        0x27: b'm',
        0x28: b'n',
        0x29: b'o',
        0x2A: b'p',
        0x2B: b'q',
        0x2C: b'r',
        0x2D: b's',
        0x2E: b't',
        0x2F: b'u',
        0x30: b'v',
        0x31: b'w',
        0x32: b'x',
        0x33: b'y',
        0x34: b'z',
        0x3F: b'0',
        0x40: b'1',
        0x41: b'2',
        0x42: b'3',
        0x43: b'4',
        0x44: b'5',
        0x45: b'6',
        0x46: b'7',
        0x47: b'8',
        0x48: b'9',
        # 0x53: b'è',
        # 0x54: b'é',
        # 0x55: b'ê',
        # 0x56: b'î',
        0x8B: b'\'',
        0x8E: b'-',
        0x8F: b'?',
        0x95: b',',
        0x96: b'.',
        0xFE: b'\n',
        0xFF: b'FF'  # -> End of string
    }

    return switcher.get(character, b'LL')


def seek_file(fileId, file_offset):
    iso_file.seek(iso_img_hd_bin_start_address + (fileId * 0x8))
    file_start_address_us = int.from_bytes(iso_file.read(0x4), byteorder='little', signed=False) * 0x800
    iso_file.seek(iso_img_bd_bin_start_address + file_start_address_us + file_offset)


def read_string(fileId, file_offset):
    seek_file(fileId, file_offset)
    curr_byte = b''

    while 1:
        byte_s = iso_file.read(1)
        if not byte_s:
            break

        char_to_write = convert_characters(int.from_bytes(byte_s, "little"))

        if char_to_write == b'LL':
            char_to_write = byte_s
        elif char_to_write == b'FF':
            break
        curr_byte = curr_byte + char_to_write

    return curr_byte


def get_subtitle_start_offset():
    curr_pos = iso_file.tell()
    seek_file(file_id, 0x0)

    return curr_pos - iso_file.tell()


if __name__ == '__main__':
    iso_file = open(f'{folder}/{iso_name}', 'rb')

    file_db = []

    for file_index in range(0, 225):

        seek_file(file_id, subtitle_index_offset + (file_index * 0x4))

        offset = int.from_bytes(iso_file.read(0x4), byteorder='little', signed=False)
        string_read = read_string(file_id, offset)
        nex_offset = get_subtitle_start_offset()
        print(f'ID: {file_index}, {string_read}, curr off: {offset}, next off: {nex_offset}')

        file = {
            'Id': file_index,
            'TextId': string_read.decode('utf-8'),
            'Text': ''
        }

        file_db.append(file)

    print(file_db)

    f = open('transcribe.json', 'w')
    json.dump(file_db, f, indent=6)

    f.close()
    iso_file.close()
