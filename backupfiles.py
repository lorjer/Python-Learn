import os
import shutil
import time

#利用windows 共享目录的方式上传文件
def GetNowTimeStamp():
    return time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
 #   return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
  
CurAbsPath = os.path.abspath('.');

RemoteHostIP = '192.168.80.219';
ShareDirName = '\\Steven_test\\';
RemoteDstDir = '\\\\' + RemoteHostIP + ShareDirName + os.getlogin() + '_' + GetNowTimeStamp();
#RemoteDstDir = '\\\\' + hostIP + '\\Steven_test' + '\copyfiletest1';

#上传目录文件至windows共享文件夹
shutil.copytree(CurAbsPath,RemoteDstDir);