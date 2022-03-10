# -*- coding: utf-8 -*- 
# @Time : 2022/1/14 18:21 
# @Author : Yu yang
# @File : service.py
import paramiko
from paramiko.ssh_exception import AuthenticationException
from scp import SCPClient

from common.excel import DoExcel


class Service:

    # def __init__(self, fpath, bname):
    #     """
    #
    #     :param fpath: 文件路径
    #     :param bname: 表单名称
    #     """
    #     self.userpass = DoExcel(fpath, bname).readUserPass()

    @staticmethod
    def upload_file(host, password, file_name, remote_path, file_path):

        """
        文件上传到远程服务器
        :param host: 连接地址
        :param password: 密码
        :param file_name: 本地文件名称
        :param remote_path: 远端存放路径
        :param file_path: 本地文件路径
        :return:
        """

        port = 22  # 端口号
        username = 'ld'

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        local_path = file_path + "\\" + file_name
        try:
            ssh_client.connect(host, port, username, password)
            scpclient = SCPClient(ssh_client.get_transport(), socket_timeout=15.0)
            scpclient.put(local_path, remote_path)
        except FileNotFoundError as e:
            print(e)
            print("系统找不到指定文件" + local_path)
        except AuthenticationException as e:
            print("身份验证失败：{}".format(host))
        ssh_client.close()


def Cmd(cmd, user_pass=None, fpath=None, bname=None):
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
    try:
        user_pass = DoExcel(fpath, bname).readUserPass()
    except BaseException as ff:
        print(ff)
    finally:
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
