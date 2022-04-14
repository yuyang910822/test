# -*- coding: utf-8 -*- 
# @Time : 2022/3/18 16:51 
# @Author : Yu yang
# @File : getversion.py
import jsonpath
import requests


def erms_version():
    """
    获取erms版本信息
    :return: 各服务版本号
    """
    url = f'http://{input("请输入ERMS地址IP:")}:8080/api/versions'
    data = requests.get(url).json()
    for name, version in dict(zip(jsonpath.jsonpath(data, '$..name'), jsonpath.jsonpath(data, '$..version'))).items():
        print(name + ": " + version)


def rsc1_version():
    """
    获取rsc1.0版本信息
    :return: 各服务版本号
    """
    url = f'http://{input("请输入RCS1.0地址IP:")}/ops-server/info/queryAllServiceInfo'
    data = requests.get(url, headers={"token": "LD-Token_jd_admin|1649939847991u36z4sd3"}).json()
    for i in data['result']:
        print(f"{i['serviceName']}: {i['serviceVersion']}")


if __name__ == '__main__':
    rsc1_version()
