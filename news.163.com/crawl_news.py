import requests
from bs4 import BeautifulSoup
import re
import time
import json
import os
import threading
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

class CrawlNews(threading.Thread):
    def __init__(self,url):
        super(CrawlNews,self).__init__()
        self.url=url

    def run(self):
        filters=['http://tech.163.com/'
                ,'http://sports.163.com/'
                ,'http://ent.163.com/'
                ,'http://news.163.com/'
                ,'http://war.163.com/']
        self.status=True
        try:
            res=requests.get(self.url,headers=headers,timeout=5)
            if res.status_code==403 or res.status_code==404:
                self.status=False
            self.html=res.text.replace('gb2312','utf-8')
            table=BeautifulSoup(self.html,'lxml').find_all('a')
            self.urls=[]
            for item in table:
                try:
                    link=item.get('href')
                    if 'photo' in link or 'special' in link or 'product' in link or 'script' in link:
                        continue
                    flag=True
                    for filter_url in filters:
                        if filter_url in link:
                            flag=False
                            break
                    if flag:
                        continue
                    self.urls.append(link)
                except:
                    continue
        except Exception as e:
            print(e)
            self.status=False

def crawl():
    try:
        os.mkdir('result')
    except:
        pass
    start_url='http://news.163.com/'
    exists={}
    urls=['http://news.163.com/'
    ,'http://news.163.com/rank/',
    'http://news.163.com/domestic/',
    'http://news.163.com/world/',
    'http://news.163.com/shehui/',
    'http://war.163.com/',
    'http://tech.163.com/',
    'http://sports.163.com/'
            ,'http://ent.163.com/'
            ,'http://news.163.com/']
    news_num=1
    while(len(urls)):
        count=0
        tasks=[]
        while count<20:
            try:
                url=urls.pop()
                task=CrawlNews(url)
                task.setDaemon(True)
                tasks.append(task)
                count+=1
            except Exception as e:
                break
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        for task in tasks:
            if task.status==False:
                continue
            if '.163.com/1' in task.url or '.163.com/0' in task.url:
                f=open('result/%s.html'%news_num,'w')
                f.write(task.html)
                f.close()
                print(news_num,'OK')
                news_num+=1
            for link in task.urls:
                if link in exists:
                    continue
                urls.append(link)
                exists[link]=1
    f=open('exists.json','w')
    json.dump(json.dumps(exists),f)

crawl()
