#coding:utf-8

import requests
from bs4 import BeautifulSoup
import time
from selenium  import webdriver

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_movies():
    f=open('data_movies2013.txt','a')
    start=1
    while start<8519:
        try:
            html=requests.get('http://www.imdb.com/search/title?at=0&sort=boxoffice_gross_us&start=%s&title_type=feature&year=2013,2013'%start,headers=headers,timeout=30).text
        except:
            continue
        items=parser(html)
        for item in items:
            f.write(item+'\n')
        start+=50
        print(start)

def parser(html):
    items=[]
    table=BeautifulSoup(html,'lxml').find('table',attrs={'class':'results'}).find_all('tr')[1:]
    for item in table:
        td=item.find('td',attrs={'class':'title'})
        title=item.find('a').get('title')
        try:
            score=td.find('span',attrs={'class':'rating-rating'}).get_text()
        except:
            score='-'
        try:
            col=item.find('td',attrs={'class':'sort_col'}).get_text()
        except:
            col='-'
        text=title+'||'+score+'||'+col
        items.append(text)
    return items

get_movies()
