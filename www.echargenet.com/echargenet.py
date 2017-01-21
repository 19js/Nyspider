import requests
import json
from bs4 import BeautifulSoup
import openpyxl
import time
import chardet
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_station(cityname):
    data={
    'chargePointName':cityname,
    'measuerModel':'',
    'isAppointment':''
    }
    html=requests.post('http://www.echargenet.com/portal/mapService/rest/map/queryChargePoint',data=data,headers=headers,timeout=30).text
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

def station_infor(stakeName):
    url='http://www.echargenet.com/portal/mapService/rest/map/queryStakeByStation?stakeName=%s&pageNo='%stakeName
    page=1
    try_num=0
    result=[]
    while True:
        if try_num==3:
            break
        try:
            html=requests.get(url+str(page), headers=headers,timeout=30).text
            try_num=0
        except:
            try_num+=1
            continue
        try:
            table=BeautifulSoup(html,'html.parser').find('table',attrs={'class':'pop-table'}).find_all('tr')
        except:
            break
        if len(table)==2:
            break
        for tr in table:
            if 'th class' in str(tr) or 'lastTr' in str(tr):
                continue
            tds=tr.find_all('td')
            line=[]
            for td in tds:
                text=td.get_text().replace('\r','').replace('\n','').replace('\t','').replace(' ','')
                line.append(text)
            result.append(line)
        page+=1
    return result

def get_time():
    timenow=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    return timenow

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    keys=['date','city','stakeName','stakeTotal','directPile','alternatingPile','stakeAddr','latitude','longitude','parkingPlace','openingHour','feesStandard','chargeServiceFees','manageOrgName','manageContactInfo','序号','名称','类型','状态','最大功率','最大电压','电压','电流','电量','SOC','支付方式','接口标准']
    sheet.append(keys)
    for filename in os.listdir(path='.'):
        if not filename.endswith('.txt'):
            continue
        for line in open(filename,'r',encoding='utf-8'):
            try:
                sheet.append(eval(line))
            except:
                continue
    excel.save('result/result.xlsx')

def main():
    citynames=load_cities()
    try:
        os.mkdir('result')
    except:
        pass
    keys=['stakeName','stakeTotal','directPile','alternatingPile','stakeAddr','latitude','longitude','parkingPlace','openingHour','feesStandard','chargeServiceFees','manageOrgName','manageContactInfo']
    for cityname in citynames:
        count=0
        status=True
        while True:
            try:
                stations=get_station(cityname=cityname)
                break
            except:
                if count==3:
                    status=False
                    break
                count+=1
        if status==False:
            print(get_time(),cityname,'Failed')
            continue
        f=open(cityname+'.txt','a',encoding='utf-8')
        for station in stations:
            timenow=get_time()
            line=[timenow,cityname]
            for key in keys:
                try:
                    line.append(station[key])
                except:
                    line.append('')
            infor=station_infor(station['stakeName'])
            for item in infor:
                f.write(str(line+item)+'\n')
            try:
                print(timenow,station['stakeName'],'ok')
            except:
                pass
        f.close()
        print(get_time(),cityname,'ok')
    write_to_excel()
    
try:
    sleeptime=input("输入间隔时间(分钟):")
    sleeptime=int(sleeptime)
except:
    sleeptime=15
while True:
    main()
    print("sleep")
    time.sleep(sleeptime*60)
