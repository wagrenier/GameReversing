import json


def convert_characters(character):
    switcher = {
        0x00: ' ',
        0x01: 'A',
        0x02: 'B',
        0x03: 'C',
        0x04: 'D',
        0x05: 'E',
        0x06: 'F',
        0x07: 'G',
        0x08: 'H',
        0x09: 'I',
        0x0A: 'J',
        0x0B: 'K',
        0x0C: 'L',
        0x0D: 'M',
        0x0E: 'N',
        0x0F: 'O',
        0x10: 'P',
        0x11: 'Q',
        0x12: 'R',
        0x13: 'S',
        0x14: 'T',
        0x15: 'U',
        0x16: 'V',
        0x17: 'W',
        0x18: 'X',
        0x19: 'Y',
        0x1A: 'Z',
        0x1B: 'a',
        0x1C: 'b',
        0x1D: 'c',
        0x1E: 'd',
        0x1F: 'e',
        0x20: 'f',
        0x21: 'g',
        0x22: 'h',
        0x23: 'i',
        0x24: 'j',
        0x25: 'k',
        0x26: 'l',
        0x27: 'm',
        0x28: 'n',
        0x29: 'o',
        0x2A: 'p',
        0x2B: 'q',
        0x2C: 'r',
        0x2D: 's',
        0x2E: 't',
        0x2F: 'u',
        0x30: 'v',
        0x31: 'w',
        0x32: 'x',
        0x33: 'y',
        0x34: 'z',
        0x3F: '0',
        0x40: '1',
        0x41: '2',
        0x42: '3',
        0x43: '4',
        0x44: '5',
        0x45: '6',
        0x46: '7',
        0x47: '8',
        0x48: '9',
        0x5A: ' ',
        0x53: 'è',
        0x54: 'é',
        0x55: 'ê',
        0x56: 'î',
        0x8B: '\'',
        0x8E: '-',
        0x8F: '?',
        0x95: ',',
        0x96: '.',
        0xFE: '\n',
        0xFF: 'FF'  # -> End of string
    }

    return switcher.get(character, 'LL')


def read_string():
    curr_byte = ''

    while 1:
        byte_s = subtitle_file.read(1)
        if not byte_s:
            return -1

        char_to_write = convert_characters(int.from_bytes(byte_s, 'little'))

        if char_to_write == 'LL':
            char_to_write = ' '
        elif char_to_write == 'FF':
            break
        curr_byte = curr_byte + char_to_write

    return curr_byte


if __name__ == '__main__':
    file_id = 'ig_msg_f.obj'
    folder = 'D:/Games/Emulator/XBOX/Games/Project Zero Mod Jap1.1/Media/msg'

    file_db = []

    file_fill_path = f'{folder}/{file_id}'

    subtitle_file = open(file_fill_path, 'rb')

    subtitle_file.seek(0x22724)  # fr=0x22724, en=0x20189

    file_index = 0
    while 1:
        subtitle_text = read_string()
        if subtitle_text == -1:
            break

        file_db.append({
            "Id": file_index,
            "TextId": subtitle_text,
            "Text": subtitle_text
        })

        file_index += 1

    subtitle_file.close()

    out_file = open(f'{folder}/transcribe.json', "w+")
    json.dump(file_db, out_file, indent=6)
