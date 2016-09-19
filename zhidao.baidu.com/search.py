import requests
from bs4 import BeautifulSoup
import time
import threading

headers = {
    'Host':"zhidao.baidu.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def search(key):
    html=requests.get('https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=utf-8&word='+key,headers=headers,timeout=30).text.encode('ISO-8859-1').decode('gbk','ignore')
    table=BeautifulSoup(html,'lxml').find('div',{'class':'list-wraper'}).find_all('dl')
    for dl in table:
        try:
            url=dl.find('a').get('href')
            if 'zhidao.baidu.com/question' in url:
                return url
        except:
            continue

class Search(threading.Thread):
    def __init__(self,key):
        super(Search,self).__init__()
        self.key=key

    def run(self):
        self.status=True
        try:
            self.url=search(self.key)
        except:
            self.status=False

def main():
    f=open('urls.txt','w')
    lines=[]
    count=0
    for line in open('./failed_words','r'):
        line=line.replace('\n','')
        lines.append(line)
        if len(lines)<5:
            continue
        threadings=[]
        for item in lines:
            work=Search(item)
            threadings.append(work)
        for work in threadings:
            work.start()
        for work in threadings:
            work.join()
        for work in threadings:
            if work.status==False:
                continue
            if work.url==None:
                continue
            count+=1
            print(count)
            try:
                f.write(work.key+"||"+work.url+'\n')
            except:
                continue
        lines.clear()
    threadings=[]
    for item in lines:
        work=Search(item)
        threadings.append(work)
    for work in threadings:
        work.start()
    for work in threadings:
        work.join()
    for work in threadings:
        if work.status==False:
            continue
        if work.url==None:
            continue
        count+=1
        print(count)
        f.write(work.key+"||"+work.url+'\n')
    lines.clear()
    f.close()
main()
