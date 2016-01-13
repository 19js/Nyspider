#coding:utf-8

import requests
from bs4 import  BeautifulSoup
import time

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_kinds():
    f=open('types.txt','w')
    url='http://www.china-10.com/brand/'
    html=requests.get(url).text
    table=BeautifulSoup(html,'lxml').find('div',id='menubox').find('ul',id='conmenu').find_all('li',attrs={'class':'menu'})
    for item in table[1:-3]:
        key=item.find('a').get_text().replace('\n','')+'||'
        for li in item.find_all('li'):
            f.write(key+li.find('a').get('title')+'||'+li.find('a').get('href')+'\n')
    f.close()

def get_brands():
    f=open('types.txt','r')
    data=open('brands.txt','w')
    for line in f.readlines():
        print(line)
        line=line.replace('\n','')
        page=1
        while True:
            html=requests.get(line.split('||')[-1]+'?action=ajax&page='+str(page),headers).text
            page+=1
            table=BeautifulSoup(html,'lxml').find_all('li')
            if(table==[]):
                break
            for item in table:
                text=line+'||'+item.get_text()+'||'+item.find('a').get('href')+'\n'
                data.write(text)
            print(page)
    f.close()

def get_infor(line):
    html=requests.get(line.split('||')[-1],headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'brandinfo'})
    des=table.find('dd').get_text()
    line+='||'+des
    table=table.find('ul').find_all('li')
    for li in table:
        line+='||'+li.get_text().replace('\r','').replace('\n','').replace('\t','').replace(' ','')
    return line

def main():
    data=open('data.txt','a')
    failed=open('failed.txt','a')
    count=0
    for line in open('brands.txt','r').readlines():
        line=line.replace('\n','')
        try:
            line=get_infor(line)
        except:
            failed.write(line+'\n')
            continue
        data.write(line+'\n')
        count+=1
        time.sleep(1)
        print(count)

main()
