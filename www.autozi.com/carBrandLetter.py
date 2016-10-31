#coding:utf-8

import requests
from bs4 import BeautifulSoup
import xlwt3
import time
import random
import re

def get_ids():
    f=open('ids.txt','w')
    html=requests.get('http://www.autozi.com/carBrandLetter/.html',headers=headers).text
    tables=BeautifulSoup(html,'lxml').find('div',id='carLetter').find_all('table',attrs={'class':'car-brand'})
    for table in tables:
        for tr in table.find_all('tr'):
            one=tr.find('th').find('h4').get_text()
            for li in tr.find('ul').find_all('li'):
                two=li.find('h4').get_text()
                for a in li.find_all('a'):
                    three=a.get_text()
                    url=a.get('s_href')
                    f.write(one+'||'+two+'||'+three+'||'+url+'\n')

def get_car():
    f=open('ids.txt','r')
    count=1
    data=open('data.txt','a')
    for line in f.readlines():
        page=1
        line=line.replace('\n','')
        code=line.split('=')[1]
        xs="%.3f"%time.time()
        xs=xs.replace('.','')
        while True:
            data_post={
            'currentPageNo':page,
            'carSeriesId':code,
            '_':xs
            }
            url='http://www.autozi.com/carmodelsAjax.do?currentPageNo=%s&carSeriesId=%s&_=%s'%(page,code,xs)
            #html=requests.get(url).text
            #print(url)
            headers = {
                'Host':"www.autozi.com",
                "X-Forwarded-For":'%s.%s.%s.%s'%(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
                'Referer':"http://www.autozi.com/carBrandLetter/.html",
                'X-Requested-With':"XMLHttpRequest",
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate'}
            html=requests.get(url,headers=headers).text
            page+=1
            table=BeautifulSoup(html,'lxml').find_all('li')
            if(table==[]):
                break
            for i in table:
                data.write(line+'||'+i.get_text()+'\n')
        print(count)
        count+=1

def write_to_excel():
    f=open('data.txt','r')
    excel=xlwt3.Workbook()
    sheet=excel.add_sheet('sheet')
    count=0
    for line in f.readlines():
        lists=line.split('||')
        sheet.write(count,0,lists[0])
        sheet.write(count,1,lists[1])
        sheet.write(count,2,lists[2])
        sheet.write(count,3,lists[4])
        title=lists[4]
        year_re=u'\d\d\d\d'
        pailiang_re=u'\d\.\dL|\d\.\dT'
        try:
            sheet.write(count,4,re.findall(year_re,title)[0])
        except:
            sheet.write(count,4,'')
        try:
            sheet.write(count,5,re.findall(pailiang_re,title)[0])
        except:
            sheet.write(count,5,'')
        count+=1
    excel.save('data.xls')

write_to_excel()
