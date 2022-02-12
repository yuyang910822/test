import time

import jsonpath
import requests

from common.readYaml import readYaml
from core.core_business import Business_ability


class Robot(Business_ability):
    """
    封装“机器人在线管理”--操作
    """

    def getRobot_Code(self):
        """获取机器人编号"""
        return jsonpath.jsonpath(self.getRobotList(), '$..robotCode')

    def operateRobot_4(self):
        """一键释放点位状态"""
        for i in self.getRobot_Code():
            request_data = self.data["operateRobot_4"]
            request_data[1]["robotCode"] = i
            r = self.http_request()(request_data)
            self.log.info('{}:{}'.format(i, r))

    def getremainingPercent(self):
        """获取未在线及低电量AMR"""
        # 低电量
        lowBatteryCode = []
        # 未上线
        notOnlineCode = []

        for i in self.getRobotList()['result']['items']:
            # 有FTA状态
            if i['baseStatus'] is not None:
                # AMR电量小于<50
                if i['remainingPercent'] < 30.0:
                    # 不属于充电中状态
                    if i['baseStatus'] != '充电中':
                        # if i['robotCode'] not in ['9002', '9026', '9027', '9028', '9029', '9030', '9032']:
                        lowBatteryCode.append(i['robotCode'])
            else:
                # if i['robotCode'] not in ['9002', '9026', '9027', '9028', '9029', '9030', '9031']:
                notOnlineCode.append(i['robotCode'])

        print('低电量：', lowBatteryCode)
        print('未上线：', notOnlineCode)

    def operateRobot_7(self):
        """一键重新定位所有AMR"""
        for i in self.getRobot_Code():

            request_data = self.data['operateRobot_7']
            request_data[1]["robotCode"] = i
            r = self.http_request(request_data)
            self.log.info('{}:{}'.format(i, r))

    def operateRobot_6(self):
        """一键关机所有AMR"""
        for i in self.getRobot_Code():
            if i != '9045':

                request_data = self.data['operateRobot_6']
                request_data[1]["robotCode"] = i
                r = self.http_request(request_data)
                self.log.info('{}:{}'.format(i, r))

    def releaseCode(self):
        robot_code = []
        for i in self.getRobotList()['result']['items']:
            if i['ftaVersion'] != 'prod-jdn-20211201-001-new':
                robot_code.append(i["robotCode"])
        print('fta版本不对：', robot_code)

    def operateRobot_1(self):
        """一键开始工作"""
        url = 'http://10.74.51.252:8070/robotManager/operateRobot'
        headers = {'Content-Type': 'application/json'}
        start = int(input('开始号'))
        end = int(input('结束号'))
        for i in range(start, end):
            data = {"timeout": 3000, "operateType": 1, "robotCode": "9001"}
            if i < 10:
                data['robotCode'] = "900{}".format(i)
            else:
                data['robotCode'] = "90{}".format(i)
            r = requests.request('post', url, headers=headers, json=data)
            print(r.json())


if __name__ == '__main__':
    a = Robot(db='kk_mysql', file='../log/robotlog.log')
    while True:
        print('1：查询机器人电量，2：释放机器人全部点位占用, 3:所有车辆重新定位, 4:所有AMR关机, 5:查询FTA版本')
        c = int(input('请输入：'))
        if c == 1:
            a.getremainingPercent()
        if c == 2:
            a.operateRobot_4()
        if c == 3:
            a.operateRobot_7()
        if c == 4:
            a.operateRobot_6()
        if c == 5:
            a.releaseCode()
        if c == 6:
            a.operateRobot_1()




