import time
from mssql import MSSQL


class Lagou(object):
    def __init__(self, driver):
        self.mssql = MSSQL()
        self.driver = driver
        # self.taltalpage = 0

    # 登录
    def setUsername(self, username):
        return self.driver.find_element_by_xpath("//input[@placeholder='请输入常用手机号/邮箱']").send_keys(username)

    def setPassword(self, password):
        return self.driver.find_element_by_xpath("//input[@placeholder='请输入密码']").send_keys(password)

    def doSubmit(self):
        return self.driver.find_element_by_xpath("//form[@class='active']/div[5]/input[@type='submit']").click()

    def getLoginErrMsg(self):
        return self.driver.find_element_by_class_name('input_tips').text.strip()


        # 首页搜索,条件少

    def firstSearch(self, keyword):
        return self.driver.find_element_by_id('search_input').send_keys(keyword)

    def firstSearchClick(self):
        return self.driver.find_element_by_id('search_button').click()

        # 详细搜索

    def detailSearch(self, keyword, city, workyear, education, financestage, industryfield, monthsalary):
        keyword = keyword.strip()

        if len(city) == 0:
            city = ""
        else:
            city = "&city=%s" % city.strip()

        if len(workyear) == 0:
            workyear = ""
        else:
            workyear = "&gj=%s" % workyear.strip()

        if len(education) == 0:
            education = ""
        else:
            education = "&xl=%s" % education.strip()

        if len(financestage) == 0:
            financestage = ""
        else:
            financestage = "&jd=%s" % financestage.strip()

        if len(industryfield) == 0:
            industryfield = ""
        else:
            industryfield = "&hy=%s" % industryfield.strip()

        if len(monthsalary) == 0:
            monthsalary = ""
        else:
            monthsalary = "&yx=%s" % monthsalary.strip()

            # 选择标签比较麻烦，直接拼接网站访问
        url = "https://www.lagou.com/jobs/list_%s?px=default" % keyword
        url = url + "%s%s%s%s%s%s" % (workyear, education, financestage, industryfield, monthsalary, city)
        self.driver.get(url)


        # 总页数

    def getTaltalPage(self):
        num = self.driver.find_element_by_xpath("//div[@class='page-number']/span[2]").text.strip()
        if len(num) == 0:
            num = 0
            # self.taltalpage = int(num)
        print("总页数：%s " % num)
        return int(num)

        # 点击下一页

    def NextPage(self):
        self.driver.find_element_by_xpath("//span[@class='pager_next ']").click()


        # 保存所有页数据

    def saveDate(self):
        taltalpage = self.getTaltalPage()
        currentpage = 1
        if taltalpage != 0:
            while currentpage <= taltalpage:
                time.sleep(3)  # 等待页面加载
                print(">> 第 %s 页数据处理中…………………………………………" % currentpage)
                print(self.driver.current_url)
                self.saveOnePageDate()  # 保存当页数据
                self.NextPage()  # 点击下一页
                currentpage = currentpage + 1
        else:
            pass


            # 保存一页数据

    def saveOnePageDate(self):
        index = 0
        while index <= 14:
            xpath = "//li[@data-index='%s']" % index
            print(">> 第 %s 条" % index)
            self.saveliDate(xpath)
            index = index + 1


            # 保存 li 到数据库

    def saveliDate(self, xpath):
        positi = self.driver.find_element_by_xpath(xpath + "/div[1]/div[1]/div[1]/a/h3").text.strip()
        citydist = self.driver.find_element_by_xpath(xpath + "/div[1]/div[1]/div[1]/a/span/em").text.strip()
        salary = self.driver.find_element_by_xpath(xpath + "/div[1]/div[1]/div[2]/div/span").text.strip()
        wy_edu = self.driver.find_element_by_xpath(xpath + "/div[1]/div[1]/div[2]/div").text.strip()
        company = self.driver.find_element_by_xpath(xpath + "/div[1]/div[2]/div[1]/a").text.strip()
        fina_ind = self.driver.find_element_by_xpath(xpath + "/div[1]/div[2]/div[2]").text.strip()
        firsttype = self.driver.find_element_by_xpath(xpath + "/div[2]/div[1]").text.strip()
        lables = self.driver.find_element_by_xpath(xpath + "/div[2]/div[2]").text.strip()

        companyfullname = company
        positionname = positi
        salary = salary  # ((wy_edu.replace(" ", "/")).split('/')[0]).strip()
        workyear = ((wy_edu.replace(" ", "/")).split('/')[1]).strip()
        education = ((wy_edu.replace(" ", "/")).split('/')[4]).strip()
        city = "昆明"
        district = ((citydist + '·' + citydist).split('·')[1]).strip()
        industryfield = (fina_ind.split('/')[0]).strip()
        financestage = (fina_ind.split('/')[1]).strip()
        firsttype = firsttype.replace(" ", ",").strip()
        positionlables = lables.replace("“", "").replace("”", "").strip()

        sql = """INSERT INTO seleniumlagou( companyfullname , positionname, salary, workyear,  
            education,city,district, industryfield, financestage, firsttype, positionlables)  
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % \
              (companyfullname, positionname, salary, workyear, education, city,
               district, industryfield, financestage, firsttype, positionlables)

        self.mssql.ExecNonQuery(sql)


        # print("companyfullname = " + companyfullname)
        # print("positionname = " + positionname)
        # print("salary = " + salary)
        # print("workyear = " + workyear)
        # print("education = " + education)
        # print("city = " + city)
        # print("district = " + district)
        # print("industryfield = " + industryfield)
        # print("financestage = " + financestage)
        # print("firsttype = " + firsttype)
        # print("positionlables = " + positionlables)
