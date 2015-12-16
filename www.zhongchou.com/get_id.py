#coding:utf-8

import requests
from bs4 import BeautifulSoup

def get_id():
    f=open('ids.txt','a')
    headers = {
            'Host':"www.zhongchou.com",
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
    for page in range(150):
        html=requests.get('http://www.zhongchou.com/browse/re-p'+str(page+1),headers=headers).text.encode('ISO-8859-1').decode('utf-8','ignore')
        table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'sousuoListBox clearfix'}).find_all('div',attrs={'class':'ssCardItem'})
        for item in table:
            text=''
            p=item.find('h3').find('a')
            text=p.get('title')+'|'+p.get('href').replace('http://www.zhongchou.com/deal-show/id-','')+'\n'
            print(text)
            f.write(text)
        print(page)
    f.close()

get_id()
