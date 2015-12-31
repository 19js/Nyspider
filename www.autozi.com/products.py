#coding:utf-8

import requests
from bs4 import BeautifulSoup
import random

def get_headers():
    headers = {
        'Host':"www.autozi.com",
        "X-Forwarded-For":'%s.%s.%s.%s'%(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
        'Referer':"http://www.autozi.com/carBrandLetter/.html",
        'X-Requested-With':"XMLHttpRequest",
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    return headers

def get_type():
    html=requests.get('http://www.autozi.com/brandList.do',headers=get_headers()).text
    table=BeautifulSoup(html,'lxml').find_all('div',attrs={'class':'brand-list'})
    f=open('types.txt','w')
    for item in table[0].find_all('li',attrs={'class':'brand-list-item'}):
        text=item.find('img').get('src')+'||'
        text+='世界知名品牌'+'||'
        text+=item.find('a').get_text().replace('\n','')+'||'
        url=item.find('a').get('href')
        html=requests.get(url,headers=get_headers()).text
        try:
            types=BeautifulSoup(html,'lxml').find('ul',attrs={'class':'list-attrBrand lA-Category fix'}).find_all('li')
        except:
            f.write(text+'\n')
            continue
        for i in types:
            try:
                te=text+i.find('a').get_text().replace('\n','')+'||'
                te+=url+'&'+i.find('a').get('url')+'\n'
                f.write(te)
            except:
                continue
    for item in table[1].find_all('li',attrs={'class':'brand-list-item'}):
        text=item.find('img').get('src')+'||'
        text+='中国知名品牌'+'||'
        text+=item.find('a').get_text().replace('\n','')+'||'
        url=item.find('a').get('href')
        html=requests.get(url,headers=get_headers()).text
        try:
            types=BeautifulSoup(html,'lxml').find('ul',attrs={'class':'list-attrBrand lA-Category fix'}).find_all('li')
        except:
            f.write(text+'\n')
            continue
        for i in types:
            try:
                te=text+i.find('a').get_text().replace('\n','')+'||'
                te+=url+'&'+i.find('a').get('url')+'\n'
                f.write(te)
            except:
                continue
    f.close()

def get_products_url():
    data_f=open('products_url.txt','a')
    f=open('types.txt','r')
    for line in f.readlines():
        line=line.replace('\n','')
        url=line.split('||')[-1]
        if url=='':
            continue
        page=1
        while True:
            html=requests.get(url+'&currentPageNo='+str(page),headers=get_headers()).text
            page+=1
            table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'good-list'}).find_all('ul',attrs={'class':'list-item fix'})
            if table==[]:
                break
            for item in table:
                text=''
                text+=line+'||'
                text+=item.find('li').find('img').get('src')+'||'
                text+=item.find('li',attrs={'class':'list-name'}).find('a').get_text().replace('\n','').replace(' ','')+'||'
                text+=item.find('a').get('href')+'\n'
                data_f.write(text)
get_products_url()
