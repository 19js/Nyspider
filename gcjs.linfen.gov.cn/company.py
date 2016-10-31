import requests
from bs4 import BeautifulSoup
import threading
import time

headers = {
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}

def get_urls():
    page=1
    while True:
        url='http://gcjs.linfen.gov.cn/shanxisheng/listdw/zhucehao//xinyongdengji//qiyename//p/%s.php'
        try:
            html=requests.get(url%page,headers=headers).text.encode('iso-8859-1').decode('gbk','ignore')
        except:
            continue
        try:
            table=BeautifulSoup(html,'lxml').find('table',{'width':'940'}).find_all('tr')
        except:
            continue
        f=open('urls.txt','a')
        for item in table:
            try:
                name=item.find('a').get_text().replace('\r','').replace('\n','').replace(' ','').replace('\xa0','')
                url='http://gcjs.linfen.gov.cn/'+item.find('a').get('href')
                f.write(name+'|'+url+'\n')
            except:
                continue
        f.close()
        print(page)
        page+=1
        if page==5515:
            break

def get_contact(url):
    html=requests.get(url,headers=headers,timeout=30).text.encode('iso-8859-1').decode('gbk','ignore')
    table=BeautifulSoup(html,'lxml').find('table',{'class':'tdata'}).find_all('tr',{'class':'a1'})
    data={}
    for item in table:
        try:
            keys=item.find_all('h5')
            values=item.find_all('td',{'class':'tinput'})
            for i in range(len(keys)):
                key=keys[i].get_text().replace('\r','').replace('\n','').replace(' ','').replace('：','')
                value=values[i].get_text().replace('\r','').replace('\n','').replace(' ','')
                data[key]=value
        except:
            continue
    result=''
    for key in ['法定代表人','联系电话','住所']:
        try:
            result+=' |'+data[key]
        except:
            result+=' |'
    return result

class Crawler(threading.Thread):
    def __init__(self,infor):
        super(Crawler,self).__init__()
        self.infor=infor

    def run(self):
        self.flag=True
        try:
            self.result=get_contact(self.infor.split('|')[-1])
        except:
            self.flag=False

def load_urls():
    items=[]
    for line in open('urls.txt','r'):
        line=line.replace('\n','')
        items.append(line)
    return items

def company_infor():
    items=load_urls()
    num=0
    while len(items):
        threadings=[]
        count=0
        while count<10:
            try:
                item=items.pop()
                crawler=Crawler(item)
                crawler.setDaemon(True)
                threadings.append(crawler)
                count+=1
            except:
                break
        for work in threadings:
            work.start()
        for work in threadings:
            work.join()
        f=open('result.txt','a')
        for work in threadings:
            if work.flag==False:
                failed=open('failed.txt','a')
                failed.write(work.infor+'\n')
                failed.close()
                continue
            num+=1
            f.write(str(work.infor+work.result)+'\n')
        print(num,'ok')
        f.close()

get_urls()
company_infor()
