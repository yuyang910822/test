import time
from core.core_business import Business_ability


class PickStationFinish(Business_ability):
    """拣货过程自动确认拣货 """

    def automatic_confirmation(self):
        """
        通过数据库进行筛选到达拣货点AMR并自动确认
        :return:
        """
        # global r
        time.sleep(3)
        status = self.execute_sql("select t1.robot_code as robotCode,t2.internal_station_name as stationName,(select "
                                  "t_wave.original_wave_no from t_wave where t_wave.id=t1.wave_id) taskNo from "
                                  "t_robot_task t1,t_robot_task_detail t2 where t1.id=t2.task_id and t1.`status`=200 "
                                  "and t2.`status`=100 and t2.arrival_time is not null", fetch=False)
        print(status)
        if len(status) >= 1:
            for i in set(status):
                if i[2][0:2] != 'OT':
                    request_data = self.data['pickStationFinish']
                    request_data[1]['robotCode'] = i[0]
                    request_data[1]['stationName'] = i[1]
                    r = self.http_request(request_data)
                    self.log.info("{},{}:{}".format(request_data[1]['robotCode'], request_data[1]['stationName'], r))
                else:
                    self.log.error('{}属于京东订单，不做自动确认处理'.format(i[2]))


if __name__ == '__main__':
    """1.修改config--url_data里面url地址
       2.新增或修改config--mysql数据库配置"""
    a = PickStationFinish('mysql', file='../log/自动确认.log')  # 入参：配置名称，日志名称
    while True:
        try:
            a.automatic_confirmation()
        except TypeError:
            continue

