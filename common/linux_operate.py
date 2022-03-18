# -*- coding: utf-8 -*- 
# @Time : 2022/3/9 18:14 
# @Author : Yu yang
# @File : linux_operate.py
import os

import paramiko
from paramiko.ssh_exception import AuthenticationException
from scp import SCPClient
from common.log import Log
from common.excel import DoExcel


class Linux:
    """
    linux相关操作
    """

    def __init__(self, file=None):
        self.log = Log(file=file)

    def pull_file(self, login: list, remote_path: list, local_path: str):
        """
        获取远程服务器文件到指定本地目录
        :param login: ip,账号，密码
        :param remote_path: 已列表形式存放需要获取的远程文件
        :param local_path: 已字符串形式把获取的远程文件存入本地指定路径
        :return:
        """

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        # 会话对象需不需要密码

        if len(login) == 2:
            ssh_client.connect(port=22, username=login[1], hostname=login[0])
        else:
            ssh_client.connect(port=22, username=login[1], password=login[2], hostname=login[0])
        scpclient = SCPClient(ssh_client.get_transport(), socket_timeout=15.0)

        for remote_file_path in remote_path:

            try:
                scpclient.get(remote_path=remote_file_path, local_path=local_path)
            except FileNotFoundError:
                self.log.error("系统找不到指定文件" + remote_file_path)
            except AuthenticationException:
                self.log.error("身份验证失败：{}".format(login[0]))
            else:
                self.log.info(f'{remote_file_path}文件已存入本地路径{local_path}')
        ssh_client.close()

    def push_file(self, local_path: str, login: list, remote_path: str):
        """
        本地文件推送远程服务器的指定目录
        :param login:  密码和ip
        :param local_path: 本地路径
        :param remote_path: 远程路径
        :return:
        """

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        for info in login:
            if len(info) == 2:
                ssh_client.connect(port=22, username=info[1], hostname=info[0])
            else:
                ssh_client.connect(port=22, username=info[1], password=info[2], hostname=info[0])
            scpclient = SCPClient(ssh_client.get_transport(), socket_timeout=15.0)

            for local_file in os.listdir(local_path):
                try:
                    scpclient.put(files=local_file, remote_path=remote_path)
                except FileNotFoundError as e:
                    self.log.error("系统找不到指定文件" + local_file)
                except AuthenticationException as e:
                    self.log.error("身份验证失败：{}".format(info[0]))
                self.log.info('推送成功')
        ssh_client.close()

    def linux_order(self, login, order):
        """
        与远程服务器交互，执行linux命令
        :param order: 多条命令格式：字符串内；分隔
        :param login: ip--/用户名--/密码
        :return:
        """

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        for info in login:
            self.log.info('开始连接')

            if len(info) == 2:
                client.connect(hostname=info[0], port=22, username=info[1], password=None)
            else:
                client.connect(hostname=info[0], port=22, username=info[1], password=info[2])
            try:
                self.log.info('执行命令')
                # 如erms安装过程是否覆盖需要再sudo执行后输入是否确认
                stdin, stdout, stderr = client.exec_command(order, get_pty=True)
                if len(info) >= 3:
                    self.log.info('需要输入密码')
                    stdin.write(info[-1] + '\n')  # 执行输入命令，输入sudo命令的密码，会自动执行
                    self.log.info('输出命令结果')
                for line in stdout:
                    print(line.strip('\n'))


            except BaseException as e:
                self.log.error('{}：执行失败{}'.format(info[0], e))
                continue
        client.close()


if __name__ == '__main__':
    l = Linux()
    l.push_file('../data/erms_config')
