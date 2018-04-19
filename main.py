import time
import unittest
from mydriver import MyDriver


class Main(unittest.TestCase):
    username = "765019300@qq.com"
    password = "5223561"
    loginUrl = 'https://passport.lagou.com/login/login.html'

    # 【登录拉钩网】
    mydriver = MyDriver()
    driver = mydriver.getDriver()
    # mydriver.setOptions()
    mydriver.setUp(loginUrl)
    mydriver.setUserPwd(username, password)
    mydriver.doSubmit()
    print("[1] " + driver.current_url)

    # 判断页面是否跳转加载，url不一样说明已跳转。
    while True:
        if loginUrl == driver.current_url:
            time.sleep(1)
            print("[-] " + driver.current_url)
            print("loading……")
            continue
        else:
            break

    print("[2] " + driver.current_url)
    # mydriver.saveScreenshot()

    # 【按条件搜索】
    # 首页筛选条件太少，任意输入直接点击搜索将跳转详细搜索列表
    #mydriver.doFirstSearch("hzc")
    print("[3] " + driver.current_url)

    # 详细搜索页面，格式：(岗位,工作城市,工作经验,学历要求,融资阶段,行业领域,月薪范围)
    # mydriver.doDetailSearch("dba","深圳","3-5年","本科","未融资","移动互联网","15k-25k")
    mydriver.doDetailSearch("java", "深圳", "", "", "", "", "")

    print("[4] " + driver.current_url)

    mydriver.saveDate()

    print("done!")


if __name__ == "__main__":
    Main()