# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2021/7/6 16:05 
  @Auth : 于洋
  @File : mysql.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
-------------------------------------------------
"""

import pymysql
from common.path import mysql_dir
from common.readYaml import readYaml


class Mysql:
    """数据库操作
    execute_sql ：执行sql语句

    """

    def __init__(self, db):
        """
        初始化数据库
        """
        self.config = readYaml(mysql_dir)[db]
        self.db = pymysql.connect(host=self.config['host'], user=self.config['user'],
                                  password=self.config['password'], port=self.config['port'],
                                  charset=self.config['charset'],database=self.config['database'])
        # 创建游标
        self.cursor = self.db.cursor()

    def closes(self):
        """关闭游标"""
        self.db.close()
        self.cursor.close()

    def execute_sql(self, sql, fetch=True):
        """
        执行sql返回结果
        :param sql: sql命令
        :param fetch: True:查询第一行 False：查询全部
        :return: 
        """""
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except :
            self.db.rollback()
        else:
            if fetch:
                return self.cursor.fetchone()
            else:
                return self.cursor.fetchall()


if __name__ == '__main__':
    a = Mysql('mysql')
    d = a.execute_sql("INSERT into test_jd_cluster_system.t_container_code VALUES(i,i,{}{})".format('2222222',100))
    print(d)