# -*- coding: utf-8 -*- 
# @Time : 2021/12/29 14:29 
# @Author : Yu yang
# @File : batchingLinux.py

import paramiko
from common.excel import DoExcel


def Cmd(cmd, fpath, bname):
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

    user_pass = DoExcel(fpath, bname).readUserPass()

    for i in user_pass:
        print('开始连接')
        client.connect(hostname=i[1], port=22, username='ld', password=i[0])
        try:
            stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
            stdin.write(i[0] + '\n')  # 执行输入命令，输入sudo命令的密码，会自动执行
            for line in stdout:
                print(line.strip('\n'))
        except:
            print('{}：执行完成'.format(i[1]))
            continue
        client.close()


if __name__ == '__main__':
    Cmd(cmd='pwd;cd /home;pwd',
        fpath=r'C:\Users\yuyang\Downloads\KK仓机器人.xlsx',
        bname='Sheet1')
