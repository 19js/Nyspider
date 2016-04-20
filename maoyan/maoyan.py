#coding:utf-8

import requests
from bs4 import BeautifulSoup
import xlwt3
import datetime


def day_get(d):
    oneday = datetime.timedelta(days=1)
    day = d - oneday
    return day

def get_ids():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}
    d = datetime.datetime.now()
    f=open('ids.txt','w')
    while True:
        d=day_get(d)
        day=str(d).split(' ')[0]
        html=requests.get('http://piaofang.maoyan.com/?date=%s&cnt=10&_v_=yes'%day,headers=headers).text
        table=BeautifulSoup(html,'lxml').find('div',id='ticket_tbody').find_all('ul')
        for item in table:
            name=item.find('li').find('b').get_text()
            url=item.get('data-com').replace("hrefTo,href:'",'').replace("'",'')
            f.write(name+'||'+'http://piaofang.maoyan.com'+url+'\n')
        print(day)
        if day=='2014-01-01':
            break
    f.close()

get_ids()
