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
    'Cookie':"showAdwh=1; city=sh; global_cookie=nixh0jr0n6xpgnczzvyrp3adm1migdj3hjt; __utma=147393320.210238066.1446201607.1446215723.1446218991.3; __utmz=147393320.1446201607.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; showAdsh=1; SoufunSessionID_Esf=3_1446206525_2155; unique_cookie=U_nixh0jr0n6xpgnczzvyrp3adm1migdj3hjt*31; __utmc=147393320; __utmb=147393320.39.10.1446218991; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

class Get_infor(threading.Thread):
    def __init__(self,url):
        super(Get_infor,self).__init__()
        self.url=url+'xiangqing/'

    def run(self):
        self.statue=1
        try:
            try:
                html=requests.get(self.url,headers=headers,timeout=30).text.encode('ISO-8859-1').decode('gbk','ignore')
            except:
                html=requests.get(self.url,headers=headers,timeout=30).text
            soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'leftinfo'})
            self.title=soup.find('span',attrs={'class':'floatl'}).get_text()
            print(self.title)
            pri_table=soup.find('dl',attrs={'class':'firstpic'}).find('dd',style='margin-top:10px;').find_all('span')
            self.price=pri_table[0].get_text()
            self.month_lilv=pri_table[1].get_text()
            self.lilv=pri_table[2].get_text()
            tables=soup.find('dl',attrs={'class':'lbox'}).find_all('dd')
            for item in tables:
                if item.find('strong').get_text()=='小区地址：':
                    self.address=item.get('title')
                if item.find('strong').get_text()=='所属区域：':
                    self.area=item.get('title')
                if item.find('strong').get_text()=='环线位置':
                    self.cell=item.get_text().replace('环线位置','')
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
                    self.hushu==item.get_text().replace('当期户数：','')
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
        urls.append(item.find('a').get('href'))
    return urls

class Main():
    def __init__(self):
        self.f=xlwt3.Workbook()
        self.sheet=self.f.add_sheet('sheet')
        self.count=0
    def run(self):
        for page in range(100):
            urls=get_urls('http://esf.sh.fang.com/housing/25__0_0_0_0_%s_0_0/'%(str(page+1)))
            for url in urls:
                work=Get_infor(url)
                work.run()
                if work.statue==0:
                    continue
                self.sheet.write(self.count,0,work.title)
                self.sheet.write(self.count,1,work.address)
                self.sheet.write(self.count,2,work.price)
                self.sheet.write(self.count,3,work.month_lilv)
                self.sheet.write(self.count,4,work.lilv)
                self.sheet.write(self.count,5,work.area)
                self.sheet.write(self.count,6,work.cell)
                self.sheet.write(self.count,7,work.wuye)
                self.sheet.write(self.count,8,work.date)
                self.sheet.write(self.count,9,work.jiegou)
                self.sheet.write(self.count,10,work.type)
                self.sheet.write(self.count,11,work.mianji)
                self.sheet.write(self.count,12,work.ground)
                self.sheet.write(self.count,13,work.hushu)
                self.sheet.write(self.count,14,work.green)
                self.sheet.write(self.count,15,work.rongji)
                self.sheet.write(self.count,16,work.wuye_price)
                self.sheet.write(self.count,17,work.url)
                self.count+=1
                self.f.save('浦东.xls')
                print(self.count)
            '''
            threadings=[]
            for url in urls:
                work=Get_infor(url)
                threadings.append(work)
            for work in threadings:
                work.run()
            for work in threadings:
                work.join()
            for work in threadings:
                if work.statue==0:
                    continue
                self.sheet.write(self.count,0,work.title)
                self.sheet.write(self.count,1,work.address)
                self.sheet.write(self.count,2,work.price)
                self.sheet.write(self.count,3,work.month_lilv)
                self.sheet.write(self.count,4,work.lilv)
                self.sheet.write(self.count,5,work.area)
                self.sheet.write(self.count,6,work.cell)
                self.sheet.write(self.count,7,work.wuye)
                self.sheet.write(self.count,8,work.date)
                self.sheet.write(self.count,9,work.jiegou)
                self.sheet.write(self.count,10,work.type)
                self.sheet.write(self.count,11,work.mianji)
                self.sheet.write(self.count,12,work.ground)
                self.sheet.write(self.count,13,work.hushu)
                self.sheet.write(self.count,14,work.green)
                self.sheet.write(self.count,15,work.rongji)
                self.sheet.write(self.count,16,work.wuye_price)
                self.sheet.write(self.count,17,work.url)
                self.count+=1
                print(self.count)
            '''

if __name__=='__main__':
    work=Main()
    work.run()
