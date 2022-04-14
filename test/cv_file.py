# -*- coding: utf-8 -*- 
# @Time : 2022/2/22 15:33 
# @Author : Yu yang
# @File : cv_file.py
from common.excel import DoExcel


class Excel(DoExcel):

    def __init__(self, file, sheet):
        super(Excel, self).__init__(file, sheet)


if __name__ == '__main__':

    rename = Excel(fr"{input('文件路径：')}",f"{input('标签名：')}")
    rename.workbook.save(rf"{input('文件存放路径：')}")



