#coding:utf-8

import requests
from bs4 import BeautifulSoup
import xlwt3
import re


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_shop_urls(url):
    html=requests.get(url,headers=headers).text
    rel='(mall.jd.com/index-\d+.html)'
    urls=re.findall(rel,html)
    urls=list(set(urls))
    return urls

def get_infor(url):
    html=requests.get(url,headers=headers).text

def get_type_url():
    html=requests.get('http://search.jd.com/jshop.php?keyword=&enc=utf-8&vender=1',headers=headers).text.encode('utf-8').decode('utf-8','ignore')
    table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'sl-value'}).find('div',attrs={'class':'sl-v-list'}).find_all('li')
    items=[]
    for li in table:
        item={}
        item['name']=li.get_text()
        item['url']=li.find('a').get('href')
        items.append(item)
    return items

def main():
    items=get_type_url()
    print(items)
    for item in items:
        page=1
        while True:
            urls=get_shop_urls('http://search.jd.com/jshop.php'+item['url']+'&page=%s'%page)
            print(urls)
            return

main()
