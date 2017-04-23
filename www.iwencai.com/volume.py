import requests
from bs4 import BeautifulSoup
import time
import os
import re
import json
import datetime

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def day_get(d):
    oneday = datetime.timedelta(days=1)
    day = d + oneday
    day = str(day).split(' ')[0].replace('-','.')
    return day

def get_token(year,month,day,hour,minutes):
    url='http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w={}年{}月{}日%20{}点{}分分时成交量&queryarea='
    html=requests.get(url.format(year,month,day,hour,minutes),headers=headers,timeout=30).text
    token=re.findall('"token":"(.*?)"',html)[0]
    return token

def get_volume(token,filename,date):
    page=1
    url='http://www.iwencai.com/stockpick/cache?token={}&p={}&perpage=30&showType=[%22%22,%22%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22]'
    while True:
        try:
            html=requests.get(url.format(token,page),headers=headers,timeout=30).text
            data=json.loads(html)
        except Exception as e:
            print(date,e,page,'Failed')
            time.sleep(1)
            continue
        try:
            result=data['result']
        except:
            break
        f=open(filename,'a',encoding='utf-8')
        for item in result:
            try:
                code=item[0].split('.')[-1]+item[0].split('.')[0]
                value=str(item[4])
            except:
                continue
            f.write(code+'\t'+date+'\t'+value+'\r\n')
        f.close()
        print(date,'Page',page,'OK')
        page+=1

def iwencai():
    try:
        os.mkdir('result')
    except:
        pass
    try:
        date=input("输入需采集的日期区间(如:2017.03.01-2017.03.31):")
        line=date.split('-')
        date_from=line[0]
        date_to=line[1]
    except Exception as e:
        print("输入时间格式不正确")
        return
    hour='09'
    minutes='25'
    while True:
        year=date_from.split('.')[0]
        month=date_from.split('.')[1]
        day=date_from.split('.')[2]
        try:
            token=get_token(year, month, day, hour, minutes)
        except Exception as e:
            print(e,year,month,day,"token 获取失败")
            continue
        get_volume(token, "result/"+date_from.replace('.','_')+'.txt',date_from.replace('.','-'))
        if date_from==date_to:
            break
        current_date=datetime.datetime.strptime(date_from, "%Y.%m.%d")
        date_from=day_get(current_date)

while True:
    iwencai()
