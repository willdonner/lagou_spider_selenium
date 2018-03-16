import sys
# import pymssql
import pymysql

import configparser

sys.path.append(r'C:\Users/willd/Desktop/lagou_selenium')
cf = configparser.ConfigParser()
cf.read("setting.cfg")

MSSQL_HOST = cf.get("mssql", "MSSQL_HOST").strip().replace("\'", "").replace(r"\n", "")
MSSQL_USER = cf.get("mssql", "MSSQL_USER").strip().replace("\'", "").replace(r"\n", "")
MSSQL_PASSWD = cf.get("mssql", "MSSQL_PASSWD").strip().replace("\'", "").replace(r"\n", "")
MSSQL_DBNAME = cf.get("mssql", "MSSQL_DBNAME").strip().replace("\'", "").replace(r"\n", "")


class MSSQL(object):
    def __init__(self):
        self.host = MSSQL_HOST
        self.user = MSSQL_USER
        self.pwd = MSSQL_PASSWD
        self.db = MSSQL_DBNAME

        self._conn = self.GetConnect()
        if (self._conn):
            self._cur = self._conn.cursor()

            # 连接数据库

    def GetConnect(self):
        conn = False
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.pwd,
                database=self.db,
                charset="utf8"
            )
        except Exception as err:
            print("连接数据库失败, %s" % err)
        else:
            return conn

            # 执行查询

    def ExecQuery(self, sql):
        res = ""
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
        except Exception as err:
            print("查询失败, %s" % err)
        else:
            return res


            # 执行非查询类语句

    def ExecNonQuery(self, sql):
        flag = False
        try:
            self._cur.execute(sql)
            self._conn.commit()
            flag = True
        except Exception as err:
            flag = False
            self._conn.rollback()
            print("执行失败, %s" % err)
        else:
            return flag


            # 获取连接信息

    def GetConnectInfo(self):
        print("连接信息：")
        print("服务器:%s , 用户名:%s , 数据库:%s " % (self.host, self.user, self.db))


        # 关闭数据库连接

    def Close(self):
        if (self._conn):
            try:
                if (type(self._cur) == 'object'):
                    self._cur.close()
                if (type(self._conn) == 'object'):
                    self._conn.close()
            except:
                raise ("关闭异常, %s,%s" % (type(self._cur), type(self._conn)))