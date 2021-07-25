# Fatal Frame

## EU
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

