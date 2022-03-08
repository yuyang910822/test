import random
import time


import requests

from common.mysql import Mysql
from common.readYaml import readYaml
from common.log import Log


class Business_ability(Mysql, Log):
    """基础能力类"""

    def __init__(self, db=None, file=None):
        self.data = readYaml('../config/url_data.yaml')
        if db is not None:
            super().__init__(db)
        self.log = Log(file=file)

    def http_request(self,loc):
        """
        接口调用封装
        :param loc: 接口数据list
        :return: http请求报文
        """
        url, body, header = loc
        r = requests.request('post', url, headers=header, json=body)
        self.log.info(f'{str(url).split("/")[-1]}入参:{r.request.body}')
        self.log.info(f'{str(url).split("/")[-1]}请求体:{r.request.headers}')
        self.log.info(f'{str(url).split("/")[-1]}出参:{r.json()}')
        return r.json()

    def re(self, data):
        """
        None不影响请求结果，达到通用场景的接口调用
        :param data:
        :return:
        """
        method = data.get("method")
        url = data.get("url")
        header = data.get("header")
        json = data.get("json")

        r = requests.request(url=url, method=method, headers=header, json=json)

        self.log.info(f'{str(url).split("/")[-1]}入参:{r.request.body}')
        self.log.info(f'{str(url).split("/")[-1]}请求体:{r.request.headers}')


        return r

    def getRobotList(self):
        """
        获取机器人列表详情
        :return:
        """
        data = self.data['getRobotList']
        r = self.http_request(data)
        self.log.info('获取机器人列表详情信息:{}'.format(r))
        return r

    def getListWithPage(self):
        data = self.data['getListWithPage']
        r = self.http_request(data)
        for i in r['result']['items']:
            print(i)

    def groptask(self):

        list = ["3CA011", "3CA251", "3CE011", "3CE251", "3CG011", "3CG251", "3CI011", "3CI251", "3CK011", "3CK251", "3CM011", "3CM251", "3DA011", "3DA251", "3DC011", "3DC251", "3DE011", "3DE251", "3DG011", "3DG251", "3DI011", "3DI251", "3DK011", "3DK251", "3DM011", "3DM251", "3DO011", "3DO251", "3CB011", "3CB251", "3CF011", "3CF251", "3CH011", "3CH251", "3CJ011", "3CJ251", "3CL011", "3CL251", "3CN011", "3CN251", "3DB011", "3DB251", "3DD011", "3DD251", "3DF011", "3DF251", "3DH011", "3DH251", "3DJ011", "3DJ251", "3DL011", "3DL251", "3DN011", "3DN251", "3DP011", "3DP251", "3BE011", "3FM311", "3FK311", "3FK011", "3FG011", "3FG311", "3FE011", "3FE311", "3FC011", "3FC311", "3FA011", "3FI011", "3FI311", "3FA311", "3EA011", "3EA311", "3EC011", "3EO011", "3EC311", "3EC211", "3EE011", "3EE211", "3EO311", "3EE411", "3EE741", "3EO611", "3EG011", "3EM011", "3EM221", "3EM421", "3FN311", "3FN131", "3EM741", "3FJ022", "3FH022", "3FJ262", "3FH262", "3FF022", "3FF262", "3EK011", "3FD022", "3FD262", "3EG211", "3EK221", "3EG411", "3FB262", "3FB022", "3EK421", "3EK741", "3EP262", "3EP022", "3EI011", "3EG741", "3EN252", "3EN012", "3EI261", "3EI421", "3EB022", "3EI741", "3EL252", "3EL012", "3EB572", "3ED022", "3EJ252", "3EJ012", "3ED252", "3EF011", "3EF251", "3EH011", "3EH251", "3BA011", "3AK011", "3AE011", "3AI011", "3AG011", "3AC011", "3AA011", "3BC011", "3GC011", "3HC011", "3GE011", "3HA011", "3GG011", "3HE011", "3HG011", "3HJ011", "3GA011"]
        for j in range(1, 1):
            request_json = []
            for k in range(1, 10):
                a2 = random.randint(1, 142)
                if list[a2][0:2] != '3A' or list[a2][0:2] != '3B':
                    request_json.append(list[a2])
            time.sleep(5)
            task_id = time.time()
            request_json.insert(0,'3FF022')
            j1 = {"taskNo": "1637989596", "priority": 1, "cutOffTime": "1637989596", "taskType": 1, "splitType": 1,
                      "tagType": 2, "navType": 1, "attachInfo": None, "mapId": "39ec2b22-914e-48e0-b87e-68b76f59035e",
                      "detailList": ["3CE011"]}
            j1['detailList'] = request_json
            j1['taskNo'] = task_id
            f = requests.request('POST',
                                     url="http://10.74.51.251:8082/rpm-server/jd/picking/receivePicking",
                                     headers={'Content-Type': 'application/json'},
                                     json=j1)
            print(f.json())





if __name__ == '__main__':
    a = Business_ability("kk_mysql")
