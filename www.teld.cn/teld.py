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

def get_station(cityname='',provincename=''):
    html=requests.get('http://www.teld.cn/StationNetwork/GetStationNetword?ProvinceName={}&CityName={}&KeyWords=&RegionName=&type='.format(provincename,cityname),headers=headers,timeout=30).text
    data=json.loads(html)
    return data

def get_chardet(filename):
    data=open(filename,'rb').read()
    coding=chardet.detect(data)
    return coding['encoding']

def load_cities():
    encoding=get_chardet('setting/cities.txt')
    if encoding=='GB2312':
        encoding='GBK'
    citynames=[]
    for line in open('setting/cities.txt'):
        name=line.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
        citynames.append(name)
    return citynames

def station_infor(stationid):
    html=requests.get('http://www.teld.cn/StationNetwork/GetChargingStationByCodeList?StationNo='+stationid,headers=headers,timeout=30).text
    data=json.loads(html)
    return data

def get_time():
    timenow=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    return timenow

def write_to_excel(filename):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in open(filename+'.txt','r',encoding='utf-8'):
        try:
            sheet.append(eval(line))
        except:
            continue
    excel.save('result/'+filename+'.xlsx')

def main():
    citynames=load_cities()
    try:
        os.mkdir('result')
    except:
        pass
    province=['北京市','上海市','天津市','重庆市']
    for name in citynames:
        provincename=''
        cityname=''
        if name in province:
            provincename=name
        else:
            cityname=name
        count=0
        status=True
        while True:
            try:
                stations=get_station(cityname=cityname,provincename=provincename)
                break
            except:
                if count==3:
                    status=False
                    break
                count+=1
        if status==False:
            print(get_time(),name,'Failed')
            continue
        f=open(name+'.txt','a',encoding='utf-8')
        for station in stations:
            count=0
            status=True
            while True:
                try:
                    infor=station_infor(station['code'])
                    break
                except:
                    if count==3:
                        status=False
                        break
                    count+=1
            if status==False:
                continue
            timenow=get_time()
            for item in infor:
                line=[timenow]
                for key in ['name','address','operateTypeName','statypename']:
                    try:
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
                f.write(str(line)+'\n')
            print(timenow,station['name'],'ok')
            time.sleep(1)
        f.close()
        write_to_excel(name)
        print(get_time(),name,'ok')

try:
    sleeptime=input("输入间隔时间(分钟):")
    sleeptime=int(sleeptime)
except:
    sleeptime=15
while True:
    main()
    print("sleep")
    time.sleep(sleeptime*60)
