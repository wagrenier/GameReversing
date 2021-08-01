import json
import struct
from io import BytesIO

import pycdlib


folder_jp = 'D:/DecompressFiles/Fatal Frame Undub/Japan'
folder_eu = 'D:/DecompressFiles/Fatal Frame Undub/EUROPE'


def undub_pss(folder, iso_file_name):
    iso = pycdlib.PyCdlib()

    iso.open(f'{folder}/{iso_file_name}')

    movies = ['MOVIE', 'MOVIE2']

    full_buffer = []
    with open(f'{folder_eu}/ffeu.iso', 'rb') as fs:
        full_buffer = fs.read()

    file_no = 0
    file_not_undub = 0

    file_db = []

    for x in movies:
        for child in iso.list_children(iso_path=f'/{x}'):
            if child.file_identifier() == b'.' or child.file_identifier() == b'..':
                continue

            iso_file = f'/{x}/{child.file_identifier().decode("utf-8")}'
            with iso.open_file_from_iso(iso_path=iso_file) as infp:
                file_no += 1
                offset_jp = infp.__getattribute__('_startpos')
                buffer = infp.read()
                offset_eu = 0x0
                size_eu = 0x0
                size_jp = len(buffer)

                iso_target = pycdlib.PyCdlib()
                iso_target.open(f'{folder_eu}/ffeu.iso')

                with iso_target.open_file_from_iso(iso_path=iso_file) as infp2:
                    offset_eu = infp2.__getattribute__('_startpos')
                    size_eu = len(infp2.read())
                iso_target.close()

                aa = full_buffer.find(struct.pack('<I', size_eu))
                a = {
                    'EuSizeOffset': aa,
                    'Filename': iso_file,
                    'EuOffset': offset_eu,
                    'EuSize': size_eu,
                    'JpOffset': offset_jp,
                    'JpSize': size_jp,
                }

                file_db.append(a)

                if size_jp <= size_eu:
                    print(f'File: {iso_file}, Offset: {offset_eu}, Offset JP: {offset_jp}, Size: {size_eu}, Size Jp: {size_jp}')
                    #iso_target = open(f'{folder_eu}/ffeu.iso', 'rb+')
                    #iso_target.seek(offset_eu)
                    #iso_target.write(buffer)
                    #iso_target.close()
                else:
                    file_not_undub += 1
                    print(f'Cannot undub file: {iso_file}, Offset: {offset_eu}, Size: {size_eu}, Diff: {size_jp - size_eu}')

    iso.close()

    out_file = open(f'{folder_eu}/pss_info.json', "w+")
    json.dump(file_db, out_file, indent=6)

    print(f'{file_not_undub}/{file_no}')


if __name__ == '__main__':
    undub_pss(folder_jp, 'ff_jp.iso')
