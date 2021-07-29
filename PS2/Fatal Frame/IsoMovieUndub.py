from io import BytesIO

import pycdlib


folder_jp = 'D:/DecompressFiles/Fatal Frame Undub/Japan'
folder_eu = 'D:/DecompressFiles/Fatal Frame Undub/EUROPE'


def extract_all_files_from_iso(folder, iso_file_name):
    iso = pycdlib.PyCdlib()

    iso.open(f'{folder}/{iso_file_name}')

    aa = ['MOVIE', 'MOVIE2']

    file_no = 0
    file_not_undub = 0

    for x in aa:
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

                if size_jp <= size_eu:
                    print(f'File: {iso_file}, Offset: {offset_eu}, Offset JP: {offset_jp}, Size: {size_eu}, Size Jp: P{size_jp}')
                    iso_target = open(f'{folder_eu}/ffeu.iso', 'rb+')
                    iso_target.seek(offset_eu)
                    iso_target.write(buffer)
                    iso_target.close()
                else:
                    file_not_undub += 1
                    print(f'Cannot undub file: {iso_file}, Offset: {offset_eu}, Size: {size_eu}, Diff: {size_jp - size_eu}')

    iso.close()

    print(f'{file_not_undub}/{file_no}')


if __name__ == '__main__':
    extract_all_files_from_iso(folder_jp, 'ff_jp.iso')
