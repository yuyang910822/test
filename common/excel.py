import openpyxl
from openpyxl.worksheet.worksheet import Worksheet


# from common.mysql import Mysql


class DoExcel:

    def __init__(self, file_name, sheet_name):
        """
        初始化excel对象或许表数据
        :param file_name: 文件名
        :param sheet_name: 表名
        """
        self.file = file_name
        self.sheet = sheet_name
        self.workbook = openpyxl.load_workbook(self.file)
        self.sheet: Worksheet = self.workbook[self.sheet]

    def readTestData(self):
        """读取测试数据"""
        data = list(self.sheet.values)
        testData = []
        for i in data[1:]:
            value = dict(zip(data[0], i))
            if list(value.values())[0] is not None:
                testData.append(value)
        return testData

    def close(self):
        """关闭工作薄对象，释放内存"""
        self.workbook.close()

    def readUserPass(self):
        """
        读取用户&密码
        :return:
        """
        return list(self.sheet.values)

    def cv_file(self):
        """
        读取用户&密码
        :return:
        """
        return list(self.sheet.values)


if __name__ == "__main__":
    # flie = DoExcel(r"C:\Users\yuyang\Desktop\测试\测试报告\【V1.51.0利丰1.0】测试报告V1.xlsx", "测试报告")
    flie = DoExcel(r"C:\Users\yuyang\Desktop\测试\excel\利丰excel\非单品单件1个格口.xlsx", "Sheet1")
    flie.workbook.save(r"C:\Users\yuyang\Desktop\测试\excel\利丰excel\非单品单件2.xlsx")
    # for i in flie.readUserPass():
    #     for j in i:
    #         if j != None:
    #             print(j)