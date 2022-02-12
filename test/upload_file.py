# -*- coding: utf-8 -*-
import logging
import os
import paramiko  # 用于调用scp命令
from paramiko.ssh_exception import AuthenticationException
from scp import SCPClient
from common.excel import DoExcel
from common import path


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


def run(fpath, userPass):
    """
    运行
    :param userPass: ip和密码
    :param fpath: 远端的路径
    :return:
    """

    for file in os.listdir(path.file_dir):
        for i in userPass:
            try:
                upload_file(i[1], i[0],
                            file_path=path.file_dir,
                            file_name=file,
                            remote_path=fpath, )
            except:
                print('{}传送失败：{}'.format(file, i[1]))
                continue


def whilerun(fpath, userPass):
    """
    死循环执行一个
    :param userPass: ip和密码
    :param fpath: 远端的路径
    :return:
    """
    while True:
        try:
            logging.error("开始传输")

            upload_file(userPass[1], userPass[0],
                        file_path=path.file_dir,
                        # file_name=r"../file/fta-1.0.0-release-jd-20220112-001-new-linux.deb",
                        file_name=r"../file/fta-1.0.0-release-jd-20220112-001-new-linux.deb",
                        remote_path=fpath, )
        except:
            print('传送失败')
            continue
        logging.error("传输完成")


if __name__ == '__main__':
    print('执行脚本前请确认file目录里文件，都为必传文件！！！！！！！！！！')
    print('正常情况传输全部失败，因权限问题修改"fpath"目标路径即可')
    # data = DoExcel(r'C:\Users\yuyang\Downloads\KK仓机器人.xlsx','Sheet1').readUserPass()
    if input('请确认知晓：'):
        whilerun(fpath=r"/home/ld/Desktop", userPass=('ld','10.3.2.72'))
    for i in os.listdir(path.file_dir):
        os.remove(os.path.join(path.file_dir, i))
        print('上传完成，文件清空完成！！！')