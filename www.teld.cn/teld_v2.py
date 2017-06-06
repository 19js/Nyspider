import requests
import json
from bs4 import BeautifulSoup
import openpyxl
import time
import chardet
import os

headers = {
    'Host':"www.teld.cn",
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_stations(page):
    url='http://www.teld.cn/StationNetwork/GetStationNetword?ProvinceName=&CityName=&KeyWords=&RegionName=&type=&page={}&rows=100'
    html=requests.get(url.format(page),headers=headers,timeout=30).text
    result=json.loads(html)['rows']
    return result

def station_infor(stationid):
    html=requests.get('http://www.teld.cn/StationNetwork/GetChargingStationByCodeList?StationNo='+stationid,headers=headers,timeout=30).text
    data=json.loads(html)
    return data

def get_time():
    timenow=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    return timenow

def write_to_excel(crawl_date):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in open('temp/'+crawl_date+'.txt','r',encoding='utf-8'):
        try:
            sheet.append(eval(line))
        except:
            continue
    excel.save('result/'+crawl_date+'.xlsx')

def crawl(station,crawl_date):
    count=0
    while True:
        try:
            infor=station_infor(station['code'])
            break
        except Exception as e:
            if count==5:
                info=[{'test':'1'}]
                break
            count+=1
    timenow=get_time()
    f=open('temp/'+crawl_date+'.txt','a',encoding='utf-8')
    for item in infor:
        line=[timenow]
        for key in ['name','address','operateTypeName','code','longitude','latitude']:
            try:
                if station[key]==None:
                    line.append('')
                else:
                    line.append(station[key])
            except:
                line.append('')
        for key in ['name','piletype','stateName']:
            try:
                if key=='piletype':
                    piletype=item['piletype']
                    if piletype=='1101':
                        line.append('交流')
                    else:
                        line.append('直流')
                else:
                    line.append(item[key])
            except:
                line.append('')
        f.write(str(line)+'\r\n')
    f.close()
    print(timenow,station['name'],'ok')

def teld():
    try:
        os.mkdir('result')
    except:
        pass
    try:
        os.mkdir('temp')
    except:
        pass
    page=1
    crawl_date=time.strftime('%Y_%m_%d')
    while True:
        try:
            stations=get_stations(page)
        except Exception as e:
            print('[get_stations][error]Page',page,e,'\n重试中')
            continue
        if len(stations)==0:
            break
        for station in stations:
            crawl(station,crawl_date)
        print(page,'OK')
        page+=1
    write_to_excel(crawl_date)
    print(get_time(),crawl_date,'抓取完成')

try:
    sleeptime=input("输入间隔时间(分钟):")
    sleeptime=int(sleeptime)
except:
    sleeptime=60

while True:
    teld()
    print("sleep")
    time.sleep(sleeptime*60)
