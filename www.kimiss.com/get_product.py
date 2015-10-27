#coding:utf-8

from bs4 import BeautifulSoup
import requests
import xlwt3
import threading
from  Nyspider import *

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_type_urls():
    html=requests.get('http://product.kimiss.com/catalog/',headers=headers).text.encode('ISO-8859-1').decode('utf-8','ignore')
    tables=BeautifulSoup(html).find('div',attrs={'class':'f_c_list'}).find_all('div',attrs={'class':'f_c_div'})
    mantable=tables[2].find_all('dl')
    f=open('man.txt','w')
    for item in mantable:
        urls=[]
        for i in item.find('dd').find_all('span'):
            try:
                url=i.find('a').get('href')+'product-mostcomment-0-0-0-1.html'
                urls.append(url)
            except:
                continue
        infor={}
        infor[item.find('dt').get_text()]=urls
        f.write(str(infor)+'\n')
    mantable=tables[3].find_all('dl')
    f=open('baby.txt','w')
    for item in mantable:
        urls=[]
        for i in item.find('dd').find_all('span'):
            try:
                url=i.find('a').get('href')+'product-mostcomment-0-0-0-1.html'
                urls.append(url)
            except:
                continue
        infor={}
        infor[item.find('dt').get_text()]=urls
        f.write(str(infor)+'\n')

def get_product_urls(url):
    urls=[]
    page=1
    while True:
        html=get_html(url+'product-mostcomment-0-0-0-'+str(page)+'.html').encode('ISO-8859-1').decode('utf-8','ignore')
        try:
            table=BeautifulSoup(html).find('div',attrs={'class':'f_mouth_con'}).find('ul').find_all('li')
        except:
            break
        for item in table:
            urls.append(item.find('a').get('href'))
        page+=1
    return urls

def product_urls():
    f=open('baby.txt','r').read()
    f_write=open('baby_pro.txt','w')
    for line in f.split('\n'):
        try:
            dicts=eval(line)
        except:
            continue
        for key in dicts:
            urls=[]
            for url in dicts[key]:
                urls+=get_product_urls(url)
            infor={}
            infor[key]=urls
            f_write.write(str(infor)+'\n')
            print(key)

class Get_product(threading.Thread):
    def __init__(self,url):
        super(Get_product,self).__init__()
        self.url=url
    def run(self):
        self.statue=1
        try:
            try:
                html=requests.get(self.url,headers=headers,timeout=20).text.encode('ISO-8859-1').decode('utf-8','ignore')
            except:
                html=requests.get(self.url,headers=headers,timeout=20).text
            soup=BeautifulSoup(html,'lxml')
            self.pinpai=soup.find('h2').get_text()
            table=soup.find('div',attrs={'class':'c1_left_1'})
            image_url=table.find('div',id='preview').find('img').get('src')
            table=table.find('div',attrs={'class':'preview_r'})
            self.image=requests.get(image_url,headers=headers,timeout=20).content
            self.title=table.find('div',attrs={'class':'preview_title'}).find('h1').get_text().replace('\n','').replace(' ','')
            self.pri_type=table.find('div',attrs={'class':'preview_brief'}).get_text().replace('\r\n','').replace(' ','')
            lists=table.find('div',attrs={'class':'previewD'}).find('ul').find_all('li')
            self.pinlei=''
            self.gongxiao=''
            for item in lists:
                if item.get_text()[2]=='品':
                    self.pinlei=item.find('a').get_text()
                if item.get_text()[2]=='功':
                    self.gongxiao=item.get_text()
            self.infor=table.find('div',attrs={'class':'previewE'}).get_text().replace(' ','')
        except:
            self.statue=0


class Main():
    def __init__(self):
        self.f=xlwt3.Workbook()
        self.sheet=self.f.add_sheet('sheet')
        self.count=0
    def run(self):
        f=open('baby_pro.txt','r').read()
        for item in f.split('\n'):
            try:
                dicts=eval(item)
            except:
                continue
            for key in dicts:
                urls=[]
                for url in dicts[key]:
                    urls.append(url)
                    if len(urls)<15:
                        continue
                    self.get(key,urls)
                    urls=[]
                self.get(key,urls)

    def get(self,key,urls):
        threadings=[]
        for url in urls:
            work=Get_product(url)
            threadings.append(work)
        for work in threadings:
            work.start()
        for work in threadings:
            work.join()
        for work in threadings:
            if work.statue==0:
                continue
            with open('baby_image/BABYHZP'+str(self.count+1)+'.jpg','wb') as f:
                f.write(work.image)
                f.close()
            self.sheet.write(self.count,0,self.count+1)
            self.sheet.write(self.count,1,'baby')
            self.sheet.write(self.count,2,key)
            self.sheet.write(self.count,3,work.pinlei)
            self.sheet.write(self.count,4,work.gongxiao)
            self.sheet.write(self.count,5,work.pinpai)
            self.sheet.write(self.count,6,work.title)
            self.sheet.write(self.count,7,work.pri_type)
            self.sheet.write(self.count,8,'BABYHZP'+str(self.count+1))
            self.sheet.write(self.count,9,work.infor)
            self.count+=1
            print(self.count)
        self.f.save('baby.xls')

#work=Get_product('http://product.kimiss.com/product/49053/')
work=Main()
work.run()
