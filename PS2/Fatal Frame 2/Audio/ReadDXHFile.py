import glob
from pathlib import Path
import binascii

folder = 'D:/DecompressFiles/Zero2_US/DXH'

if __name__ == '__main__':
    all_files = glob.glob(f'{folder}/*.DXH')

    for file in all_files:
        with open(file, 'rb') as curr_file:
            curr_file.seek(0x29)
            bytes = curr_file.read(0x1)

            curr_file.seek(0x20)
            frequency = int.from_bytes(curr_file.read(0x2), "little", signed=False)
            print(f'File: {Path(file).name}, Value: {binascii.hexlify(bytes)}, freq: {frequency}')
