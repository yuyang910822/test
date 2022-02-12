# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2021/7/6 16:39 
  @Auth : 于洋
  @File : log.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
-------------------------------------------------
"""

import logging
from logging.handlers import TimedRotatingFileHandler


class Log(logging.Logger):
    """
    集群日志收集器
    """

    def __init__(self, name='日志', level='DEBUG', file=None):
        super().__init__(name, level)
        # 日志格式
        fmt = logging.Formatter("%(levelname)s - %(asctime)s - %(filename)s[line:%(lineno)d] : %(message)s")
        # 日志处理器
        p = logging.StreamHandler()
        p.setLevel('ERROR')
        p.setFormatter(fmt)
        self.addHandler(p)

        # 文件处理器
        if file:
            f = TimedRotatingFileHandler(file, when='D', backupCount=7, encoding='utf-8')
            f.setLevel('DEBUG')
            f.setFormatter(fmt)
            self.addHandler(f)


if __name__ == '__main__':

    # 创建日志收集器
    # logger = logging.getLogger('root')
    #
    # # 创建日志格式
    # fmt = logging.Formatter("%(levelname)s - %(asctime)s - %(filename)s[line:%(lineno)d] : %(message)s")
    #
    # # 创建日志处理器并添加到收集器
    # s = logging.StreamHandler()
    # # s.setLevel('INFO')
    # # 创建文件处理器
    # f = logging.handlers.TimedRotatingFileHandler("1 .log", when='D', backupCount=7, encoding='utf-8')
    # f.setLevel('INFO')
    # # 设置日志格式
    # s.setFormatter(fmt)
    # f.setFormatter(fmt)
    # # 处理器添加到收集器
    # logger.addHandler(s)
    # logger.addHandler(f)
    #
    # logger.info('111')
    a =Log(file='1.txt')
    a.info('11111')