menu_curr_costume = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8]
menu_costume_letter = ['nomral', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
clear_flg_ctrl = 0x0027f148

unlocked_costumes = 0x1FF #0x00 | 0x100 | 0x80 | 0x60 | 0x18 | 0x6

iVar4 = 0
# Check for moving up in list
for curr_costume in menu_curr_costume:
    iVar6 = (curr_costume + 0x1) % 0x9
    iVar5 = iVar6 << 0x18
    new_curr_costume = iVar6
    uVar7 = iVar5 >> 0x18
    iVar4 += 1
    #Left side assignation : hex((clear_flg_ctrl + (iVar5 >> 0x1d) * 4 + 0x10)) -> always 0x0027f158 -> FF
    check_statement = unlocked_costumes & 1 << (uVar7 & 0x1f)
    print(f'costume:{curr_costume, menu_costume_letter[curr_costume]}, check_statement:{check_statement}, RS:{1 << (uVar7 & 0x1f)}, uVar7:{uVar7}, iVar6:{iVar6}, iVar4:{iVar4}')

