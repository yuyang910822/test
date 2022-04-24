# -*- coding: utf-8 -*- 
# @Time : 2022/4/24 16:39 
# @Author : Yu yang
# @File : count_di.py
import decimal
import jira
import jsonpath


def count_Di():
    """
    计算"报告人"为当前用户的具体项目的DI值
    :return:
    """
    username, password = input('用户名：'), input("密码：")
    search_info = input('请输入要搜索的文本：')
    calculate = {'无': 0, '致命': 10, '严重': 3, '一般': 1, '建议': 0.1}
    calculate_result = 0
    data = []
    j = jira.JIRA(server="https://issue.forwardx.ai", basic_auth=(username, password))
    # 循环筛选条件
    for issue in j.search_issues(f'reporter in (currentUser()) AND text ~ {search_info} ORDER BY status ASC, updated DESC'):
        issues = j.issue(issue)

        # 获取对应问题单的状态
        if str(issues.fields.status) == '修改实施':
            # print(issues.key, issues.fields.status)
            # 获取对应状态的严重程度
            info = jsonpath.jsonpath(issues.raw, '$..customfield_10733')[0]['value']
            title = jsonpath.jsonpath(issues.raw,'$..summary')[0]

            print(issues.key, title, info)
            data.append(info)

    for k, v in calculate.items():
        # 统计严重类型*对应数值进行相加
        calculate_result += (decimal.Decimal(str(data.count(k))) * decimal.Decimal(str(v)))

    print(f'\n\n参考上述遗留修改实施的问题，计算DI值为：{calculate_result}')


if __name__ == '__main__':
    count_Di()
