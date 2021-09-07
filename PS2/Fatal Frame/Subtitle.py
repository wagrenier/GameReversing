import os

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
        0x49: 'ア',
        0x4A: 'イ',
        0x4B: 'ウ',
        0x4C: 'エ',
        0x4D: 'オ',
        0x4E: 'カ',
        0x4F: 'キ',
        0x50: 'ク',
        0x51: 'ケ',
        0x52: 'コ',
        0x53: 'サ',
        0x54: 'シ',
        0x55: 'ス',
        0x56: 'せ',
        0x57: 'ソ',
        0x58: 'タ',
        0x59: 'チ',
        0x5A: 'ツ',
        0x5B: 'テ',
        0x5C: 'ト',
        0x5D: 'ナ',
        0x5E: '二',
        0x5F: 'ヌ',
        0x60: 'ネ',
        0x61: 'ノ',
        0x62: 'ハ',
        0x63: 'ヒ',
        0x63: 'フ',
        0x64: 'ヘ',
        0x65: 'ホ',
        0x66: 'マ',
        0x67: 'ミ',
        0x68: 'ム',
        0x69: 'メ',
        0x6A: 'モ',
        0x6B: 'ヤ',
        0x6C: 'ユ',
        0x6D: 'ヨ',
        0x6E: 'ラ',
        0x6F: 'リ',
        0x70: 'ル',
        0x71: 'レ',
        0x72: 'ロ',
        0x73: 'ワ',
        0x74: 'ヲ',
        0x75: 'ン',
        0x76: 'ァ',
        0x77: 'ル',
        0x78: 'ル',
        0x79: 'ル',
        0x7A: 'ル',
        0x7B: 'ル',
        0x7C: 'ル',
        0x7D: 'ル',
        0x7E: 'ル',
        0x7F: 'ル',

        0x8B: '\'',
        0x8E: '-',
        0x8F: '?',
        0x95: ',',
        0x96: '.',
        0xFE: '\n',
        0xFF: '\n'  # -> End of string
    }

    return switcher.get(character, '!')


if __name__ == '__main__':
    file_name = 20 #'ig_msg_' # 40
    sub = ['en', 'fr', 'de', 'es', 'it']
    folder = 'D:/DecompressFiles/Fatal Frame Undub/Japan/extract' # 'D:/DecompressFiles/Fatal Frame Undub/EUROPE/extract' 'D:/Games/Emulator/XBOX/Games/Project Zero Mod Jap1.1/Media/msg'

    files = [f'{file_name}'] #['e', 'f', 'g', 'i', 'j', 's']

    for file in files:
        curr_file = f'{file_name}'
        file_fill_path = f'{folder}/{curr_file}.out'

        file_size = os.stat(file_fill_path).st_size

        subtitle_file = open(file_fill_path, 'rb')
        subtitle_file_extract = open(f'{folder}/subtitles_{file}.bin', 'w+', encoding='utf8')
        a = 0

        while a < file_size:
            byte_s = subtitle_file.read(1)
            a += 1
            char_to_write = convert_characters(int.from_bytes(byte_s, "little"))

            subtitle_file_extract.write(char_to_write)

        subtitle_file.close()
        subtitle_file_extract.close()
