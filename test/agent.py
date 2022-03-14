# -*- coding: utf-8 -*- 
# @Time : 2022/3/9 18:02 
# @Author : Yu yang
# @File : agent.py


from common.service import Cmd
from common.linux_operate import Linux


def agent_install(login):
    c = Linux()
    download_agent = f'cd /home/ld;wget {input("请输入下载连接:")} --no-check-certificate'
    print(download_agent)
    # 下载agnet
    f = c.linux_order(login, download_agent)
    # 安装agent
    package = download_agent.split('/')[-1].split(' ')[0]
    print(package)
    install_agent = f'cd /home/ld;' \
                    f'systemctl stop a4stack-erms-agent.service;' \
                    f'sudo dpkg -i {package};' \
                    f'systemctl restart a4stack-erms-agent.service;' \
                    f'systemctl status a4stack-erms-agent.service'
    c.linux_order(login, install_agent)


if __name__ == '__main__':
    # 以列表嵌套格式存储多个AMR信息，单台AMR也需要遵守
    # list[['地址', '用户名'，'密码']]
    agent_install([['10.3.4.169', 'root']])
