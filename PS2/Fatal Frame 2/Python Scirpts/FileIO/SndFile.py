snd_bank_max = 0x1E
snd_bd_file = 0x4EEE20


# SndBankFileSearch(snd_bd_file);
def SndBankFileGet(param_1):
    sVar1 = 0x0
    iVar2 = 0x0

    if (snd_bank_max < 1):
        param_1 = 0
    else:
        sVar1 = (param_1 + 2)

        while sVar1 != 0:
            iVar2 += 1
            if snd_bank_max <= iVar2:
                param_1 = 0
                return param_1
            sVar1 = (param_1 + 0x12)
            param_1 = param_1 + 0x10

    return param_1


# SndBankFileSearch(snd_bd_file);
def SndBankFileSearch(param_1, param_2):
    iVar1 = 0x0
    if 0 < snd_bank_max:
        while True:
            if ((param_1 + 2) != 0) and ((param_1 + 4) == param_2):
                return param_1

            iVar1 += 1
            param_1 += 0x10
            if iVar1 < snd_bank_max:
                break

    return 0


if __name__ == '__main__':
    print(SndBankFileGet(snd_bd_file))

