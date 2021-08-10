audio_segment = b'\x00\x00\x01\xBD'
pack_start = b'\x00\x00\x01\xBA'
end_file = b'\x00\x00\x01\xB9'

first_header_size = 0x3f
header_size = 0x17


def seek_next_audio(file):
    while True:
        block_id = file.read(0x4)

        if block_id == pack_start:
            file.seek(0xa, 1)
        elif block_id == audio_segment:
            return False
        elif block_id == end_file:
            return True
        else:
            block_size = file.read(0x2)
            file.seek(int.from_bytes(block_size, 'big'), 1)


def initial_audio_block(file):
    b_size = int.from_bytes(file.read(0x2), 'big')

    file.seek(0x3b - 0x6, 1)

    audio_total_size = int.from_bytes(file.read(0x4), 'little')

    data_size = b_size - first_header_size + 0x6

    print(audio_total_size)
    print(data_size)

    return [audio_total_size, data_size]


def audio_block(file):
    b_size = int.from_bytes(file.read(0x2), 'big')

    file.seek(-0x6, 1)
    file.seek(header_size, 1)

    data_size = b_size - header_size + 0x6

    print(data_size)

    return data_size


def build_full_audio_buffer(file):
    seek_next_audio(file)
    total_size, curr_block_size = initial_audio_block(file)
    buff = []
    buff += file.read(curr_block_size)

    while True:
        done = seek_next_audio(file)

        if done:
            break

        curr_block_size = audio_block(file)

        buff += file.read(curr_block_size)

    file.seek(0)
    return buff


if __name__ == '__main__':
    eu = open('D:\DecompressFiles\Fatal Frame Undub\eu.PSS', 'rb+')
    jp = open('D:\DecompressFiles\Fatal Frame Undub\jp.PSS', 'rb')

    total_buffer_written = 0x0
    jp_full_buff = build_full_audio_buffer(jp)

    seek_next_audio(eu)
    seek_next_audio(jp)

    eu_total_size, eu_curr_block_size = initial_audio_block(eu)
    jp_total_size, jp_curr_block_size = initial_audio_block(jp)

    jp.seek(jp_curr_block_size, 1)
    eu.write(bytearray(jp_full_buff[0:eu_curr_block_size]))

    total_buffer_written += eu_curr_block_size

    while True:
        eu_done = seek_next_audio(eu)
        jp_done = seek_next_audio(jp)

        if eu_done or jp_done:
            break

        eu_curr_block_size = audio_block(eu)
        jp_curr_block_size = audio_block(jp)

        jp.seek(jp_curr_block_size, 1)

        end_offset = total_buffer_written + eu_curr_block_size
        eu.write(bytearray(jp_full_buff[total_buffer_written:end_offset]))

        total_buffer_written += eu_curr_block_size

        if eu_curr_block_size < jp_curr_block_size:
            print('Smaller block size')
        elif eu_curr_block_size > jp_curr_block_size:
            print('Bigger block size')

    eu.close()
    jp.close()
