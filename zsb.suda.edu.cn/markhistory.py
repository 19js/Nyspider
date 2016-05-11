#coding:utf-8


#导入模块
import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import os

#获取招生省份
def get_provinces():
    #打开网页获取网页源码
    html=requests.get('http://zsb.suda.edu.cn/markHistory.aspx').text
    #解析网页，查找到省份，这个要结合网页源码
    table=BeautifulSoup(html,'html.parser').find('select',id='ctl00_ContentPlaceHolder1_DropDownList2').find_all('option')
    provinces={}
    #获取省份名
    for option in table:
        provinces[option.get_text()]=option.get('value')
    return provinces

#获取招生专业，分数及其他信息
def parser(year,aid,province):
    #构造url,打开网页，获取源码
    url='http://zsb.suda.edu.cn/view_markhistory.aspx?aa=%s年%s各专业录取分数一览表&aid=%s&ay=%s'%(year,province,aid,year)
    print(url)
    html=requests.get(url).text
    #解析网页，获取具体信息
    table=BeautifulSoup(html,'html.parser').find('table',id='ctl00_ContentPlaceHolder1_GridView1').find_all('tr')[1:]
    items=[]
    #遍历表格每一项，获取信息
    for tr in table:
        item=[year,province]
        for td in tr.find_all('td'):
            item.append(td.get_text().replace('\n',''))
        items.append(item)
    return items

def main():
    try:
        os.remove('data.db')
    except:
        pass
    #连接数据库
    conn=sqlite3.connect('data.db')
    #创建游标
    cursor=conn.cursor()
    #创建数据表
    cursor.execute("create table if not exists markhistory(year varchar(8),province varchar(80),professional varchar(80),length varchar(20),category varchar(20),numbers varchar(20),highest varchar(20),minimum varchar(20),average varchar(20))")
    #需要抓取的年份
    need_years=['2015','2014','2013']
    #获取招生的省份
    provinces=get_provinces()
    #获取每个省每一年的信息
    for year in need_years:
        for key in provinces:
            #获取 某年（year)某地区（province）各专业信息
            try:
                items=parser(year,provinces[key],key)
            except:
                continue
            for item in items:
                #入库
                cursor.execute('insert into markhistory(year,province,professional,length,category,numbers,highest,minimum,average) values'+str(tuple(item)))
            #提交事物，入库
            conn.commit()
            #打印完成信息
            print(year,key,'--ok')
    #关闭游标
    cursor.close()
    #关闭数据库连接
    conn.close()

main()
