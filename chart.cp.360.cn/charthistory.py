import requests
from bs4 import BeautifulSoup
import time
import datetime

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def get_history(date):
    url='http://chart.cp.360.cn/kaijiang/kaijiang?lotId=255401&spanType=2&span=%s_%s'%(date,date)
    html=requests.get(url,headers=headers).text.encode('iso-8859-1').decode('gbk')
    tables=BeautifulSoup(html,'lxml').find('div',id='his-tab').find('table',{'width':'100%'}).find_all('table')
    result=[]
    for table in tables:
        for tr in table.find_all('tr'):
            try:
                tds=tr.find_all('td')
                number=tds[0].get_text()
                if number=='':
                    continue
                value=tds[1].get_text()
                if value=='':
                    continue
                value1=value[:3]
                value2=value[1:4]
                value3=value[2:]
                result.append([date,number,value,value1,value2,value3])
            except:
                continue
    return result

def nextday(d):
    oneday = datetime.timedelta(days=1)
    day = d+oneday
    return day

def main():
    day=datetime.datetime.strptime('2010-01-01','%Y-%m-%d')
    while True:
        str_day=str(day).split(' ')[0]
        f=open('result.txt','a')
        try:
            result=get_history(str_day)
        except:
            print(str_day,'failed')
            time.sleep(1)
            continue
        for item in result:
            f.write(str(item)+'\n')
        f.close()
        day=nextday(day)
        print(str_day,'ok')
        time.sleep(1)
        if str_day=='2016-10-23':
            break

main()
