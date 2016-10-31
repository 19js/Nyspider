#coding:utf-8

import requests
from bs4 import BeautifulSoup
import xlwt3
import os
import jieba.analyse
import re
import threading

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}


def get_urls(html):
    rel='href="(.*?)"'
    results=re.findall(rel,html)
    urls=[]
    for url in results:
        if url.endswith('js') or url.endswith('css') or url.startswith('http://www.xidian.edu.cn') or url.endswith('jpg') or 'java' in url or '@' in url or 'php' in url:
            continue
        if  not url.startswith('http'):
            url='http://news.fudan.edu.cn/'+url
        if not url.startswith('http://news.fudan.edu.cn/'):
            continue
        urls.append(url)
    urls=list(set(urls))
    return urls

def get_keywords(text):
    results=jieba.analyse.textrank(text, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v','adj'))
    text=''
    for item in results:
        text+=item+';'
    return text

class Infor(threading.Thread):
    def __init__(self,url):
        super(Infor,self).__init__()
        self.url=url

    def run(self):
        self.statue=True
        try:
            self.html=requests.get(self.url,headers=headers,timeout=40).text.encode('ISO-8859-1').decode('utf-8','ignore')
            self.parser(self.html)
        except:
            self.statue=False

    def parser(self,html):
        date_re='发布时间：(\d+-\d+-\d+)'
        comefrom_re='来源：(.*?)<'
        author_re='作者：(.*?)<'
        soup=BeautifulSoup(html,'lxml')
        self.title=soup.title.get_text()
        try:
            self.body=soup.find('div',id='main').get_text()
        except:
            self.body=soup.get_text()
        try:
            self.author=re.findall(author_re,html)[0]
        except:
            self.author=''
        try:
            self.date=re.findall(date_re,self.body)[0]
        except:
            self.date=''
        try:
            self.comefrom=re.findall(comefrom_re,html)[0]
        except:
            self.comefrom=''
        self.keywords=get_keywords(self.body)
        self.urls=get_urls(html)

def main():
    excel=xlwt3.Workbook()
    sheet=excel.add_sheet('sheet')
    queue=[]
    urls=['http://news.fudan.edu.cn']
    exists_urls=[]
    count=0
    try:
        os.mkdir('fudan')
    except:
        print('Exists')
    while len(urls):
        url=urls.pop()
        if url in exists_urls:
            continue
        exists_urls.append(url)
        work=Infor(url)
        queue.append(work)
        if len(urls)>0 and len(queue)<20:
            continue
        for work in queue:
            work.start()
        for work in queue:
            work.join()
        while len(queue):
            work=queue.pop()
            if work.statue:
                if work.title=='404 Not Found':
                    continue
                sheet.write(count,0,count)
                sheet.write(count,1,work.url)
                sheet.write(count,2,work.title)
                sheet.write(count,3,work.date)
                sheet.write(count,4,work.author)
                sheet.write(count,5,work.comefrom)
                sheet.write(count,6,work.body)
                text=''
                for item in work.urls:
                    text+=item+';'
                sheet.write(count,7,text)
                sheet.write(count,8,work.keywords)
                urls+=work.urls
                with open('fudan/'+str(count)+'.html','w') as f:
                    f.write(work.html)
                del work
                count+=1
            excel.save('fudan.xls')
        print(count)
        if count>1500:
            break

main()
