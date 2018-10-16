import os
from ftplib import FTP
import time

ftp = FTP();
ftp_ip = '192.168.80.219';
port = 21;
timeout = 30;
user = 'steven.liu';
pwd = 'moremoney';

#local directory
LocalSourcePath = 'E:\Github\Testsource';
CurAbsPath = os.path.abspath('.');
SourcePath = LocalSourcePath + '\copyfiletest1';
SourceFileNames = os.listdir(SourcePath);
print("SourcePath path is:",SourcePath);
print("SourceFileNames is:",SourceFileNames);

#target directory
TargetPath = '/MD/' + os.getlogin();
print("Target path is:",TargetPath);

#local user account name / os info
#print("Current Os is:",os.name);
print("Current User is:",os.getlogin());

def GetNowTimeStamp():
    return time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
 #   return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

print("Current time is:",GetNowTimeStamp());
 
def ftp_connect():
 #   ftp.set_debuglevel(2); #debug info 2 -- detail， 0 - close
    ftp.connect(ftp_ip,port,timeout);
    ftp.login(user,pwd);
    print("FTP connect ok");
    
def ftp_disconnect():
    ftp.set_debuglevel(0); #debug info 2 -- detail， 0 - close
    ftp.close();
    print("FTP disconnect ok");
    
#md new directory, use current timestamp as name,return 
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
    
def ftp_uploadtree(localpath,targetpath):
    if os.path.isdir(localpath) == False:
        return False;
    print("Upload_localpath is:",localpath);
    localfiles = os.listdir(localpath);
    print("localfilenames is:",localfiles);
    print("Targetpath is:",targetpath);
    ftp.cwd(targetpath);
    for opfile in localfiles:
        src = os.path.join(localpath,opfile);
        if os.path.isdir(src): 
            ftp.mkd(opfile);
            ftp_uploadtree(src,opfile);
        else :
            ftp_uploadfile(src,opfile);
    ftp.cwd('..');
    return;
    
ftp_connect();
#ftp.cwd(TargetPath);
#ftp_uploadfile('kpi.xlsx','kpi.xlsx');
#ftp_uploadtree(SourcePath,TargetPath);
ftp_uploadtree(SourcePath,ftp_mdnewdir1(TargetPath));

ftp.dir();
ftp_disconnect();