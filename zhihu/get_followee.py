#coding:utf-8

import requests
from bs4 import BeautifulSoup
import json


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    'Cookie':'q_c1=52c451e7774943a2983e4b1341af47c4|1455451362000|1449924628000; _za=b08b756f-83e2-44b8-8719-9fd22ea0e8fc; __utma=51854390.837289251.1457412853.1457412853.1457412853.1; __utmz=51854390.1457412853.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/gejinyuban/topics; cap_id="MWRmMmU0NjlhMmM1NDRhMWFlYzg1MmI3OTJmYjJmN2I=|1457411531|febb54ce12ed1f54a9d134f44ad639a8d21a406a"; _xsrf=3193e002ffde3f8236b8bf0425ba0a8c; udid="AFBAu5wSlAmPTqUZ3Pnq-vBRhHF-_se18_Q="; n_c=1; __utmc=51854390; __utmb=51854390.2.10.1457412853; z_c0="QUFCQVB4azVBQUFYQUFBQVlRSlZUZERpQlZjb1l3SmlXMlVuTTVXNmMyamsyaFh0TmNZZm9BPT0=|1457411536|03555bed95004f561fc044aa14585204ce700106"; unlock_ticket="QUFCQVB4azVBQUFYQUFBQVlRSlZUZGhjM2xaVGJYbi1uVzlzS1pGODllTFZGaXpzTFZZbFZBPT0=|1457411536|9d460fe15bde1d5e5e723349745d7084654ce709"; __utmt=1; __utmv=51854390.100-1|2=registration_date=20141006=1^3=entry_date=20141006=1',
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_followe(ID,hashid):
    html=requests.get('https://www.zhihu.com/people/%s/followees'%ID,headers=headers).text
    xsrf=BeautifulSoup(html,'lxml').find('input',attrs={'name':'_xsrf'}).get('value')
    print(xsrf)
    count=0
    persons=[]
    while True:
        data={
        'method':"next",
        'params':'{"offset":%s,"order_by":"created","hash_id":"%s"}'%(count,hashid),
        '_xsrf':xsrf
        }
        try:
            html=requests.post('https://www.zhihu.com/node/ProfileFolloweesListV2',headers=headers,data=data).text
        except:
            continue
        try:
            jsondata=json.loads(html)['msg']
        except:
            return persons
        if(jsondata==[]):
            break
        for item in jsondata:
            name=BeautifulSoup(item,'lxml').find('a',attrs={'class':'zg-link'}).get('title')
            persons.append(name)
        count+=20
    return persons

def main():
    f=open('followee.txt','a',encoding='utf-8')
    statue=True
    for line in open('data.txt','r').readlines():
        lists=line.split('||')
        name=lists[0]
        if(statue):
            if(name=='keso'):
                statue=False
            continue
        ID=lists[1]
        item={}
        item['name']=name
        item['id']=ID
        hashid=lists[3]
        item['followee']=get_followe(ID, hashid)
        f.write(str(item)+'\n')
        print(name)
main()
