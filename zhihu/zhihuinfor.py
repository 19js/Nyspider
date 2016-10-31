#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    'Cookie':'q_c1=52c451e7774943a2983e4b1341af47c4|1455451362000|1449924628000; _za=b08b756f-83e2-44b8-8719-9fd22ea0e8fc; __utma=51854390.837289251.1457412853.1457412853.1457412853.1; __utmz=51854390.1457412853.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/gejinyuban/topics; cap_id="MWRmMmU0NjlhMmM1NDRhMWFlYzg1MmI3OTJmYjJmN2I=|1457411531|febb54ce12ed1f54a9d134f44ad639a8d21a406a"; _xsrf=3193e002ffde3f8236b8bf0425ba0a8c; udid="AFBAu5wSlAmPTqUZ3Pnq-vBRhHF-_se18_Q="; n_c=1; __utmc=51854390; __utmb=51854390.2.10.1457412853; z_c0="QUFCQVB4azVBQUFYQUFBQVlRSlZUZERpQlZjb1l3SmlXMlVuTTVXNmMyamsyaFh0TmNZZm9BPT0=|1457411536|03555bed95004f561fc044aa14585204ce700106"; unlock_ticket="QUFCQVB4azVBQUFYQUFBQVlRSlZUZGhjM2xaVGJYbi1uVzlzS1pGODllTFZGaXpzTFZZbFZBPT0=|1457411536|9d460fe15bde1d5e5e723349745d7084654ce709"; __utmt=1; __utmv=51854390.100-1|2=registration_date=20141006=1^3=entry_date=20141006=1',
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_topics(ID):
    try:
        html=requests.get('https://www.zhihu.com/people/%s/topics'%ID,headers=headers).text
        table=BeautifulSoup(html,'lxml').find('div',id='zh-profile-topic-list').find_all('strong')
        topics=''
        for item in table:
            topics+=item.get_text()+','
        return topics[:-1]
    except:
        return get_topics(ID)

def get_profile(ID):
    try:
        html=requests.get('https://www.zhihu.com/people/%s'%ID,headers=headers).text
        rel='class="zg-gray-darker">(.*?)</a>'
        table=re.findall(rel,html)
        profile=''
        for item in table:
            profile+=item+','
        return profile[:-1]
    except:
        return get_profile(ID)

def main():
    f=open('person.txt','a',encoding='utf-8')
    statue=True
    for line in open('data.txt','r').readlines():
        line=line.replace('\n','')
        ID=line.split('||')[1]
        if(statue):
            if(ID=='kun-yu'):
                statue=False
            continue
        topics=get_topics(ID)
        profile=get_profile(ID)
        f.write(line+'||'+topics+'||'+profile+'\n')
        print(line)
    f.close()

main()
