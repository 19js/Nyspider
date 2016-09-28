import requests
from bs4 import BeautifulSoup
import time
import pymysql
import random
import json
import re

def get_headers():
    headers = {
        "X-Forwarded-For":'%s.%s.%s.%s'%(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
        'Host':"www.3j1688.com",
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    return headers

def login():
    session=requests.session()
    html=session.post('http://www.3j1688.com/member/index.html',data=data,headers=get_headers()).text
    return session

def get_phones(session):
    html=session.get('http://www.3j1688.com/goods/lj/3/bjd.html',headers=get_headers()).text.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
    table=re.findall('varsg={(.*?)}',html)[0].split(',')
    keys=[]
    for item in table:
        try:
            keys.append(item.split(':')[0])
        except:
            continue
    print(keys)
    phones=[]
    for key in keys:
        try:
            html=session.post('http://www.3j1688.com/goods/lj/bjdjsonByBrand.html',data={'brandName':key},headers=get_headers()).text
            data=json.loads(html)['data']
            for item in data:
                phones.append(item)
        except:
            continue
    return phones

def get_phone(item,session):
    html=session.get('http://www.3j1688.com/goods/detail/%s.html?s=bjd'%item['goodsNum'],headers=get_headers()).text
    soup=BeautifulSoup(html,'lxml').find('div',id='xq_mian')
    table=soup.find('div',{'class':'xq_main_02_let_03'}).find_all('div',{'class':'xq_main_02_let_02'})
    products=[]
    for div in table:
        try:
            tds=div.find('tr').find_all('td')
            phone_infor=[]
            for td in tds[2:6]:
                try:
                    phone_infor.append(td.get_text())
                except:
                    phone_infor.append('')
            price=div.find('h4').get_text().replace('\r','').replace('\n','').replace('\t','').replace(' ','').replace('/','')
            products.append({'infor':phone_infor,'price':price})
        except:
            continue
    des=str(soup.find('div',{'class':'goods_main_contents'}))
    item['des']=des
    item['products']=products
    return item

session=login()
#get_phones(session)
html=open('./template.html','r').read()
item=get_phone({'goodsNum': '875', 'isCollected': False, 'isNew': False, 'price': 2228, 'goodsName': '乐视 乐视Max 2 （6G+64GB）', 'isHot': False},session)
with open('html.html','w') as f:
    f.write(html.format(title=item['goodsName'],des=item['des']))
