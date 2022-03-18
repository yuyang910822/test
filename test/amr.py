# -*- coding: utf-8 -*- 
# @Time : 2022/3/16 10:05 
# @Author : Yu yang
# @File : amr.py

from common.linux_operate import Linux


class Amr(Linux):
    """

    """

    def amr_install(self, login):
        """

        :param login:
        :return:
        """
        # download_order = f'cd /home/ld;wget {input("请输入下载连接:")} --no-check-certificate'
        # self.log.info(download_order)
        # # 下载单机
        # f = self.linux_order(login, download_order)
        self.linux_order(login, 'cd home/ld;dpkg -l|grep ros-kinetic-raccoon-universal')

        # install_order = 'cd /home/ld;'


if __name__ == '__main__':
    f = Amr()
    f.amr_install([["10.3.1.174", "ld", "ld"]])
