#coding:utf-8

import requests
from bs4 import BeautifulSoup

def get_infor():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}
    fi=open('ids.txt','r')
    infor_f=open('data.txt','a')
    count=0
    for line in fi.readlines():
        if(count<608):
            count+=1
            continue
        lists=line.split('||')
        try:
            html=requests.get(lists[1].replace('\n',''),headers=headers).text
            soup=BeautifulSoup(html,'lxml')
            infor=soup.find('aside',attrs={'class':'infos'}).find_all('p')
            Type=infor[0].get_text()
            date=infor[3].get_text()
            tags=soup.find('article',attrs={'class':'tags clearfix'}).find_all('span')
        except:
            continue
        try:
            zong_piao=tags[0].get_text().replace('总票房:','')
            zhou_piao=tags[1].get_text().replace('首周票房:','')
        except:
            continue
        try:
            text=lists[0]+'||'+date+'||'+Type+'||'+zong_piao+'||'+zhou_piao+'||'
            table=soup.find('div',id='ticket_tbody').find_all('ul')
        except:
            continue
        for item in table:
            lis=item.find_all('li')
            infor_f.write(text+lis[0].get_text()+'||'+lis[3].get_text()+'\n')
        count+=1
        print(count)

get_infor()
