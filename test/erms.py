# -*- coding: utf-8 -*- 
# @Time : 2022/2/25 11:49 
# @Author : Yu yang
# @File : erms.py
import os, time, paramiko, requests
from paramiko.ssh_exception import AuthenticationException
from scp import SCPClient
from common.path import erms_dir
from core.core_business import Business_ability


class Erms(Business_ability):

    def get_version(self, re_data):
        """
        获取连接内所有版本名称与连接进行拼接，生成版本下载连接地址
        :param re_data: 请求数据
        :return: 各个版本下载连接地址
        """
        r = self.re(re_data)
        data1 = []
        for i in r.text.split('<tr><td><a')[2:]:
            f = ''.join([re_data["url"], i.split('" title')[0].split(' href="')[1]])
            data1.append(f)
        return data1

    def download_upload_config(self, data, path, judge):
        """
            拉取推送指定文件到指定目录
        :param path: 路径
        :param data: 用户名和ip
        :param judge: True拉取，False推送
        :return:
        """
        port = 22  # 端口号
        username = 'ld'
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        erms = ['/etc/a4stack/erms-agent.conf', '/etc/a4stack/erms-api.conf', '/etc/a4stack/erms-base-manager.conf',
                '/etc/a4stack/erms-broker.conf', '/etc/a4stack/erms-job-manager.conf',
                '/etc/a4stack/erms-map-manager.conf', '/etc/a4stack/erms-monitoring-manager.conf',
                '/etc/a4stack/erms-mp-poller.conf', '/etc/a4stack/erms-schedule-manager.conf',
                '/etc/a4stack/erms-thirdparty-manager.conf']

        if judge:
            for i in erms:
                try:
                    ssh_client.connect(data[1], port, data[0], )
                    scpclient = SCPClient(ssh_client.get_transport(), socket_timeout=15.0)
                    scpclient.get(i, path)
                except FileNotFoundError as e:
                    print(e)
                    print("系统找不到指定文件" + data[3])
                except AuthenticationException as e:
                    print("身份验证失败：{}".format(data[1]))
                print('拉取/导入成功')
                ssh_client.close()
        else:
            for file in os.listdir(path):
                i = os.path.join(path, file)
                try:
                    ssh_client.connect(data[1], port, data[0], )
                    scpclient = SCPClient(ssh_client.get_transport(), socket_timeout=15.0)

                    scpclient.put(i, '/etc/a4stack')
                except FileNotFoundError as e:
                    print(e)
                    print("系统找不到指定文件" + data[3])
                except AuthenticationException as e:
                    print("身份验证失败：{}".format(data[1]))
                print('拉取/导入成功')
                ssh_client.close()

    def install(self, data, cmd):
        """
        :param data: 连接的服务器数据--> list
        :return:
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(hostname=data[1], port=22, username=data[0])
        try:
            print(f'开始执行{cmd}')
            stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
            stdin.write('n' + '\n')  # 执行输入命令，输入sudo命令的密码，会自动执行
            for line in stdout:
                print(line.strip('\n'))
        except:
            print('{}：执行失败'.format(data[1]))
            client.close()


if __name__ == '__main__':
    from common.readYaml import *
    from common.path import *

    f = Erms()

    path = os.path.join(erms_dir, str(int(time.time())))
    data = readYaml(url_dir)["ermsPackage"]
    userip = ['root', '10.3.4.169']
    # data["url"] = input('请输入下载地址：')
    data["url"] = 'http://packages.forwardx.ai/download/04.Others/SW_OLY/RCS/ERMS/'

    print(f.get_version(data))

    # 创建文件夹存放erms当前配置文件
    filename = os.system(fr'mkdir {userip[2]}')
    # 获取服务器配置文件到本地文件夹
    f.download_upload_config(userip, path, judge=True)

    # 下载各个依赖包
    for i in data:
        cmd = f'cd /home/ld;sudo mkdir yy;cd yy;wget {i}'
        f.install(data=userip, cmd=cmd)

    # 安装各个依赖包
    for i in data:
        if i.split("ERMS/")[1].split('.')[-1] == 'rpm':
            cmd1 = f'cd /home/ld/yy;sudo rpm -Uvh {i.split("ERMS/")[1]};n'
            f.install(data=userip, cmd=cmd1)
        else:
            cmd1 = f'cd /home/ld/yy;sudo dpkg -i {i.split("ERMS/")[1]};n'
            f.install(data=userip, cmd=cmd1)

    # 本地配置文件推送服务器指定位置
    f.download_upload_config(userip, path, judge=False)

    # 重启各个服务
    c = ['a4stack-erms-agent.service', 'a4stack-erms-api.service', 'a4stack-erms-base-manager.service',
         'a4stack-erms-broker.service', 'a4stack-erms-job-manager.service', 'a4stack-erms-map-manager.service',
         'a4stack-erms-monitoring-manager.service', 'a4stack-erms-mp-poller.service',
         'a4stack-erms-schedule-manager.service',
         'a4stack-erms-thirdparty-manager.service']
    for i in c:
        cmd = f'cd /etc/systemd/system;systemctl restart {i}'
        f.install(data=userip, cmd=cmd)
