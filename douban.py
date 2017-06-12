# -*- coding: utf-8 -*-
#豆瓣词频分析
#模块1：爬虫数据
#模块2：数据存取
#模块3：数据分析
import requests
import MySQLdb
from bs4 import BeautifulSoup as bs
import jieba
from collections import Counter
str1=''#从mysql读取数据
def getDatafromDouBan():#从豆瓣获取数据并存入mysql数据库
    ii=1
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='$$$$', port=3306)
        cur = conn.cursor()
        url = 'https://www.douban.com/group/69593/discussion?start=0'
        # 爬虫
        for i in range(0, 38676, 25):
            url1 = url + str(i)
            r = requests.get(url1)
            soup = bs(r.content, 'lxml')
            datas = soup.find_all(name='a')
            for data in datas:
                title = data.get('title')
                href = data.get('href')
                if title != None:
                    sql="insert into title1 VALUES('%d','%s','%s')"%(ii,title,href)
                    try:
                        cur.execute(sql)
                        print str(ii),' ',title, '----', href
                        ii = ii + 1
                    except Exception :
                        pass
            conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def getDatafromMysql():#从数据库读取数据
    global str1
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='$$$$$',port=3306)
        cur=conn.cursor()
        cur.execute('select * from title1')
        results=cur.fetchall()
        result=list(results)
        cur.scroll(0, mode='absolute')
        for i in result:
            str1=str1+' '+str(i[1])
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def analyseData():#分析数据
    global str1
    data = jieba.cut(str1)
    data = dict(Counter(data))
    vl=1
    strresult=''
    buyao=[' ','的','，','…','了','？','。','我','有','！','吗','在','你','想','是','去']#排除无效关键词
    for k,v in data.items():
        if v>vl:
            if k.encode('utf-8') not in buyao:
                vl=v
                strresult=k.encode('utf-8')
        #print ("%s,%d\n" % (k.encode('utf-8'),v))
    print ("%s,%d\n" % (strresult,vl))
    t=sorted(data.items(), key=lambda item: item[1], reverse=True)
    for i , j in t:
        print i,j
#getDatafromDouBan()
getDatafromMysql()
analyseData()
