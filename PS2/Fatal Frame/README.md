# Fatal Frame

## EU
### Subtitles
* The arrays `subtitles####` contain the `int` values in order of their required subtitle ID
* `Address` of the first sentence in the first cinematic `0x86AFDF`
* Find the sentences through the method `int GetStrWidthMain(byte *text,long param_2)`

#### Subtitle Files
* English -> `40`
* French -> `41`
  * Offset: `0x20FD0`
* Deutsch -> `42`
* Spanish -> `43`
* Italian -> `44`

### Hex Values Ascii
* `0x00` -> ` `
* `0x01` -> `A`
* `0x02` -> `B`
* `0x03` -> `C`
* `0x04` -> `D`
* `0x05` -> `E`
* `0x06` -> `F`
* `0x07` -> `G`
* `0x08` -> `H`
* `0x09` -> `I`
* `0x0A` -> `J`
* `0x0B` -> `K`
* `0x0C` -> `L`
* `0x0D` -> `M`
* `0x0E` -> `N`
* `0x0F` -> `O`
* `0x10` -> `P`
* `0x11` -> `Q`
* `0x12` -> `R`
* `0x13` -> `S`
* `0x14` -> `T`
* `0x15` -> `U`
* `0x16` -> `V`
* `0x17` -> `W`
* `0x18` -> `X`
* `0x19` -> `Y`
* `0x1A` -> `Z`
* `0x1B` -> `a`
* `0x1C` -> `b`
* `0x1D` -> `c`
* `0x1E` -> `d`
* `0x1F` -> `e`
* `0x20` -> `f`
* `0x21` -> `g`
* `0x22` -> `h`
* `0x23` -> `i`
* `0x24` -> `j`
* `0x25` -> `k`
* `0x26` -> `l`
* `0x27` -> `m`
* `0x28` -> `n`
* `0x29` -> `o`
* `0x2A` -> `p`
* `0x2B` -> `q`
* `0x2C` -> `r`
* `0x2D` -> `s`
* `0x2E` -> `t`
* `0x2F` -> `u`
* `0x30` -> `v`
* `0x31` -> `w`
* `0x32` -> `x`
* `0x33` -> `y`
* `0x34` -> `z`
* `0x53` -> `è`
* `0x54` -> `é`
* `0x8B` -> `'`

### Language

Selected language is located at `0x0025605C`
* `0x0` -> English
* `0x1` -> French
* `0x2` -> Deutsch
* `0x3` -> Espanol
* `0x4` -> Italian

```
// This method returns the beginning of the file info located in the IMG_HD.BIN
GetImgArrangement(int file_index_){
    return file_index * 8 + 0x12f0000;
}
```

Therefore, it means that file info are `8` of length

### Files
For each file:
* 4 byte - LBA
* 4 byte - Size

Calculation of real LBA:
* real LBA = LBA * 0x800

Total Number of File:  
* US -> `0x769`
* JP -> `0x73A`
* EU -> `0x879`

