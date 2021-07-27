# Fatal Frame

## EU
### Subtitles
* The arrays `subtitles####` contain the `int` values in order of their required subtitle ID
* `subtitles_sys[12]`@`002af454` seems to be ID of the current subtitle to be displayed
* `Address` of the first sentence in the first cinematic `0x86AFDF`
* Find the sentences through the method `int GetStrWidthMain(byte *text,long param_2)`

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

