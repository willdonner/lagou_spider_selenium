from selenium import webdriver
import time
browser = webdriver.Chrome()
browser.get("http://www.baidu.com")
browser.close()