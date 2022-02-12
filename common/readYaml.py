# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2021/7/6 16:13 
  @Auth : 于洋
  @File : readYaml.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
-------------------------------------------------
"""
import yaml

from common.path import *


def readYaml(path):
    """
    path: config下文件路径
    return：读取的yaml数据
    """
    with open(path, encoding='utf-8') as y:
        data = yaml.load(y, Loader=yaml.FullLoader)
    return data


if __name__ == '__main__':
   readYaml(url_dir)
