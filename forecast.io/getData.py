#coding:utf-8

import requests
import xlwt3
import time
import json


headers = {
    'Host':"forecast.io",
    'X-Requested-With':"XMLHttpRequest",
    'Referer':"http://forecast.io/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    'Cookie':"__utma=188038335.1670853311.1460370725.1460370725.1460374016.2; __utmc=188038335; __utmz=188038335.1460370725.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gauges_unique_day=1; _gauges_unique_month=1; _gauges_unique_year=1; _gauges_unique=1; __utmb=188038335.6.10.1460374016; __utmt=1; _gauges_unique_hour=1",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def getdata(timestr,session):
    html=session.get('http://forecast.io/forecast?q=35,105,%s&satellites'%timestr,headers=headers,proxies=proxies).text
    data=json.loads(html)['hourly']['data']
    return data

def timetostr(timestr):
    date=time.localtime(timestr)
    return time.strftime("%Y-%m-%d %H:%M:%S", date)

def main():
    excel=xlwt3.Workbook()
    sheet=excel.add_sheet('sheet')
    keys=['summary','temperature','windSpeed','humidity','visibility','pressure']
    count=0
    starttime=1262318400
    endtime=time.time()
    session=requests.session()
    while starttime<endtime:
        result=getdata(starttime,session)
        try:
            data=result[10]
        except:
            continue
        date=timetostr(starttime)
        num=1
        for key in keys:
            try:
                sheet.write(count,num,data[key])
                num+=1
            except:
                num+=1
                continue
        sheet.write(count,0,date)
        starttime+=86400
        count+=1
        print(date,'--ok')
        excel.save('result.xls')

main()
