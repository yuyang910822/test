# -*- coding: utf-8 -*- 
# @Time : 2021/12/29 14:29 
# @Author : Yu yang
# @File : batchingLinux.py

import paramiko
from common.excel import DoExcel


def Cmd(cmd, fpath=None, bname=None):
    """
    与远程服务器交互，执行linux命令
    多条命令格式：字符串内；分隔
    :param cmd: 执行命令，多条；隔开
    :param fpath: excel路径
    :param bname: execl表单名称
    :return:
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # user_pass = DoExcel(fpath, bname).readUserPass()
    data = [['root','10.3.4.169']]
    for i in data:
        if len(data) <=2:
            print('开始连接')
            client.connect(hostname=i[1], port=22, username=i[0])
            # client.connect(hostname=i[1], port=22, username=i[0], password=i[0])
            # client.connect(hostname='10.3.4.169', port=22, username='root')
            try:
                stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
                stdin.write(i[0] + '\n')  # 执行输入命令，输入sudo命令的密码，会自动执行
                for line in stdout:
                    print(line.strip('\n'))
            except:
                print('{}：执行完成'.format(i[1]))
                client.close()


if __name__ == '__main__':
    Cmd(cmd='cd /home/ld;pwd;sudo mkdir yy;cd yy;'
            'wget http://packages.forwardx.ai/download/02.RCS/v1.10/Official/1.10.100/ERMS/a4stack-erms-schedule-manager-1.10.14.deb')
