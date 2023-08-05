from etabackend.jit_linker import link_libs,link_global,link_function,jit,ffi,nb

BytesofRecords_get = link_global("BytesofRecords")
TTRes_pspr_get = link_global("TTRes_pspr")
SYNCRate_pspr_get = link_global("SYNCRate_pspr")
DTRes_pspr_get = link_global("DTRes_pspr")
TTF_header_offset_get = link_global("TTF_header_offset")
RecordType_get =link_global("RecordType")
PARSE_TimeTagFileHeader = link_function("PARSE_TimeTagFileHeader",2)

@jit(nopython=True, nogil=True)
def PARSE_TimeTagFileHeader_wrapper(UniBuf, filetype):
    link_libs()
    UniBufPtr = ffi.from_buffer(UniBuf)
    ret1 = PARSE_TimeTagFileHeader(UniBufPtr,nb.int32(filetype))
    # can not return them as a list because the cast from int32 to unicode is not possible 
    return (ret1,[
            TTF_header_offset_get(),#0
            TTF_header_offset_get(),#1 set to zero size by default
           
            TTRes_pspr_get(),#2
            DTRes_pspr_get(),#3
            SYNCRate_pspr_get(),#4
            BytesofRecords_get(),#5
            RecordType_get(),#6

            0,#7
            0,
            16,
            0,
            ])

def parse_header(filename1,filetype):
    with open(filename1, "rb") as f:
        fileheader=bytearray(1024*20) #20KB header
        f.readinto(fileheader)
        return PARSE_TimeTagFileHeader_wrapper(fileheader,filetype)
   

if __name__ == "__main__":
    for i in range(1,1000):
        out = parse_header("..\\..\\HH400_T3_80MHz_HBT.ptu",-1)
        print(out)
    with open("llvm.txt", "w") as writeto:
        codelist = PARSE_TimeTagFileHeader_wrapper.inspect_llvm()
        for each in codelist:
            writeto.write(str(each))
            writeto.write("//////////////")
            writeto.write(codelist[each])
