import requests
from bs4 import BeautifulSoup
import time
import openpyxl

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_house():
    page=1
    url='http://newhouse.cs.fang.com/house/s/b9'
    while True:
        html=requests.get(url+str(page),headers=headers).text.encode('iso-8859-1').decode('gbk')
        table=BeautifulSoup(html,'lxml').find('div',{'class':'nhouse_list'}).find_all('li')
        f=open('urls.txt','a')
        for item in table:
            detail=item.find('div',{'class':'nlc_details'})
            house_url=detail.find('a').get('href')
            name=detail.find('a').get_text()
            address_div=detail.find('div',{'class':'address'})
            address=address_div.find('a').get('title')
            try:
                location=address_div.find('span').get_text()
            except:
                location='-'
            try:
                price=detail.find('div',{'class':'nhouse_price'}).find('span').get_text()
            except:
                price='-'
            line=name+'|'+house_url+'|'+price+'|'+location+'|'+address
            line=line.replace('\r','').replace('\n','').replace('\t','')
            f.write(line+'\n')
        f.close()
        print(page,'ok')
        page+=1
        time.sleep(1)

def get_house_live_history(url):
    html=requests.get(url,headers=headers).text.encode('iso-8859-1').decode('gbk')
    table=BeautifulSoup(html,'lxml').find('div',id='tc_jiaofang').find_all('tr')
    lines=[]
    for tr in table[2:-1]:
        tds=tr.find_all('td')
        date=tds[0].get_text()
        month=date.split('-')[1]
        infor=tds[1].get_text()
        line=month+'|'+date+'|'+infor
        lines.append(line.replace('\xa0',''))
    return lines

def house_live_history():
    is_ok=True
    for item in open('urls.txt','r'):
        item=item.replace('\n','')
        url=item.split('|')[1]
        if url!='http://jiulongshanjy.fang.com/' and is_ok==True:
            continue
        is_ok=False
        try:
            lines=get_house_live_history(url)
        except:
            lines=[]
        print(item)
        f=open('changsha.txt','a')
        if lines==[]:
            f.write(item+'\n')
            f.close()
            continue
        for line in lines:
            f.write(item+'|'+line+'\n')
        f.close()
        time.sleep(1)

house_live_history()
