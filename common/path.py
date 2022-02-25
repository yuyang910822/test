# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2021/7/6 16:13 
  @Auth : 于洋
  @File : path.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
-------------------------------------------------
"""

import os


dirs = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

log_dir = os.path.join(dirs, r'log')

url_dir = os.path.join(dirs, r'config\url_data.yaml')

mysql_dir = os.path.join(dirs, r'config\mysql.yaml')

file_dir = os.path.join(dirs,r'file')

erms_dir= os.path.join(dirs, r'data\erms_config')