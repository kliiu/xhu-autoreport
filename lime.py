# -*- coding: UTF-8 -*-
import time
from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from apscheduler.schedulers.blocking import BlockingScheduler
#import numpy as np
#import pandas as pd
from selenium.webdriver.support.ui import Select
import yagmail
import datetime
from selenium.webdriver.common.action_chains import ActionChains
import os
import re
from aip import AipOcr
from PIL import Image
from selenium.webdriver.support.ui import Select
import selenium.webdriver.support.ui as ui
import threading

class Student(object):
    def __init__(self,id,name,password,email):
        self.id=id
        self.name=name
        self.password=password
        self.email=email
    def sendMail(self,content):
        yag = yagmail.SMTP("发件邮箱", "授权码", 'smtp.126.com')
        yag.send(self.email, "打卡提醒", content)
    
    
    # 截图方法
    def code_jt(self,browser,loginImage,codeImage):
        # (1)登录页面截图
        browser.save_screenshot(loginImage)  # 可以修改保存地址
        # (2)图片4个点的坐标位置
        image = Image.open(loginImage)
        width,height=image.size
        left = width/4*3  # 图片最左边的x坐标
        top = 0# 最上面y坐标
        right = width # 右边点的x坐标
        down = height/2# 最下面的y坐标
        print(left,top,right,down) #打印四个角的横纵坐标
        
        # (3)将图片验证码截取e
        
        code_image = image.crop((left,top,right,down))
        code_image.save(codeImage)  # 截取的验证码图片保存为新的文件
    def get_file_content(self,filePath):
        # 读取图片
        with open(filePath, 'rb') as fp:
            return fp.read()

    #调用百度云文字识别验证码
    def bd_img(self,browser,loginImage,codeImage,i):
        '''
        百度云 通用文字识别 5000次/天 免费
        https://console.bce.baidu.com/
        '''
        image = self.get_file_content(codeImage)
        """ 调用baidu通用文字识别, 图片参数为本地图片 """
        # results = client.general(image)["words_result"]  # 还可以使用身份证驾驶证模板，直接得到字典对应所需字段
        """ 调用通用文字识别（高精度版） """
        # {'log_id': 4411569300744191453, 'words_result_num': 1, 'words_result': [{'words': ' Y7Y.: 4'}]}
        
        #注册后并领取额度获取
        APP_ID = 'xxxx'
        API_KEY = 'xxxxx'
        SECRET_KEY = 'xxx'
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        results = client.basicAccurate(image)

        # print(results)
        for result in results["words_result"]:
            text = result["words"]
            text = text.strip()
            text=text.replace(' ','')
            if re.match("^[a-zA-Z0-9]*$", text):
                print("正确："+text)
                browser.find_element_by_xpath(".//*[@id='app']/div/div[3]/div[7]/div/div/div/div/input").send_keys(text)
                # 提交按钮查看按钮元素，click模拟点击提交
                #browser.find_element_by_name('loginsubmit').click()
                time.sleep(5)  # 等待5秒，等待网页加载完成

                # 实现登录点击签到功能
                links = browser.find_element_by_xpath(".//*[@id='app']/div/div[3]/div[8]/button")
                links.click()
            else:
                print("错误：" + text)
                # 识别度不高，所以我们重复刷新验码 click模拟点击刷新验证码
                sleep(1)
                browser.find_element_by_xpath(".//*[@id='app']/div/div[3]/div[7]/div/img").click()
                if i > 30:
                    print('验证码获取失败')
                    exit(1)
                else:
                    i += 1
                    sleep(2)
                    self.code_jt(browser,loginImage,codeImage)
                    sleep(1)
                    self.bd_img(browser,loginImage,codeImage,i)

    #定位截图验证码         
    def verifycode(self,driver):
        i = 0
        # 获取项目目录
        path = os.path.abspath(os.path.dirname(__file__))
      
        loginImage = path + "/login.png"  # 登录页面截图
        codeImage = path + "/code.png"  # 定位验证码截图
        

        self.code_jt(driver,loginImage,codeImage)
        self.bd_img(driver,loginImage,codeImage,i)

    #模拟点击表单
    def submit_form(self):
       
            driver = webdriver.Chrome()
            driver.maximize_window()
            
            #打卡网站
            driver.get('https://wxyqfk.zhxy.net/?yxdm=10623#/login')
            #点击+填入信息
            #sleep(1)
            elements=driver.find_elements_by_css_selector('input')#定位输入框，返回列表（由于没有id和name,使用css selector）
            
            elements[0].send_keys(self.id)#填入学号
            elements[1].send_keys(self.name)#填入姓名
            driver.find_element_by_css_selector("[type='password']").send_keys(self.password)#填入密码
            driver.find_element_by_css_selector('button').click()#点击登录
            sleep(1)
            driver.find_element_by_css_selector('button').click()#点击确认(提示清理微信缓存)
            sleep(1)
            driver.find_element_by_css_selector("[src='/static/img/self_diagnosis_icon.2864a514.png']").click()
            sleep(2)
            try:
                if(driver.find_element_by_class_name('already-title')):
                        print("已打卡")
                        driver.__exit__()
                        return 0

            except(selenium.common.exceptions.NoSuchElementException):
                print('Unable to locate element')
            
            #sleep(1)
            driver.find_element_by_css_selector('button').click()#去填报
            #当无法自动获取定位时可打开位置选择
            #sleep(18)
            #选择省
            #ActionChains(driver).move_to_element(driver.find_element_by_xpath(".//*[@id='app']/div/div[5]/div/div[2]/div[1]/ul/li[24]")).click().perform() # 鼠标左键点击， 1920为x坐标， 1030为y坐标
            #sleep(1)
            #选择市
            #ActionChains(driver).move_to_element(driver.find_element_by_xpath(".//*[@id='app']/div/div[5]/div/div[2]/div[2]/ul/li[2]")).click().perform() # 鼠标左键点击， 1920为x坐标， 1030为y坐标
            #sleep(1)
            #选择区
            #ActionChains(driver).move_to_element(driver.find_element_by_xpath(".//*[@id='app']/div/div[5]/div/div[2]/div[3]/ul/li[12]")).click().perform() # 鼠标左键点击， 1920为x坐标， 1030为y坐标
            #sleep(1)
            #driver.find_element_by_class_name('van-picker__confirm').click()#确认
            sleep(1)
            driver.find_element_by_css_selector("[for='a_10_0']").click()
            driver.find_element_by_css_selector("[for='a_11_0']").click()
            driver.find_element_by_css_selector("[for='a_12_0']").click()
            driver.find_element_by_css_selector("[for='a_14_0']").click()
            driver.find_element_by_css_selector("[for='a_15_0']").click()

            
            js = 'var q=document.documentElement.scrollTop=10000'
            driver.execute_script(js)
            sleep(1)
            self.verifycode(driver)

            
            sleep(1)
            #邮件提醒
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if(driver.find_element_by_class_name('already-title')):
                self.sendMail(nowTime+"\n打卡成功")
                mark= 0
            else:
                mark=-1
            
            if mark==0:
                driver.__exit__()
                print('打卡成功')
                return 0
            else:
                self.submit_form()
       

if __name__ == "__main__":#__name__ 是当前模块名，当模块被直接运行时模块名为 __main__ 。当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行。

    # 请输入(学号 ，姓名，密码, 邮箱)
    student1=Student('学号','姓名','密码','接收通知的邮箱')
    students=[student1]

    for student in students:
        a=1
        while(a!=0):
            try:
                a=student.submit_form()
            except Exception as e:
                print(e)
                
                


    
    
