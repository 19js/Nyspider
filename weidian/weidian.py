#coding:utf-8

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"}

def get_place():
    f=open('place.txt','w')
    browser=webdriver.Firefox()
    #html=requests.get('http://weidian.com/near_shop/chunjie/city.html?&from=weidian&userid=211106418&umk=34542211106418',headers=headers).text.encode('ISO-8859-1').decode('utf-8','ignore')
    browser.get('http://weidian.com/near_shop/chunjie/city.html?&from=weidian&userid=211106418&umk=34542211106418')
    time.sleep(10)
    html=browser.page_source
    table=BeautifulSoup(html,'lxml').find('div',id='show-place').find_all('ul')
    places={}
    print(html)
    for item in table[1:]:
        for li in item.find_all('li'):
            places[li.get_text()]='http://weidian.com/near_shop/chunjie/'+li.find('a').get('href')
    for li in table[0].find_all('li'):
        places[li.get_text()]='http://weidian.com/near_shop/chunjie/'+li.find('a').get('href')
    for key in places:
        text=key+'||'+places[key]+'\n'
        f.write(text)
    f.close()

def get_shop():
    f=open('shops.txt','a',encoding='utf-8')
    for line in open('place.txt').readlines():
        city=line.split('||')[0]
        place=re.findall('place=(.*?)&',line)[0]
        page=0
        while True:
            url='http://api.buyer.weidian.com/h5/appserver_nearbyShop.do?place='+place+'&seed=0&category=%E7%AE%B1%E5%8C%85&limit=50&page='+str(page)+'&callback=jsonp4&rnd=0.8898308666990978'
            html=requests.get(url,headers=headers).text
            rel='"shopid":"(.*?)","entranceName":"(.*?)","address":"(.*?)"'
            lists=re.findall(rel,html)
            if lists==[]:
                break
            for item in lists:
                text=item[0]+'||'+item[1]+'||'+item[2]
                f.write(text+'\n')
            print(city+place+'--'+str(page))
            page+=1
    f.close()

def get_weixin():
    f=open('data.txt','a')
    for line in open('shops.txt'):
        line=line.replace('\n','')
        shopurl='http://weidian.com/?userid='+line.split('||')[0]
        html=requests.get(shopurl,headers=headers).text
        try:
            html=requests.get(shopurl,headers=headers).text
            rel='微信: (.*?)<'
            weixin=re.findall(rel,html)[0]
        except:
            continue
        print(line+'---OK')
        line=line+'||'+weixin+'\n'
        f.write(line)

def main():
    #get_shop()
    get_weixin()

main()
