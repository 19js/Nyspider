import requests
from bs4 import BeautifulSoup
import time
import random
import os
import math
import datetime
import re
import logging

def get_headers():
    headers = {
        "X-Forwarded-For":'%s.%s.%s.%s'%(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
        'Host':"www.umetrip.com",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    return headers

def load_route(filename):
    routes=[]
    for line in open(filename,'r',encoding='utf-8'):
        try:
            line=line.replace('\r','').replace('\n','').replace('\t','').replace(' ','').split('-')
        except:
            continue
        routes.append(line)
    return routes

def get_flights_by_route(from_city,to_city,need_date):
    url='http://www.umetrip.com/mskyweb/fs/fa.do?dep={}&arr={}&date={}&channel='.format(from_city,to_city,need_date)
    while True:
        try:
            html=requests.get(url,headers=get_headers(),timeout=30).text.replace('\r','').replace('\n','').replace('\t','')
            break
        except:
            print(url,"获取失败，重试中")
    flights=re.findall('temp.push\((.*?)\);i\+\+;',html)
    result=[]
    for item in flights:
        spans=BeautifulSoup(item,'lxml').find_all('span')
        flight_num=spans[0].find('b').get_text().replace('"+"','')
        flight_company=spans[0].find_all('a')[-1].get_text()
        line=[need_date,from_city,to_city,flight_num[:2],flight_num,flight_company]
        for span in spans[1:-1]:
            line.append(span.get_text().replace('"+"',''))
        result.append(line)
    return result

def get_flight_info(flight_num,need_date,from_city,to_city):
    url='http://www.umetrip.com/mskyweb/fs/fc.do?flightNo={}&date={}&channel='.format(flight_num,need_date)
    while True:
        try:
            html=requests.get(url,headers=get_headers(),timeout=20).text
            break
        except:
            print(url,"获取失败，重试中")
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'flydetail'})
    flight_info=soup.find('div',{'class':'p_info'})
    fly_box=soup.find_all('div',{'class':'fly_box'})
    line=[]
    num=0
    index=0
    for box in fly_box:
        fly_name=box.find('h2').get('title').replace(' 始发','')
        fly_date=box.find('span').get_text()
        if from_city in fly_name:
            line+=[fly_name,fly_date]
            index=num
        if to_city in fly_name:
            line+=[fly_name,fly_date]
        num+=1
    for class_name in ['mileage','time','age']:
        try:
            line.append(flight_info.find_all('li',{'class':class_name})[index].find('span').get_text())
        except:
            line.append('')
    try:
        if '[' in str(fly_box[index]):
            print(str(fly_box[index]))
        pre_flight=re.findall('前序航班(.*?)\[',str(fly_box[index]))[0]
        print(pre_flight)
    except:
        pre_flight='-'
    line=[pre_flight]+line
    return line

def test():
    routes=load_route('./201702-ROUTE.txt')
    flag=True
    for route in routes:
        flag=False
        try:
            result=get_flights_by_route(route[0], route[1], '2017-05-07')
        except Exception as e:
            logging.exception(e,route)
            continue
        f=open('result.txt','a')
        for line in result:
            try:
                item=get_flight_info(line[4], '2017-05-07',line[1],line[2])
            except:
                print(line,'failed')
                continue
            f.write(str(line+item)+'\n')
        f.close()
        print(route,'OK')

test()
