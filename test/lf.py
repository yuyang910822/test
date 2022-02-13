# -*- coding: utf-8 -*- 
# @Time : 2022/2/11 15:58 
# @Author : Yu yang
# @File : lf.py
import time

import jsonpath

from core.core_business import Business_ability


class Lf(Business_ability):
    """利丰流程自动化"""

    l = Business_ability(db='mysql', file='lifeng.log')

    token = jsonpath.jsonpath(l.http_request([
        'http://gateway.lifeng.test.be.hwc.forwardx.com/base-server/auth/login',
        {"userName": "lifeng_admin", "password": "MtLzAXpnvLmGadTE8tUaEU9i09tBTuT3AL6WUyMyVmhedRv1PZ9N+jZvDYoVZ44"
                                                 "/P2sJnj6yvZofCasiWrB8bOKPX5ylhSo7qFJMy5egUtWHAr4LUzP5JFFVkKbnjc3yf2+V"
                                                 "+BN/v0Qlp84t54/pAs31MyTrxQocCgiLbDjfe"
                                                 "/iRwsMBEvXHE2gD0iyqeFA85VC1HdcBlOAUa2qxuvTFZ5mnAt"
                                                 "/pUx2QLm3JzJZ3ujyxbZcPBEA8u/f1br5EV43b0fqhv2"
                                                 "+qCxahsbnQnhZDqbUe838iao3EjzAKY2O3c0VNyoZ1x3r1qipzJbCLzj829iYkSeMRRhgPHm1jarLkiw=="},
        {"Content-Type": "application/json",
         "deviceType": "1"}
    ]), "$..token")[0]
    headers = {"Content-Type": "application/json", "deviceType": "3", 'token': token}

    ip = "http://gateway.lifeng.test.be.hwc.forwardx.com/"

    #   {"taskId":1639645,"userName":"admin","userId":"1"}

    def depart(self):
        """上箱点出发"""
        # 获取未出发AMR的taskId
        data = self.execute_sql(
            "select t.id from test_lifeng_rpm.t_robot_task t where status = 200 and biz_type = "
            "'PICK_LOADING' and exists (select 1 from test_lifeng_rpm.t_robot_task_detail detail where detail."
            "task_id = t.id and detail.biz_type ='PICK_LOADING' and detail.arrival_time is not null and detail.l"
            "eave_time is null )", fetch=False)
        self.log.error(f'待出发AMR:{data}')

        depart_data = [''.join([self.ip, 'rpm-server/picking/page/loading/finish']),
                       {"taskId": 1639645, "userName": "admin", "userId": "1"},
                       self.headers, ]

        if data is not None:
            if len(data) >= 0:
                for i in data:
                    depart_data[1]['taskId'] = str(i[0])
                    time.sleep(5)
                    # 调接口出发
                    r = self.http_request(depart_data)
                    self.log.error(f'depart{r}')

    def theBox(self):
        """绑定容器"""
        # 查询待绑定箱子的AMR
        times = str(time.time() * 1000)
        data = self.execute_sql(
            "select t.id from test_lifeng_rpm.t_robot_task t where status = 200 and biz_type = "
            "'PICK_LOADING' and exists (select 1 from test_lifeng_rpm.t_robot_task_detail detail where detail."
            "task_id = t.id and detail.biz_type ='PICK_LOADING' and detail.arrival_time is not null and detail.l"
            "eave_time is null )", fetch=False)
        self.log.error(f'待上箱AMR:{data}')

        theBox_data = [''.join([self.ip, 'rpm-server/picking/page/loading/bindSowWallContainer']),
                       {"containerCode": "12345688888", "pickingId": "6430", "userId": 3341, "userName": "lifeng01"},
                       self.headers]

        if data is not None:
            if len(data) >= 0:
                theBox_data[1]["containerCode"] = times
                theBox_data[1]["pickingId"] = "data"
                theBox_data[1]["userId"] = "data"

                for i in data:
                    time.sleep(5)
                    # 调接口出发
                    r = self.http_request(theBox_data)
                    self.log.error(f'theBox{r}')

    def sortLattice(self):
        """获取分拣格口"""
        data = self.execute_sql(
            "select t.id from test_lifeng_rpm.t_robot_task t where status = 200 and biz_type = "
            "'PICK_LOADING' and exists (select 1 from test_lifeng_rpm.t_robot_task_detail detail where detail."
            "task_id = t.id and detail.biz_type ='PICK_LOADING' and detail.arrival_time is not null and detail.l"
            "eave_time is null )", fetch=False)
        self.log.error(f'待分格口AMR:{data}')

        sortLattice_data = [''.join([self.ip, 'rpm-server/picking/page/pick/sortLattice']),
                            {"pickedQty": "1", "pickingDetailId": "21707"},
                            self.headers]

        if data is not None:
            if len(data) >= 0:
                sortLattice_data[1]["pickedQty"] = data
                sortLattice_data[1]["pickingDetailId"] = data

                for i in data:
                    time.sleep(5)
                    # 调接口出发
                    r = self.http_request(sortLattice_data)
                    self.log.error(f'sortLattice结果{r}')

    def picking(self):
        """拣货完成"""
        # 待拣货
        data = self.execute_sql(
            "select t.id from test_lifeng_rpm.t_robot_task t where status = 200 and biz_type = "
            "'PICK_LOADING' and exists (select 1 from test_lifeng_rpm.t_robot_task_detail detail where detail."
            "task_id = t.id and detail.biz_type ='PICK_LOADING' and detail.arrival_time is not null and detail.l"
            "eave_time is null )", fetch=False)
        self.log.error(f'待拣货AMR:{data}')

        picking_data = [''.join([self.ip, 'rpm-server/picking/page/pick/confirm']),
                        {
                            "closeBox": False,
                            "fulledUp": False,
                            "packageTypeId": 0,
                            "fullSubOrderDetailId": [],
                            "goodsSN": [],
                            "pickedQty": "1",
                            "pickingId": 6430,
                            "robotTaskId": "1639646",
                            "pickingDetailId": 21707
                        },
                        self.headers]

        if data is not None:
            if len(data) >= 0:
                picking_data[1]["pickedQty"] = data
                picking_data[1]["pickingId"] = data
                picking_data[1]["robotTaskId"] = data
                picking_data[1]["pickingDetailId"] = data
                for i in data:
                    time.sleep(5)
                    # 调接口出发
                    r = self.http_request(picking_data)
                    self.log.error(f'出发结果{r}')


f = Lf(db='mysql', file='lifeng.log')
while True:
    f.depart()
    f.theBox()
    f.sortLattice()
    f.picking()
