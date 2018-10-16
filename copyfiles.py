#operate file, copy file to other directory
import os
import shutil
import time

def GetNowTimeStamp():
    return time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
 #   return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    

print("Current Os is:",os.name);
print("Current User is:",os.getlogin());
print("Current time stamp is:",GetNowTimeStamp());

CurAbsPath = os.path.abspath('.');
print("Current Abspath is:",CurAbsPath);
print("Num of files in current dir:",os.listdir(CurAbsPath));
#os.path.join(CurAbsPath,'testdir');
#newdir = CurAbsPath+'testdir';
#os.mkdir('newdir');


# copy 本地文件 目录-> 目录
DstPath = 'e:/';

copysrcdir = CurAbsPath + '\copyfiletest1';
copydstdir = DstPath + '\copyfiletest2';

#shutil.copytree(os.path.join(CurAbsPath,'copyfiletest1'),copydstdir);
#shutil.copy2('kpi.xlsx',copydstdir);


#下载远程目录文件至本地
#hostIP = '192.168.80.219';
#RemoteSrcDir = '\\\\' + hostIP + '\\Steven_test';
#shutil.copytree(RemoteSrcDir,copydstdir);

#上传目录文件至windows共享文件夹
#RemoteDstDir = '\\\\' + hostIP + '\\Steven_test' + '\copyfiletest1';
#shutil.copytree(copysrcdir,RemoteDstDir);

