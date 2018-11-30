import os
from ftplib import FTP
import time
import filetype
import struct

ftp = FTP();
ftp_ip = '192.168.80.219';
port = 21;
timeout = 30;
user = 'steven.liu';
pwd = 'moremoney';

#local directory
LocalSourcePath = 'D:\p4\GV300N\MCU_6261A_MOB_NEW\\build';
CurAbsPath = os.path.abspath('.');
SourcePath = LocalSourcePath + '\GV300N_MOD_11C';
SourceFileNames = os.listdir(SourcePath);
print("SourcePath path is:",SourcePath);
#print("SourceFileNames is:",SourceFileNames);

#target directory
TargetPath = '/MD/steven/' + os.getlogin();
print("Target path is:",TargetPath);

#local user account name / os info
#print("Current Os is:",os.name);
#print("Current User is:",os.getlogin());

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

def GetNowTimeStamp():
    return time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
 #   return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

#print("Current time is:",GetNowTimeStamp());
 
def findfiletype(filename):
    bFound = False
    if os.path.getsize(filename) < 8:
       return bFound
    file_handler = open(filename,'rb')
    filetype_dict = filetypedict()
    ftype = 'unknown'
    #print("Current file is %s,size is %d"%(filename,os.path.getsize(filename)));
    for headerindict in filetype_dict.keys():
        numofbytes = int(len(headerindict) /2) #bytes need read for each filetype
        file_handler.seek(0)  #set file pointer to 0
        #print('CurrHeader is %s,numbofbytes is %d'%(headerindict,numofbytes))
        headerbyte = struct.unpack_from("B"*numofbytes,file_handler.read(numofbytes))
        curfilehead = bytes2hex(headerbyte)
        if curfilehead == headerindict:
            ftype = filetype_dict[headerindict];
            bFound = True
            break
    file_handler.close();
    return bFound
 
def ftp_connect():
 #   ftp.set_debuglevel(2); #debug info 2 -- detail， 0 - close
    ftp.connect(ftp_ip,port,timeout);
    ftp.login(user,pwd);
    print("FTP connect ok");
    
def ftp_disconnect():
    ftp.set_debuglevel(0); #debug info 2 -- detail， 0 - close
    ftp.close();
    print("FTP disconnect ok");
    
#md new directory, use current timestamp as name,return new path
def ftp_mdnewdir1(currentdir):
    ftp.cwd(currentdir);
    curtimestamp = GetNowTimeStamp();
    try:
        ftp.mkd(curtimestamp);
    except ftplib.error_perm:
        print("WARNING: No Authority to make dir");
    finally:
        return currentdir + '/' + curtimestamp ;
    
#md new directory, if not exist, then create a new one 
#def ftp_mdnewdir2(sourcedir):      
def ftp_uploadfile(localfile,targetfile):
    if os.path.isfile(localfile) == False:
        return False;
    file_handle = open(localfile,'rb');
    ftp.storbinary('STOR %s'%targetfile,file_handle,4096);
    file_handle.close();
    return True;
    
def ftp_uploadtree(localpath,targetpath):  #search sub-directory
    if os.path.isdir(localpath) == False:
        return False;
    print("Upload_localpath is:",localpath);
    localfiles = os.listdir(localpath);
    print("localfilenames is:",localfiles);
    print("Targetpath is:",targetpath);
    ftp.cwd(targetpath);
    for opfile in localfiles:
        src = os.path.join(localpath,opfile);
        print("Cur dir/file is:",src);
        if os.path.isdir(src): 
            ftp.mkd(opfile);
            ftp_uploadtree(src,opfile);
        else :
            if findfiletype(src) == True:
                ftp_uploadfile(src,opfile);
        print("Deal %s successfully!"%src);
    ftp.cwd('..');
    return;

def ftp_uploadtree2(localpath,targetpath):  #not search sub-directory
	if os.path.isdir(localpath) == False:
		return False;
	print("Upload_localpath is:",localpath);
	localfiles = os.listdir(localpath);
#	print("localfilenames is:",localfiles);
	print("Targetpath is:",targetpath);
	ftp.cwd(targetpath);
	for opfile in localfiles:
		src = os.path.join(localpath,opfile);
		if os.path.isdir(src) == True:
			print("%s is dir"%src);
		else :
			print("%s is a file"%src);
			if findfiletype(src) == True:
				ftp_uploadfile(src,opfile);
			print("Deal %s successfully!"%src);
	ftp.cwd('..');
	return;
	
def main():
    ftp_connect();
    #ftp.cwd(TargetPath);
    #ftp_uploadfile('kpi.xlsx','kpi.xlsx');
    #ftp_uploadtree(SourcePath,TargetPath);
    #ftp_uploadtree(SourcePath,ftp_mdnewdir1(TargetPath));
    ftp_uploadtree2(SourcePath,ftp_mdnewdir1(TargetPath));
    #ftp.dir();
    ftp_disconnect(); 
    
if __name__ == '__main__':
    main();