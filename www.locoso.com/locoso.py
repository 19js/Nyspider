#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_citys():
    url='http://www.locoso.com/s2/js/topcity.js'
    html=requests.get(url,headers=headers).text.replace('\\"','')
    table=BeautifulSoup(html,'lxml')
    lists=table.find_all('div',attrs={'class':'pro_bt'})
    f=open('citys.txt','a')
    root={}
    rel='prcity2(.*?)"'
    rel=re.compile(rel)
    citys={}
    for item in lists:
        try:
            root[str(item.get_text())]=eval(rel.findall(str(item))[0])[0]
        except:
            continue
        dicts={}
        for i in table.find('div',id=item.get('id')+'_2').find_all('li'):
            dicts[str(i.get_text())]=eval(rel.findall(str(i))[0])[0]
        citys[str(item.get_text())]=dicts
    for key in citys:
        for city in citys[key]:
            qu={}
            url='http://www.locoso.com/search/-all/c'+citys[key][city]
            html=requests.get(url,headers=headers).text
            table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'xiaofenlei_zhong02c2'}).find_all('li')
            dicts={}
            for i in table:
                dicts[i.find('a').get('title')]=i.find('a').get('href').replace('/search/-all/c','')
            qu[city]=dicts
            f.write(str(qu)+'\n')
            print(city)

def get_industry():
    html=requests.get('www.locoso.com/search/-all/',headers=headers)

get_citys()
