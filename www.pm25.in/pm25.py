import requests
from bs4 import BeautifulSoup
import time
import os
import re

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def get_city():
    html=requests.get('http://www.pm25.in/',headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'all'}).find_all('a')
    result={}
    for item in table:
        result[item.get_text()]='http://www.pm25.in/'+item.get('href')
    return result

def get_time():
    timenow=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    return timenow

def infor(url):
    count=0
    while True:
        try:
            html=requests.get(url,headers=headers,timeout=30).text
            break
        except:
            count+=1
            if count==3:
                return False
    soup=BeautifulSoup(html,'lxml')
    date=soup.find('div',{'class':'live_data_time'}).get_text().replace('\r','').replace('\n','').replace('\t','').replace('数据更新时间：','')
    table=soup.find('table',id='detail-data').find('tbody').find_all('tr')
    result={'date':date}
    result['list']=[]
    for item in table:
        line=[]
        for td in item.find_all('td'):
            line.append(td.get_text().replace('\r','').replace('\n','').replace('\t',''))
        result['list'].append(line)
    return result

def main():
    try:
        os.mkdir('result')
    except:
        pass
    count=0
    while True:
        try:
            cities=get_city()
            break
        except:
            count+=1
            if count==3:
                return
            f=open('log.txt','a',encoding='utf-8')
            print('Get City Failed!')
            timenow=get_time()
            f.write(str(timenow)+'---Get City Failed!\r\n')
            f.close()
    log_f=open('log.txt','a',encoding='utf-8')
    for city in cities:
        try:
            os.mkdir('result/'+city)
        except:
            pass
        count=0
        status=True
        while True:
            try:
                result=infor(cities[city])
                break
            except:
                count+=1
                if count==3:
                    status=False
                    break
        if not status:
            continue
        date=result['date']
        for item in result['list']:
            try:
                text=open('result/'+city+'/'+item[0]+'.txt','r',encoding='utf-8').read()
                if date in text:
                    continue
            except:
                pass
            f=open('result/'+city+'/'+item[0]+'.txt','a',encoding='utf-8')
            line=[date]+item
            f.write('\t'.join(line)+'\r\n')
            f.close()
        print(date,city,'ok')
        log_f.write(date+'---'+city+'ok'+'\r\n')
    log_f.close()

while True:
    try:
        main()
    except:
        time.sleep(20)
        continue
    date=time.strftime("%Y-%m-%d %H:%M:%S")
    print(date,'sleep')
    time.sleep(20*60)
