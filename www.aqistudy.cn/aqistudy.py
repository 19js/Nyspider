import requests
import time
from bs4 import BeautifulSoup
import os
import time


headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}

def get_city():
    html=requests.get('https://www.aqistudy.cn/historydata/',headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'all'}).find_all('a')
    cities=[]
    for item in table:
        try:
            name=item.get_text()
            url='https://www.aqistudy.cn/historydata/'+item.get('href')
            cities.append({'name':name,'url':url})
        except:
            continue
    return cities

def get_data(url):
    count=0
    while True:
        try:
            html=requests.get(url,headers=headers,timeout=30).text
            break
        except:
            count+=1
            if count==5:
                return []
    table=BeautifulSoup(html,'lxml').find('table',{'class':'table-condensed'}).find_all('tr')
    result=[]
    for item in table[1:]:
        try:
            tds=item.find_all('td')
            line=''
            for td in tds:
                line+=td.get_text().replace('\r','').replace('\n','').replace('\t','')+'\t'
            result.append(line)
        except:
            continue
    return result


def crawler(item):
    try:
        exists=os.listdir('result/'+item['name'])
    except:
        exists=[]
    try:
        os.mkdir('result')
    except:
        pass
    try:
        os.mkdir('result/'+item['name'])
    except:
        pass
    count=0
    while True:
        try:
            html=requests.get(item['url'],headers=headers,timeout=30).text
            break
        except:
            count+=1
            if count==5:
                return
    table=BeautifulSoup(html,'lxml').find('table',{'class':'table-condensed'}).find_all('tr')
    dates=[]
    for tr in table:
        try:
            date=tr.find('a').get_text()
            if date+'.txt' in exists:
                continue
            dates.append(date)
        except:
            continue
    for date in dates:
        try:
            data=get_data('https://www.aqistudy.cn/historydata/daydata.php?city=%s&month=%s'%(item['name'],date))
        except:
            continue
        if data==[]:
            continue
        f=open('result/%s/%s.txt'%(item['name'],date),'w')
        for line in data:
            f.write(line+'\n')
        f.close()
        print(item['name'],date,'ok')

def main():
    cities=get_city()
    for city in cities:
        try:
            crawler(city)
        except:
            print(city,'failed')
    print('完成')

main()
time.sleep(60)
