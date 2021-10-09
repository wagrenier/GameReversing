import struct
import Zero2TOC

sector_size = 0x800
project_file_num_ = 0x106B
p_cd_dat_us = 0x002F30B8
p_cd_dat_jp = 0x002F25F8
p_ext_lbl = 0x002FF5C0
cd_dat_tbl_us = {}
cd_dat_tbl_jp = {}
file_ext_dat_a = []

folder = 'D:/DecompressFiles/Fatal Frame 2 Undub/full'

elf_file = 'SLUS_207.66'
bin_file = 'IMG_BD.BIN'

file_id = 3283
elf_table_offset = 0x1F40B8

if __name__ == '__main__':
    img_db = open(f'{folder}/{bin_file}', 'ab')
    elf = open(f'{folder}/{elf_file}', 'rb+')

    us_file_db = Zero2TOC(project_file_num_, p_cd_dat_us, p_ext_lbl, cd_dat_tbl_us, file_ext_dat_a)
    jp_file_db = Zero2TOC(project_file_num_, p_cd_dat_jp, p_ext_lbl, cd_dat_tbl_jp, file_ext_dat_a)

    for a_file in jp_file_db.file_table:
        Zero2TOC.print_file_info(a_file)

    new_size = len(pss)
    loc = elf_table_offset + file_id * 0xC
    elf.seek(loc)

    file_start_addr = img_db.tell()

    new_start_address = ((int)(file_start_addr / 0x800) << 2) + 2

    print(hex(new_start_address))

    elf.write(struct.pack('<I', new_start_address))
    elf.write(struct.pack('<I', new_size))

    img_db.write(pss)

    blank_bytes = 0x800 - (img_db.tell() % 0x800)

    img_db.write(bytes(blank_bytes))

    img_db.close()
    elf.close()
