# Import statements
from FileGlobalParameters import *

# Look into the following method, as it seems to be remapping a file values into a vertex list
#{Some data}
#{Some float array}
#{File name}
def sgdRemap(sgdFileHeader):
    if sgdFileHeader == 0x0:
        return
    if sgdFileHeader.file_header_id != 0x1050:
        return
    if sgdFileHeader.indicators != 0:
        return

    uVar7 = sgdFileHeader.info_size
    sgdFileHeader.file_initialized = True

    if uVar7 < 0x30000000:
        first_loop_index = sgdFileHeader.file_header_id + uVar7
        if uVar7 != 0:
            sgdFileHeader.info_size = first_loop_index
            uVar7 = first_loop_index

    # Checks if the file has been initialized, if not, the original value at sgdFileHeader.name_ptr (which is raw in
    # file) is the total size of the header but the final value will be the file_name which is located later in the file
    # (hence why the X + sgdFileHeader)
    # The first condidition is checking if the resulting address is not within the IMG_BD.BIN addr
    # The second condition is checking that the resulting pointer is not just and empty char
    pcVar1 = sgdFileHeader.name_ptr
    if (pcVar1 < 0x30000000) and (pcVar1 != 0x0):
        sgdFileHeader.name_ptr = pcVar1 + sgdFileHeader

    #if uVar7 == 0:
        #iVar3 = sgdFileHeader->field_0x10;
