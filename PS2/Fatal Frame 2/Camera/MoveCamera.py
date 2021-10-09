import struct
import keyboard
from ReadWriteMemory import ReadWriteMemory

rwm = ReadWriteMemory()
cam_info = 0x3420bc
pcsx2_base_ptr = 0x20000000
distance_per_tick = float(1)
curr_camera_ptr = pcsx2_base_ptr + cam_info


def read_value(address):
    return process.read(address)


def add_to_float_at_mem_location(address, new_value_offset):
    value = struct.unpack('f', struct.pack("<I", read_value(address)))[0]
    return struct.unpack('I', struct.pack('f', value + new_value_offset))[0]


def change_value_if_key_pressed(address, new_value_offset, convert_float=True):
    if convert_float:
        new_value = add_to_float_at_mem_location(address, new_value_offset)
        process.write(address, new_value)
    else:
        new_value = process.readByte(address)[0] + new_value_offset
        process.writeByte(address, [new_value])


def apply_change_when_key_pressed(key, address, value_difference, convert_float=True):
    if keyboard.is_pressed(key):
        change_value_if_key_pressed(address, value_difference, convert_float)


def handle_camera_type():
    print()


if __name__ == '__main__':
    process = rwm.get_process_by_name('pcsx2.exe')
    ignoreY = True
    ignoreU = True

    while(True):
        process.open()
        curr_camera_info = read_value(curr_camera_ptr)

        curr_camera_info = pcsx2_base_ptr + curr_camera_info

        curr_camera_info_type = curr_camera_info + 0x8
        curr_camera_info_x = curr_camera_info + 0xC
        curr_camera_info_y = curr_camera_info + 0x10
        curr_camera_info_z = curr_camera_info + 0x14
        curr_camera_info_interest_x = curr_camera_info + 0x18

        if keyboard.is_pressed('y') and not ignoreY:
            change_value_if_key_pressed(curr_camera_info_type, 1, False)
            ignoreY = True

        if not keyboard.is_pressed('y') and ignoreY:
            ignoreY = False

        if keyboard.is_pressed('u') and not ignoreU:
            change_value_if_key_pressed(curr_camera_info_type, -1, False)
            ignoreU = True

        if not keyboard.is_pressed('u') and ignoreU:
            ignoreU = False

        apply_change_when_key_pressed('p', curr_camera_info_x, distance_per_tick)
        apply_change_when_key_pressed('o', curr_camera_info_x, -distance_per_tick)

        apply_change_when_key_pressed('l', curr_camera_info_y, distance_per_tick)
        apply_change_when_key_pressed(';', curr_camera_info_y, -distance_per_tick)

        apply_change_when_key_pressed(',', curr_camera_info_z, distance_per_tick)
        apply_change_when_key_pressed('.', curr_camera_info_z, -distance_per_tick)

        apply_change_when_key_pressed('g', curr_camera_info_interest_x, distance_per_tick)
        apply_change_when_key_pressed('h', curr_camera_info_interest_x, -distance_per_tick)

        process.close()