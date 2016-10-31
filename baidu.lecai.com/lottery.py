import requests
from bs4 import BeautifulSoup
import time
import json
import datetime
import openpyxl

headers = {
    'Host':"baidu.lecai.com",
    'X-Requested-With':"XMLHttpRequest",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    'Referer':"http://baidu.lecai.com/lottery/draw/sorts/cqssc.php?phase=20161027023&agentId=5591",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_data(date):
    url='http://baidu.lecai.com/lottery/draw/sorts/ajax_get_draw_data.php?lottery_type=200&date='+date
    html=requests.get(url,headers=headers).text
    data=json.loads(html)['data']['data']
    result=[]
    num=1
    while(len(data)):
        item=data.pop()
        result.append([date,num]+item['result']['result'][0]['data'])
        num+=1
    return result

def day_get(d):
    oneday = datetime.timedelta(days=1)
    day = d - oneday
    return day

def load_data():
    data={}
    for line in open('result.txt','r'):
        item=eval(line)
        date=item[0]
        value=item
        try:
            data[date].append(value)
        except:
            data[date]=[value]
    return data

def compare(first,second):
    line=first
    value1=int(first[-2])
    value2=int(first[-1])
    value3=int(second[-2])+10
    value4=int(second[-1])+10
    value5=(value3-value1)%10
    value6=(value4-value2)%10
    line+=[value5,value6,str(value5*10+value6)]
    return line

def lottery_data():
    d=datetime.datetime.now()
    d=day_get(d)
    while True:
        date=str(d).split(' ')[0]
        if date=='2015-10-25':
            break
        result=get_data(date)
        f=open('result.txt','a')
        for line in result:
            f.write(str(line)+'\n')
        f.close()
        print(date,'ok')
        d=day_get(d)
        time.sleep(1)

def deal():
    data=load_data()
    result={}
    for key in data:
        lines=data[key]
        length=len(lines)
        result[key]=[]
        counter={}
        for index in range(0,length-1):
            first=lines[index]
            second=lines[index+1]
            line=compare(first,second)
            result[key].append(line)
            try:
                counter[line[-1]]+=1
            except:
                counter[line[-1]]=1
        for line in result[key]:
            line.append(counter[line[-1]])
        result[key].append(lines[-1])
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    result=sorted(result.items(),key=lambda x:x[0],reverse=True)
    for item in result:
        for line in item[1]:
            sheet.append(line)
    excel.save('result.xlsx')

deal()
