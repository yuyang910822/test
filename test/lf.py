# -*- coding: utf-8 -*- 
# @Time : 2022/2/11 15:58 
# @Author : Yu yang
# @File : lf.py
import time

import jsonpath

from core.core_business import Business_ability




class Lf(Business_ability):

    l =Business_ability(db='mysql', file='lifeng.log')

    token = jsonpath.jsonpath(l.http_request([
        'http://gateway.lifeng.test.be.hwc.forwardx.com/base-server/auth/login',
        {"userName":"lifeng_admin","password":"MtLzAXpnvLmGadTE8tUaEU9i09tBTuT3AL6WUyMyVmhedRv1PZ9N+jZvDYoVZ44"
                                              "/P2sJnj6yvZofCasiWrB8bOKPX5ylhSo7qFJMy5egUtWHAr4LUzP5JFFVkKbnjc3yf2+V"
                                              "+BN/v0Qlp84t54/pAs31MyTrxQocCgiLbDjfe"
                                              "/iRwsMBEvXHE2gD0iyqeFA85VC1HdcBlOAUa2qxuvTFZ5mnAt"
                                              "/pUx2QLm3JzJZ3ujyxbZcPBEA8u/f1br5EV43b0fqhv2"
                                              "+qCxahsbnQnhZDqbUe838iao3EjzAKY2O3c0VNyoZ1x3r1qipzJbCLzj829iYkSeMRRhgPHm1jarLkiw=="},
        {"Content-Type": "application/json",
         "deviceType": "1"}
    ]), "$..token")[0]
    headers = {"Content-Type": "application/json", "deviceType": "1", 'token': token}
    ip = "http://gateway.lifeng.test.be.hwc.forwardx.com/base-server/auth/login/"

    depart_data = [''.join([ip, '11']),headers]
    theBox_data = [''.join([ip, '11']),headers]
    picking_data = [''.join([ip, '11']),headers]


    def depart(self):
        """上箱点出发"""

        # 查询到达上箱点的AMR
        data = self.execute_sql(
            "select t.robot_code,t.* from test_lifeng_rpm.t_robot_task t where status = 200 and biz_type = "
            "'PICK_LOADING' and exists (select 1 from test_lifeng_rpm.t_robot_task_detail detail where detail."
            "task_id = t.id and detail.biz_type ='PICK_LOADING' and detail.arrival_time is not null and detail.l"
            "eave_time is null )")
        self.log.info(f'待出发AMR:{data}')
        if data is not None:
            if len(data) >= 0:
                for i in data:
                    self.depart_data[1]['robotcode'] = data[0]
                    time.sleep(5)
                    # 调接口出发
                    r = self.http_request(self.depart_data)
                    self.log.info(f'出发结果{r}')

    def theBox(self):
        """上箱子"""
        # 查询待绑定箱子的AMR
        times = time.time()
        data = self.execute_sql('')

        self.log.info(f'待上箱AMR:{data}')
        if data is not None:
            if len(data) >= 0:
                url = ''.join([self.ip, 'e'])
                head = {}
                json = {}
                for i in data:
                    time.sleep(5)
                    # 调接口出发
                    r = self.http_request([url, head, json])
                    self.log.info(f'出发结果{r}')

    def picking(self):
        """拣货完成"""
        # 待拣货
        data = self.execute_sql('')
        self.log.info(f'待拣货AMR:{data}')
        if data is not None:
            if len(data) >= 0:
                url = ''.join([self.ip, 'e'])
                head = {}
                json = {}
                for i in data:
                    time.sleep(5)
                    # 调接口出发
                    r = self.http_request([url, head, json])
                    self.log.info(f'出发结果{r}')


f = Lf(db='mysql', file='lifeng.log')
# while True:
#     f.depart()
print(f.token)
