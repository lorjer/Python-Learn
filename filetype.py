import struct

testfile = 'E:\Github\Testsource\GV56R00A01V01M128_MXIC_UBI\MT3333.bin'

def filetypedict():
    return {
    '4341544405000000':'Mt2503AE_Databasefile',
    '4D4D4D0138000000':'Mt2503AE_EXTBOOTLOADER/BIN/ROM',
    '18F09FE5':'MT3333',
    '233C5359':'SYM',
    '41524D20':'LIS',
    '7F454C46':'ELF',    
    '23232323':'CFG' '''text file,23 = #'''
    '''
    'FFD8FF':'JPEG',
    '89504E47':'PNG',
    '47494638':'GIF',
    '49492A00':'TIFF',
    '424D':'bmp',
    '38425053':'psd',
    '7B5C727466':'rtf',
    '3C3F786D6C':'XML',
    '68746D6C3E':'HTML',
    '44656C69766572792D646174653A':'eml',
    '2142444E':'pst',
    'CFAD12FEC5FD746F':'dbx',
    'D0CF11E0':'xls.or.doc',
    '5374616E64617264204A':'mdb'
    '''
    }
    
# string convert into hex string
def bytes2hex(string):
    num = len(string)
    hexstr = u""
    for i in range(num):
        t = u"%x" % string[i]
        if len(t)%2:
            hexstr += u'0'
        hexstr += t
    return hexstr.upper()
    
def filetype(filename):
    file_handler = open(filename,'rb')
    filetype_dict = filetypedict()
    ftype = 'unknown'
    for headerindict in filetype_dict.keys():
        numofbytes = int(len(headerindict) /2) #bytes need read for each filetype
        file_handler.seek(0)  #set file pointer to 0
        headerbyte = struct.unpack_from("B"*numofbytes,file_handler.read(numofbytes))
        curfilehead = bytes2hex(headerbyte)
        if curfilehead == headerindict:
            ftype = filetype_dict[headerindict];
            break
    file_handler.close();
    return ftype

if __name__ == '__main__':
    print('find {} file'.format(filetype(testfile)))