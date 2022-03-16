# -*- coding: utf-8 -*- 
# @Time : 2022/3/9 18:02 
# @Author : Yu yang
# @File : agent.py


from common.service import Cmd
from common.linux_operate import Linux
from common.log import Log


class Agent(Linux):

    def agent_install(self, login):
        """
        下载安装agent
        :param login: 可以手写或读取
        :return:
        """
        download_agent = f'cd /home/ld;wget {input("请输入下载连接:")} --no-check-certificate'
        self.log.info(download_agent)
        # 下载agnet
        f = self.linux_order(login, download_agent)
        # 安装agent
        package = download_agent.split('/')[-1].split(' ')[0]
        self.log.info(package)
        install_agent = f'sudo systemctl stop a4stack-erms-agent.service;' \
                        f'cd /home/ld;' \
                        f'sudo dpkg -i {package};' \
                        f'sudo systemctl restart a4stack-erms-agent.service;' \
                        f'sudo systemctl status a4stack-erms-agent.service'
        self.linux_order(login, install_agent)


if __name__ == '__main__':
    # 以列表嵌套格式存储多个AMR信息，单台AMR也需要遵守
    # list[['地址', '用户名'，'密码']]
    install = Agent(file='../log/agent.log')
    install.agent_install([['10.3.1.174', 'ld', 'ld']])
