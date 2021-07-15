# Info concerning the coding standards used:
* When a **variable ends** with `_num`, it is most likely a size for an `array`
* All chXXX_Y_ are an array of 15, 31
* When a **variable contains** `_WRK`, it is most likely a `struct`
* When a **variable contains** `_CTRL`, it is most likely an `enum` for control
* When a **variable contains** `cmp`, it is most likely indicating a function for `compressed` data

# General useful information:
* The PS2 DVD sectors are `2048 (0x800) bytes`
* **PCSX2**'s base address is `0x20000000`

# Files
For each file:
* 4 byte - LBA
* 4 byte - unpack file size
* 4 byte - file size in archive

Calculation of real LBA:
* real LBA = (LBA bitwise shift right 2) * 0x800

Value of right 2 bits of LBA is:
* 0 - no file
* 2 - file not compressed
* 3 - file compressed

File ID:
* 0x1064 -> subtitles

File Types
* 0x2 -> MDL?
* 0x3 -> FULL TIM2 (not in model archive)
* 0xC -> str
* 0xD -> DXH
* 0xF -> PSS

# Fun With Cameras
* Address of the pointer containing the current camera's properties `0x003420BC`

# Uncensoring the USA Version

* If a +1 is applied, then you can play as the sister
* The game applies a `+1` to the selected costume for the sister
* Possible to load `Plyr` as `Sis` by giving `Mayu`'s costume ID, which is just a '+1`
* Possible to load `Mayu` as `Plyr` with same logic

## Fatal Frame 2 USA

* Menu address of current selected costume `0x00409125`

Mio (First sister, referenced in code as `Plyr`)
* Mio's selected costume address `0x00408f40`

Mayu (Second sister, referenced in code as `Sis`)
* Mayu's selected costume address `0x00408f44`

(Costume Values)
* NORMAL -> `0x00`, `0x01`
* G -> 0x3E, 0x3F
* H (BLOCKED) -> 0x4C, 0x4D


## Fatal Frame 2 JP
Mio (First sister, referenced in code as `Plyr`)
* Mio's selected costume address `0x00408500`

Mayu (Second sister, referenced in code as `Sis`)
* Mayu's selected costume address `0x00408504`

