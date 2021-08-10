import json
import struct

transcribe_real = {}

iso_name = 'ffeu.iso'

# Be sure to insert the name with forward slash '/' and not backward slash '\'
folder = 'PUT IN HERE THE FOLDER THAT CONTAINS THE ISO'

file_subtitle = 40

subtitle_index_offset = 0x1EA13 # 0x1EA13, 0x20B95
subtitle_text_offset = 0x1ED97 #0x1ED97, 0x20FD1
subtitle_overall_offset = 0x0
iso_img_hd_bin_start_address = 0xA63000    # 0x20836000
iso_img_bd_bin_start_address = 0x384A7800

with open(f'{folder}/transcribe_real.json') as f:
    transcribe_real = json.load(f)


def convert_char_to_font(char):
    switcher = {
        ord(' '): b'\x00',
        ord('A'): b'\x01',
        ord('B'): b'\x02',
        ord('C'): b'\x03',
        ord('D'): b'\x04',
        ord('E'): b'\x05',
        ord('F'): b'\x06',
        ord('G'): b'\x07',
        ord('H'): b'\x08',
        ord('I'): b'\x09',
        ord('J'): b'\x0A',
        ord('K'): b'\x0B',
        ord('L'): b'\x0C',
        ord('M'): b'\x0D',
        ord('N'): b'\x0E',
        ord('O'): b'\x0F',
        ord('P'): b'\x10',
        ord('Q'): b'\x11',
        ord('R'): b'\x12',
        ord('S'): b'\x13',
        ord('T'): b'\x14',
        ord('U'): b'\x15',
        ord('V'): b'\x16',
        ord('W'): b'\x17',
        ord('X'): b'\x18',
        ord('Y'): b'\x19',
        ord('Z'): b'\x1A',
        ord('a'): b'\x1B',
        ord('b'): b'\x1C',
        ord('c'): b'\x1D',
        ord('d'): b'\x1E',
        ord('e'): b'\x1F',
        ord('f'): b'\x20',
        ord('g'): b'\x21',
        ord('h'): b'\x22',
        ord('i'): b'\x23',
        ord('j'): b'\x24',
        ord('k'): b'\x25',
        ord('l'): b'\x26',
        ord('m'): b'\x27',
        ord('n'): b'\x28',
        ord('o'): b'\x29',
        ord('p'): b'\x2A',
        ord('q'): b'\x2B',
        ord('r'): b'\x2C',
        ord('s'): b'\x2D',
        ord('t'): b'\x2E',
        ord('u'): b'\x2F',
        ord('v'): b'\x30',
        ord('w'): b'\x31',
        ord('x'): b'\x32',
        ord('y'): b'\x33',
        ord('z'): b'\x34',
        ord('0'): b'\x3F',
        ord('1'): b'\x40',
        ord('2'): b'\x41',
        ord('3'): b'\x42',
        ord('4'): b'\x43',
        ord('5'): b'\x44',
        ord('6'): b'\x45',
        ord('7'): b'\x46',
        ord('8'): b'\x47',
        ord('9'): b'\x48',
        ord('\''): b'\x8B',
        ord('-'): b'\x8E',
        ord('?'): b'\x8F',
        ord(','): b'\x95',
        ord('.'): b'\x96',
        ord('\n'): b'\xFE'
    }

    return switcher.get(ord(char), b'')


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


def insert_newline(string, index):
    return string[:index] + '\n' + string[index:]


def line_split_string(subtitle):
    str_len = len(subtitle)

    if str_len < 25:
        return subtitle

    newline_insert_index = subtitle.find(' ', 25)

    if newline_insert_index < 0:
        return subtitle

    return insert_newline(subtitle, newline_insert_index)


def write_string(subtitle_id, string_byte):
    seek_subtitle_text(subtitle_id)
    curr_byte = b''
    overall_offset = 0x0

    string_byte = line_split_string(string_byte)

    for curr_byte in string_byte:
        write_char = convert_char_to_font(curr_byte)
        iso_file.write(write_char)
        overall_offset += 1

    iso_file.write(b'\xFF')
    overall_offset += 1

    return overall_offset


def seek_file(file_id, file_offset):
    iso_file.seek(iso_img_hd_bin_start_address + (file_id * 0x8))
    file_start_address_us = int.from_bytes(iso_file.read(0x4), byteorder='little', signed=False) * 0x800
    iso_file.seek(iso_img_bd_bin_start_address + file_start_address_us + file_offset)


def seek_subtitle_address_index(subtitle_id):
    seek_file(file_subtitle, subtitle_id * 0x4 + subtitle_index_offset)


def read_subtitle_address_index(subtitle_id):
    seek_subtitle_address_index(subtitle_id)
    return int.from_bytes(iso_file.read(0x4), byteorder="little", signed=False)


def seek_subtitle_text(subtitle_id):
    seek_file(file_subtitle, subtitle_text_offset + subtitle_overall_offset)


def read_string(subtitle_id):
    seek_subtitle_text(subtitle_id)
    curr_byte = b''

    aaa = 0

    while 1:
        byte_s = iso_file.read(1)
        if not byte_s:
            break
        aaa += 1
        char_to_write = convert_characters(int.from_bytes(byte_s, 'little'))

        if char_to_write == b'LL':
            char_to_write = byte_s
        elif char_to_write == b'FF':
            break
        curr_byte = curr_byte + char_to_write

    return [curr_byte, aaa]


def write_subtitle_file_address(subtitle_id, address):
    seek_subtitle_address_index(subtitle_id)
    iso_file.write(struct.pack('<I', address))


def patch_subtitles():
    iso_file.seek(0x257313)
    iso_file.write(b'\x10')
    iso_file.seek(0x25711B)
    iso_file.write(b'\x14')
    iso_file.seek(0x257153)
    iso_file.write(b'\x14')
    iso_file.seek(0x261BB3)
    iso_file.write(b'\x14')


if __name__ == '__main__':
    iso_file = open(f'{folder}/{iso_name}', 'rb+')
    patch_subtitles()

    file_db = []

    for file_index in range(0, 271):
        if file_index < 271:
            text_inject = transcribe_real[file_index]['Text']
            write_subtitle_file_address(file_index, subtitle_overall_offset + subtitle_text_offset)
            initial_offset = read_subtitle_address_index(file_index)
            subtitle_text, string_offset_read = read_string(file_index)
            string_offset = write_string(file_index, text_inject)
            subtitle_overall_offset += string_offset
            subtitle_text = subtitle_text.decode("utf-8")
        else:
            subtitle_text = f'SUBTITLE-ID-{file_index}'

        #file_db.append({
        #    "Id": file_index,
        #    "TextId": subtitle_text,
        #    "Text": subtitle_text
        #})
        #print(f'Subtitle Id: {file_index}, Offset: {hex(initial_offset)}, Text Read: {subtitle_text}')

    iso_file.close()
    #out_file = open(f'{folder}/transcribe.json', "w+")
    #json.dump(file_db, out_file, indent=6)
