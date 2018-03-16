import sys
import configparser
from selenium import webdriver
from lagou import Lagou
import os

sys.path.append(r'C:/Users/willd/Desktop/lagou_selenium')
cf = configparser.ConfigParser()
cf.read("setting.cfg")

driverPath = cf.get("driver", "driverPath").strip().replace("\'", "").replace(r"\n", "")
imgPath = cf.get("driver", "imgPath").strip().replace("\'", "").replace(r"\n", "")


class MyDriver(object):
    def __init__(self):
        self.imgPath = imgPath
        self.driverPath = driverPath
        # self.driver = webdriver.PhantomJS()
        # abspath = os.path.abspath(r"C:\Program Files\Mozilla Firefox\geckodriver.exe")
        self.driver = webdriver.Firefox()
        self.myweb = Lagou(self.driver)

    def setUp(self, url):
        self.driver.get(url)

        # 本类变量处理

    def setImgPath(self, imgPath):
        self.imgPath = imgPath

    def setDriverPath(self, driverPath):
        self.driverPath = driverPath

    def getImgPath(self):
        return self.imgPath

    def getDriverPath(self):
        return self.driverPath

    def getDriver(self):
        return self.driver

        # driver 相关操作

    def setOptions(self):
        self.driver.maximize_window()
        # self.driver.set_window_size(宽，高)

    def saveScreenshot(self):
        self.driver.get_screenshot_as_file(imgPath)

    def quitDriver(self):
        self.driver.quit()

        # web 通用函数登录操作

    def setUserPwd(self, username, password):
        self.myweb.setUsername(username)
        self.myweb.setPassword(password)

    def doSubmit(self):
        self.myweb.doSubmit()

    def getLoginErrMsg(self):
        return self.myweb.getLoginErrMsg()

        # web 拉钩其他操作

    def doFirstSearch(self, keyword):
        self.myweb.firstSearch(keyword)
        self.myweb.firstSearchClick()

    def doDetailSearch(self, keyword, city, workyear, education, financestage, industryfield, monthsalary):
        self.myweb.detailSearch(keyword, city, workyear, education, financestage, industryfield, monthsalary)

    def saveDate(self):
        self.myweb.saveDate()