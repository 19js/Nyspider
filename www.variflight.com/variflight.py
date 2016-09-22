import requests
from bs4 import BeautifulSoup
import time

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}


def flights():
    html=requests.get('http://www.variflight.com/sitemap.html?AE71649A58c77',headers=headers).text
    table=BeautifulSoup(html,'html.parser').find('div',{'class':'list'}).find_all('a')
    f=open('flights.txt','a',encoding='utf-8')
    for item in table:
        try:
            url='http://www.variflight.com/'+item.get('href')+'&fdate='
            if 'flight/fnum/' not in url:
                continue
            name=item.get_text()
            f.write(name+'|'+url+'\n')
        except:
            continue
    f.close()

def get_image(img_url):
    count=0
    while True:
        try:
            content=requests.get(img_url,headers=headers,timeout=30).content
            return content
        except:
            count+=1
            if count==4:
                return False

def parser(url):
    count=0
    while True:
        try:
            html=requests.get(url,headers=headers,timeout=30).text
            break
        except:
            count+=1
            if count==4:
                return False
    table=BeautifulSoup(html.replace('\n','').replace('\t',''),'html.parser').find('ul',id='list').find_all('div',{'class':'li_com'})
    result=[]
    for item in table:
        try:
            flight={}
            spans=item.find_all('span')
            flight['name']=spans[0].get_text()
            flight['fly_time']=spans[1].get_text()
            flight['r_fly_time_url']='http://www.variflight.com/'+spans[2].find('img').get('src')
            flight['from']=spans[3].get_text()
            flight['arrive_time']=spans[4].get_text()
            flight['r_arrive_time_url']='http://www.variflight.com/'+spans[5].find('img').get('src')
            flight['to']=spans[6].get_text()
            flight['on_time']='http://www.variflight.com/'+spans[7].find('img').get('src')
            flight['status']=spans[8].get_text()
            result.append(flight)
        except:
            continue
    return result

def crawler(date):
    timenow=time.strftime('%Y%m%d_%H%M%S')
    f=open(timenow+'.txt','a',encoding='utf-8')
    for line in open('flights.txt','r',encoding='utf-8'):
        line=line.replace('\r','').replace('\n','')
        url=line.split('|')[-1]
        try:
            item=parser(url+date)
        except:
            continue
        if item==[]:
            continue
        print(line)
        f.write(str(item)+'\n')
        time.sleep(1)
    f.close()

flights()
crawler('20160920')
