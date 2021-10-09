# Import Statements
import struct


def get_uint16(file_r):
    return struct.unpack('<H', file_r.read(0x2))[0]


def get_float32(file_r):
    return struct.unpack('<f', file_r.read(0x4))[0]


def get_uint32(file_r):
    return struct.unpack('<I', file_r.read(0x4))[0]


def get_uint_from_byte(file_r):
    return int.from_bytes(file_r.read(0x1), 'little', signed=False)
