# Import statements
from FileGlobalParameters import *


def GetAlignUp(param_1, param_2):
    return ((param_1 + ~(-1 << (param_2 & 0x1f))) >> (param_2 & 0x1f)) << (param_2 & 0x1f)


def cddatIsCmpFile(file_index):
    return cd_dat_tbl[hex(p_cd_dat + file_index * 0xc)] & 1


def cddatIsFile(file_index):
    file_status = cd_dat_tbl[hex(p_cd_dat + file_index * 0xc)] & 0b00000011
    if file_status == 0b00:
        return FileStatus.NO_FILE
    elif file_status == 0b10:
        return FileStatus.FILE_NOT_COMPRESSED
    elif file_status == 0b11:
        return FileStatus.FILE_COMPRESSED

    return FileStatus.NO_FILE



def GetFileData(file_index, param_2):
    # The second parameter might be a file within a file?
    #    iVar2 = GetMenuFileDispFileID(DAT_00404134, (&DAT_00404150)[DAT_00404134 * 3]
    #    iVar3 = GetFileTexId(iVar3,iVar2)
    #    GetFileTexId just transforms it into a pointer

    return (file_dat_tbl + file_index * 4) + param_2 * 4


def GetFile(file_index):
    return GetAlignUp((p_cd_dat + file_index * 0xc), 4)


def GetFileSize(file_index):
    return GetAlignUp((p_cd_dat + file_index * 0xc + 4), 4)


def GetFileCmpSize(file_index):
    return GetAlignUp((p_cd_dat + file_index * 0xc + 8), 4)


def GetFileSectorSize(file_index):
    iVar1 = GetFileSize(file_index)
    return iVar1 + 0x7ff >> 0xb


def GetFileStartSector(file_index):
    return (p_cd_dat + file_index * 0xc) >> 2


def FurnCtlCheckFileType(param_1):
    iVar1 = 0x0
    uVar2 = 0xffffffff

    if param_1 != 0x0:
        iVar1 = param_1
        uVar2 = 0

        if iVar1 != 0x627a70:
            uVar2 = 1
            if iVar1 != 0x666870:
                uVar2 = 2
                if iVar1 != 0x1050:
                    uVar2 = 4
                    if (param_1[1] | param_1[2] | param_1[3]) != 0:
                        uVar2 = 0xffffffff

    return uVar2


def GetFileNoFromSceneNo(scene_number):
    return scene_number * 3 + 0xcd0
