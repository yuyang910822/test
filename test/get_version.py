# -*- coding: utf-8 -*- 
# @Time : 2022/3/18 16:51 
# @Author : Yu yang
# @File : getversion.py
import jsonpath
import requests


def erms_version():
    """
    输入ip拼接erms版本号
    :return: 各服务版本号
    """
    url =f'http://{input("请输入ERMS地址IP:")}:8080/api/versions'
    data = requests.get(url).json()
    for name, version in dict(zip(jsonpath.jsonpath(data, '$..name'), jsonpath.jsonpath(data, '$..version'))).items():
        print(name+": "+version)

if __name__ == '__main__':

    erms_version()