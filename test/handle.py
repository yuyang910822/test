import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By

d = webdriver.Chrome()
d.get('http://10.74.51.251:8090/#/exceptMonitor')
print('请先进入异常监控界面')
a = input('输入输入任意键开始查找异常！')
while True:
    """
    死循环查找异常
    """
    try:
        d.find_element(By.XPATH,  "//span[text()='处理']").click()
        time.sleep(2)
    except NoSuchElementException:
        time.sleep(2)
        continue
    else:
        try:
            print('找到异常')
            d.find_element(By.XPATH,  '//*[@id="app"]/div/section/main/div[2]/div/div[2]/form/div[4]/div/div[1]/input').clear()
            time.sleep(2)
            print('清空输入')
            d.find_element(By.XPATH, '//*[@id="app"]/div/section/main/div[2]/div/div[2]/form/div[4]/div/div[1]/input').send_keys(268)
            time.sleep(2)
            print('输入编号')
        except NoSuchElementException:
            print('没有找到输入栏')
            time.sleep(2)
        except ElementNotInteractableException:
            d.find_element(By.XPATH, "//span[text()=' 处理 ']").click()
        finally:
            d.find_element(By.XPATH, "//span[text()=' 处理 ']").click()
            print('处理完成')
