#coding:utf-8

import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import re


#获取招生省份
def get_provinces():
    #打开网页获取网页源码
    html=requests.get('http://zsb.suda.edu.cn/markHistory.aspx').text
    #解析网页，查找到省份，这个要结合网页源码
    table=BeautifulSoup(html,'html.parser').find('select',id='ctl00_ContentPlaceHolder1_DropDownList2').find_all('option')
    provinces=[]
    #获取省份名
    for option in table:
        provinces.append(option.get_text())
    return provinces

def get_school():
    #打开网页获取网页源码
    html=requests.get('http://zsb.suda.edu.cn/markHistory.aspx').text
    #解析网页，查找到学院，这个要结合网页源码
    table=BeautifulSoup(html,'html.parser').find('select',id='ctl00_ContentPlaceHolder1_DropDownList3').find_all('option')
    school=[]
    #获取学院名
    for option in table:
        school.append(option.get_text())
    return school

#获取招生专业，分数及其他信息
def parser(year,province,school):
    #构造url,打开网页，获取源码
    url='http://zsb.suda.edu.cn/search.aspx?nf=%s&sf=%s&xy=%s'%(year,province,school)
    html=requests.get(url).text
    #解析网页，获取具体信息
    table=BeautifulSoup(html,'html.parser').find('table',id='ctl00_ContentPlaceHolder1_GridView1').find_all('tr')[1:]
    items=[]
    #遍历表格每一项，获取信息
    for tr in table:
        item=[]
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
    cursor.execute("create table if not exists markhistory(school varchar(80),year varchar(8),province varchar(80),professional varchar(80),length varchar(20),category varchar(20),numbers varchar(20),highest varchar(20),minimum varchar(20),average varchar(20))")
    #需要抓取的年份
    need_years=['2015','2014','2013']
    #获取招生的省份
    provinces=get_provinces()
    schools=get_school()
    #获取每个省每一年的信息
    for year in need_years:
        for province in provinces:
            for school in schools:
                #获取 某年（year)某地区（province）各专业信息
                index=schools.index(school)+1
                if(index>19):
                    index+=2
                try:
                    items=parser(year,provinces.index(province)+1,index)
                except:
                    continue
                for item in items:
                    item.insert(2, school)
                    #入库
                    cursor.execute('insert into markhistory(school,year,province,professional,length,category,numbers,highest,minimum,average) values'+str(tuple(item)))
                #提交事物，入库
                #打印完成信息
                print(school,year,province,'--ok')
    conn.commit()
    #关闭游标
    cursor.close()
    #关闭数据库连接
    conn.close()

main()
