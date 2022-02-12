from common.excel import DoExcel
from core.core_business import Business_ability
import decimal


class Station(DoExcel, Business_ability):
    """ 点位标注&映射&分组"""
    id = 1


    @staticmethod
    def writ_file(name):
        """
        文件进行写入
        :param name: 文件名称
        :return:
        """
        f = open("../data/{}.txt".format(name), mode="w+", encoding="utf-8")
        return f

    def set_interior_external_location(self):
        """生成停靠点映射"""
        d = self.writ_file('停靠点映射sql')
        for i in self.sheet:
            data = []
            for j in i:
                data.append(j.value)

            d.write("INSERT INTO `test_jd_rcs`.`internal_external_station_mapping`(`id`, `customerId`, "
                    "`customerName`, `workSpaceId`, `workSpaceName`, `mapId`, `mapName`, `internalStationName`, "
                    "`externalStationName`, `tmplName`, `createTime`, `modifyTime`) VALUES ({}, 71, '京东', 10, "
                    "'华南水饮仓', 1, NULL, '{}', '{}', '拣货点', '2021-09-03 01:41:41', '2021-09-03 01:41:41'); \n"
                    .format(self.id, data[-2], data[-1]))
            self.id += 1

    def set_interior_location(self, name):
        """
        生成内部点位
        :param name: 点位类型名称
        :return:
        """
        data = []
        d = self.writ_file('内部点位sql')
        for i in self.sheet:
            for j in i:
                data.append(j.value)
                break
        for l in set(data):
            d.write("INSERT INTO `test_jd_rcs`.`station_deploy`(`id`, `groupId`, `name`, `tmplName`, "
                    "`businessTypeName`, `extTmplName`, `sortNum`, `posX`, `posY`, `rotation`, `drawRulerId`, "
                    "`mapId`, `type`, `param`, `groupName`, `createTime`, `modifyTime`) VALUES ({}, 0, '{}', '{}', "
                    "NULL, NULL, 0, 2.14, -6.73, 4.71239, 0, 1, 'DEFAULT', 'Null', '', '2021-08-31 14:34:54', "
                    "'2021-08-31 06:34:55'); \n".format(self.id, l, name))
            self.id += 1

        return set(data)

    def set_staiton(self, count, name):
        """
        生成非拣货内部点数据
        :param count: 数量
        :param name: 名字
        :return:
        """
        d = self.writ_file('非拣货点sql')
        for i in range(count):
            d.write("INSERT INTO `test_jd_rcs`.`station_deploy`(`id`, `groupId`, `name`, `tmplName`, "
                    "`businessTypeName`, `extTmplName`, `sortNum`, `posX`, `posY`, `rotation`, `drawRulerId`, "
                    "`mapId`, `type`, `param`, `groupName`, `createTime`, `modifyTime`) VALUES ({}, 0, '{}-0{}', '{}', "
                    "NULL, NULL, 0, 2.14, -6.73, 4.71239, 0, 1, 'DEFAULT', 'Null', '', '2021-08-31 14:34:54', "
                    "'2021-08-31 06:34:55'); \n".format(self.id, name, i, name))
            self.id += 1

    def set_xy(self, count_x, count_y, x, y, differ_x, differ_y):
        """
        1.生成一行的X坐标\n
        2.在X的基础上生成所有行坐标\n
        :param count_x: 一行几列
        :param count_y: 一共几行
        :param x: 列
        :param y: 行
        :param differ_x:相邻列的间距
        :param differ_y: 相邻行的间距
        :return:
        """
        x = decimal.Decimal(str(x))
        y = decimal.Decimal(str(y))
        for i in range(count_x):
            x -= decimal.Decimal(str(differ_x))
            print(x)
        for j in range(count_y):
            y += decimal.Decimal(str(differ_y))
            print(y)

    def set_station_group(self, group_name, count):
        """
        点位分组
        :param count: 数量
        :param group_name: 分组名称
        :return:
        """
        if group_name == '拣货点':
            data = self.set_interior_location("拣货点")
            request_data = self.data['pickingGroup']
            for i in data:
                request_data[1]['groupName'] = i[0:3]
                request_data[1]['stationList'] = '{}-012,{}-011'.format(i[0:3], i[0:3])
                self.http_request(request_data)

        if group_name == '上箱点':
            request_data = self.data['loadingGroup']
            for i in range(1, count + 1):
                request_data[1]['groupName'] = "上箱点分组-0{}".format(i)
                request_data[1]['stationList'] = '上箱点-0{},上箱点进-0{},上箱点出-0{}'.format(i, i, i)
                self.http_request(request_data)

        if group_name == '卸箱点':
            request_data = self.data['uninstallGroup']
            for i in range(1, count + 1):
                request_data[1]['groupName'] = "卸箱点分组-30{}".format(i)
                request_data[1]['stationList'] = '卸货区03-1-0{},卸箱区进03-1-0{},卸箱区出03-1-0{}'.format(i, i, i)
                self.http_request(request_data)

        if group_name == '停车点':
            request_data = self.data['parkingGroup']
            for i in range(1, count + 1):
                request_data[1]['groupName'] = "停车点分组-0{}".format(i)
                request_data[1]['stationList'] = '停车点-0{},停车点进-0{},停车点出-0{}'.format(i, i, i)
                self.http_request(request_data)


if __name__ == '__main__':
    a = Station(r'C:\Users\yuyang\Downloads\kk需求变更--测试用例.xlsx', "Sheet0")
    a.set_interior_location('卸箱点')
