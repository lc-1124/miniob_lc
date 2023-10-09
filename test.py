import subprocess
import time
import os
import glob

# 删除/root/miniob/miniob/db/sys/目录下的所有文件
files_to_remove = glob.glob('/root/miniob/miniob/db/sys/*')
for f in files_to_remove:
    try:
        os.remove(f)
    except Exception as e:
        print(f"Error deleting file {f}: {e}")

# 启动observer进程的命令
observer_command = ['./build/bin/observer', '-f', './etc/observer.ini', '-p', '6789']

# 启动obclient进程的命令
obclient_command = ['./build/bin/obclient', '-p', '6789']

# 使用Popen启动observer进程
observer_process = subprocess.Popen(observer_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# 给observer进程一些时间来启动和初始化
time.sleep(2)

# 使用Popen启动obclient进程，并获取stdin、stdout和stderr的句柄
obclient_process = subprocess.Popen(obclient_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# 打开input.txt并逐行读取命令
with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()  # 去掉行尾的换行符
        if line:  # 确保行不是空的
            # 将命令发送到obclient进程
            obclient_process.stdin.write(line + '\n')
            obclient_process.stdin.flush()  # 清空stdin的缓冲区，确保命令被发送

# 从stdout和stderr中读取输出和错误信息
output, error = obclient_process.communicate()

# 打印输出和错误信息
print(output)
if error:
    print("Errors:", error)

# 确保进程已关闭
obclient_process.terminate()
observer_process.terminate()
