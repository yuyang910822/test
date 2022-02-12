# -*- coding: utf-8 -*- 
# @Time : 2021/12/28 16:52 
# @Author : Yu yang
# @File : setContainerCode.py
from common.mysql import Mysql


def setContainerCode(start, end, jd_code, mysqlaAddress):
    """
    二维码编号和容器编号绑定，容器后三位与二维码保持一致
    :param start: 起始编号
    :param end:  结束编号
    :param jd_code: 去除后三位的容器编号
    :param mysqlaAddress: 连接的数据库名称 在config-mysql.yaml里
    :return:
    """
    for i in range(start, end + 1):
        sql = "INSERT into test_jd_cluster_system.t_container_code VALUES({},{},{}{})".format(i, i, jd_code, i)
        Mysql(mysqlaAddress).execute_sql(sql)


if __name__ == '__main__':
    setContainerCode(100, 200, '0000056780000', 'mysql')
