import requests
from bs4 import BeautifulSoup
import time
import os
import re
import json

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_token(year,month,day,hour,minutes):
    url='http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w={}年{}月{}日%20{}点{}分分时成交量&queryarea='
    html=requests.get(url.format(year,month,day,hour,minutes),headers=headers,timeout=30).text
    token=re.findall('"token":"(.*?)"',html)[0]
    return token

def get_volume(token,filename):
    page=1
    url='http://www.iwencai.com/stockpick/cache?token={}&p={}&perpage=30&showType=[%22%22,%22%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22]'
    while True:
        try:
            html=requests.get(url.format(token,page),headers=headers,timeout=30).text
            data=json.loads(html)
        except Exception as e:
            print(e,page,'Failed')
            time.sleep(1)
            continue
        try:
            result=data['result']
        except:
            break
        f=open(filename,'a',encoding='utf-8')
        for item in result:
            f.write('\t'.join([str(i) for i in item])+'\r\n')
        f.close()
        print('Page',page,'OK')
        page+=1

def iwencai():
    try:
        date=input("输入需采集的日期和时间(如:2017.03.31-09:25):")
        line=date.split('-')
        year=line[0].split('.')[0]
        month=line[0].split('.')[1]
        day=line[0].split('.')[2]
        hour=line[1].split(':')[0]
        minutes=line[1].split(':')[1]
    except Exception as e:
        print("输入时间格式不正确")
        return
    try:
        token=get_token(year, month, day, hour, minutes)
    except Exception as e:
        print(e,"token 获取失败")
        return
    try:
        os.mkdir('result')
    except:
        pass
    get_volume(token, "result/"+date.replace('.','_').replace(':','_').replace('-','_'))

while True:
    iwencai()
