#coding:utf-8

import requests
from bs4 import BeautifulSoup
import xlwt3
import threading


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

class Get_infor(threading.Thread):
    def __init__(self,url):
        super(Get_infor,self).__init__()
        self.url=url.replace('esf/','')+'xiangqing/'
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
    def run(self):
        self.statue=1
        try:
            try:
                print(self.url)
                html=requests.get(self.url,headers=self.headers,timeout=30).text.encode('ISO-8859-1').decode('gbk','ignore')
            except:
                html=requests.get(self.url,headers=self.headers,timeout=30).text
            soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'leftinfo'})
            self.title=soup.find('span',attrs={'class':'floatl'}).get_text()
            pri_table=soup.find('dl',attrs={'class':'firstpic'}).find('dd',style='margin-top:10px;').find_all('span')
            self.price=pri_table[0].get_text()
            self.month_lilv=pri_table[1].get_text()
            self.lilv=pri_table[2].get_text()
            tables=soup.find('dl',attrs={'class':'lbox'}).find_all('dd')
            self.ground=' '
            self.address=' '
            self.area=' '
            self.cell=' '
            self.wuye=' '
            self.date=' '
            self.jiegou=' '
            self.type=' '
            self.mianji=' '
            self.ground=' '
            self.hushu=' '
            self.green=' '
            self.rongji=' '
            self.wuye_price=' '
            for item in tables:
                if item.find('strong').get_text()=='小区地址：':
                    self.address=item.get('title')
                if item.find('strong').get_text()=='所属区域：':
                    self.area=item.get_text().replace('所属区域：','')
                if item.find('strong').get_text()=='环线位置':
                    self.cell=item.get_text().replace('环线位置:','')
                if item.find('strong').get_text()=='物业类别：':
                    self.wuye=item.get_text().replace('物业类别：','')
                if item.find('strong').get_text()=='竣工时间：':
                    self.date=item.get_text().replace('竣工时间：','')
                if item.find('strong').get_text()=='建筑结构：':
                    self.jiegou=item.get_text().replace('建筑结构：','')
                if item.find('strong').get_text()=='建筑类别：':
                    self.type=item.get_text().replace('建筑类别：','')
                if item.find('strong').get_text()=='建筑面积：':
                    self.mianji=item.get_text().replace('建筑面积：','')
                if item.find('strong').get_text()=='占地面积：':
                    self.ground=item.get_text().replace('占地面积：','')
                if item.find('strong').get_text()=='当期户数：':
                    self.hushu=item.get_text().replace('当期户数：','')
                if item.find('strong').get_text()=='绿 化 率：':
                    self.green=item.get_text().replace('绿 化 率：','')
                if item.find('strong').get_text()=='容 积 率：':
                    self.rongji=item.get_text().replace('容 积 率：','')
                if item.find('strong').get_text()=='物 业 费：':
                    self.wuye_price=item.get_text().replace('物 业 费：','')
        except:
            self.statue=0

def get_urls(url):
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'houseList'}).find_all('div',id='Div1')
    urls=[]
    for item in table:
        urls.append(item.find('div',attrs={'class':'img rel floatl'}).find('a').get('href'))
    return urls

class Main():
    def __init__(self):
        self.f=open('data.txt','w')
        self.count=0
    def run(self):
        for page in range(80):
            urls=get_urls('http://esf.sh.fang.com/housing/18__0_0_0_0_%s_0_0/'%(str(page+1)))
            for url in urls:
                work=Get_infor(url)
                work.run()
                if work.statue==0:
                    continue
                infor=work.title+'|'+work.address+'|'+work.price+'|'+work.month_lilv+'|'+work.lilv+"|"+work.area+'|'+work.cell+'|'+work.wuye+'|'+work.date+'|'+work.jiegou+'|'+work.type+'|'+work.mianji+'|'+work.ground+'|'+work.hushu+'|'+work.green+"|"+work.rongji+'|'+work.wuye_price+'|'+work.url+'\n'
                self.f.write(infor)
                self.count+=1
                print(self.count)

if __name__=='__main__':
    work=Main()
    work.run()
