# -*- coding: utf-8 -*- 
# @Time : 2022/2/22 15:33 
# @Author : Yu yang
# @File : cv_file.py
from common.excel import DoExcel


class Excel(DoExcel):

    def __init__(self, file, sheet):
        super(Excel, self).__init__(file, sheet)



if __name__ == '__main__':
    rename = Excel(r"C:\Users\yuyang\Desktop\恒艺腾6个订单11.xlsx","Sheet1")
    rename.workbook.save(r"C:\Users\yuyang\Desktop\恒艺腾6个订单1111.xlsx")



