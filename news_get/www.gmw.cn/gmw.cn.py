import requests
from bs4 import BeautifulSoup
import time
import re
import threading


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def search():
    url='http://zhannei.baidu.com/cse/search?q=%E7%81%BE%E5%90%8E%E9%87%8D%E5%BB%BA&p={}&s=6995449224882484381'
    page=0
    while True:
        try:
            html=requests.get(url.format(page),headers=headers,timeout=30).text.encode('iso-8859-1').decode('utf-8','ignore')
        except:
            print(page,'failed')
            continue
        try:
            table=BeautifulSoup(html,'lxml').find('div',{'id':'results'}).find_all('div',{'class':'result'})
        except:
            break
        if len(table)==0:
            break
        f=open('urls.txt','a')
        for ul in table:
            try:
                title=ul.find('a').get_text()
                news_url=ul.find('a').get('href')
            except:
                continue
            try:
                date=re.findall('(\d+-\d+-\d+)',str(ul))[0]
            except:
                date='-'
            f.write(str([title,date,news_url])+'\n')
        f.close()
        print(page,'ok')
        if page==74:
            break
        page+=1

def news_content(url):
    html=requests.get(url,headers=headers,timeout=30).text.encode('iso-8859-1').decode('utf-8','ignore')
    soup=BeautifulSoup(html,'lxml')
    ok=False
    try:
        text=soup.find('div',{'id':'contentMain'}).get_text()
        ok=True
    except:
        pass
    if not ok:
        try:
            text=soup.find('div',{'id':'ArticleContent'}).get_text()
            ok=True
        except:
            pass
    if not ok:
        try:
            text=soup.find('div',{'id':'articleContent'}).get_text()
            ok=True
        except:
            pass
    '''
    if not ok:
        try:
            text=soup.find('div',{'class':'text_show'}).get_text()
            ok=True
        except:
            pass
    if not ok:
        try:
            text=soup.find('div',{'class':'text_box'}).get_text()
            ok=True
        except:
            pass
    if not ok:
        try:
            text=soup.find('body').get_text()
            ok=True
        except:
            pass
    '''
    return text

class NewsGet(threading.Thread):
    def __init__(self,infor):
        super(NewsGet,self).__init__()
        self.infor=infor
        self.url=self.infor[-1]

    def run(self):
        self.ok=True
        try:
            text=news_content(self.url)
            if text!=False:
                self.infor.append(text)
            else:
                self.ok=False
        except:
            self.ok=False

def load_urls():
    items=[]
    for line in open('./urls.txt','r'):
        item=eval(line)
        items.append(item)
        if len(items)==10:
            yield items
            items.clear()
        else:
            continue
    yield items

def main():
    #search()
    count=0
    for items in load_urls():
        threadings=[]
        for item in items:
            work=NewsGet(item)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()
        for work in threadings:
            work.join()
        f=open('result.txt','a')
        for work in threadings:
            if work.ok==False:
                failed=open('failed.txt','a')
                failed.write(str(work.infor)+'\n')
                failed.close()
                continue
            f.write(str(work.infor)+'\n')
            count+=1
        f.close()
        print(count,'ok')

main()
