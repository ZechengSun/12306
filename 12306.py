from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from base64 import b64decode
from bs4 import BeautifulSoup

import requests
import re


class CrackSlider():
    """
    通过浏览器截图，识别验证码中缺口位置，获取需要滑动距离，并模仿人类行为破解滑动验证码
    """
    def __init__(self,url):
        self.url=url
        self.driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver")
        self.wait = WebDriverWait(self.driver, 60)
        self.zoom = 1
        self.driver.get(self.url)
        self.email = 'test@test.com'
        self.pasword = '123456'
        self.target = 'target.jpg'


        #self.driver.maximize_window()

    # 寻找按钮
    def get_geetest_button(self):
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-hd-account'))).click()
        #EC.element_to_be_clickable((By.ID, 'loginname')).send_keys(self.email)
        #EC.element_to_be_clickable((By.ID, 'nloginpwd')).send_keys(self.pasword)
        self.driver.find_element_by_id("J-userName").send_keys(self.email)
        self.driver.find_element_by_id("J-password").send_keys(self.pasword)

    def get_pic(self):
        data = self.driver.page_source
        # 构建beautifulsoup实例
        soup = BeautifulSoup(data, 'lxml')
        img_str = soup.find(class_="imgCode")
        img_str=img_str.get('src')
        img_str = img_str.split(",")[-1]  # 删除前面的 “data:image/jpeg;base64,”
        img_data = b64decode(img_str)  # b64decode 解码
        with open('./target.jpg', 'wb') as fout:
            fout.write(img_data)
            fout.close()

    def ai_get(self):

        files = {'pic_xxfile': open('./target.jpg', 'rb')}
        r = requests.post("http://littlebigluo.qicp.net:47720/", files=files)
        text = r.text
        text = re.search('<B>(.*)</B>', text).group()  # 寻找标签
        text = re.compile(r'\d+').findall(text)  # re.findall遍历匹配，可以获取字符串中所有匹配的字符串，返回一个列表。
        print(text)
        return text

    def actions(self,num):
        write = self.driver.find_element_by_xpath('//img [@id="J-loginImg"]')
        action = ActionChains(self.driver)
        for i in num:
            if   i=="1":
                action.move_to_element(write).perform()
                action.move_by_offset(-100, -20).click().perform()
            elif i=="2":
                action.move_to_element(write).perform()
                action.move_by_offset(-30, -20).click().perform()
            elif i=="3":
                action.move_to_element(write).perform()
                action.move_by_offset(40, -20).click().perform()
            elif i=="4":
                action.move_to_element(write).perform()
                action.move_by_offset(110, -20).click().perform()
            elif i=="5":
                action.move_to_element(write).perform()
                action.move_by_offset(-100, 60).click().perform()
            elif i=="6":
                action.move_to_element(write).perform()
                action.move_by_offset(-30, 60).click().perform()
            elif i=="7":
                action.move_to_element(write).perform()
                action.move_by_offset(40, 60).click().perform()
            elif i=="8":
                action.move_to_element(write).perform()
                action.move_by_offset(110, 60).click().perform()


if __name__ == '__main__':
    cs = CrackSlider(url='https://kyfw.12306.cn')
    cs.get_geetest_button()

    cs.get_pic()
    cs.actions(cs.ai_get())


