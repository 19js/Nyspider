#coding:utf-8

import requests
from bs4 import BeautifulSoup
import time
import xlwt3
import re
import threading
import datetime

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_products(page):
    statue=True
    while statue:
        try:
            html=requests.get('http://www.jfz.com/simu/list_p%s.html'%page,headers=headers,timeout=50).text
            statue=False
        except:
            continue
    rel='href="(/product.*?html)"'
    result=re.findall(rel,html)
    urls=[]
    for url in result:
        url='http://www.jfz.com'+url
        urls.append(url)
    return urls

class Product_Infor(threading.Thread):
    def __init__(self,url):
        super(Product_Infor,self).__init__()
        self.url=url

    def run(self):
        statue=True
        while statue:
            try:
                html=requests.get(self.url,headers=headers,timeout=50).text.encode('ISO-8859-1').decode('utf-8','ignore')
                statue=False
            except:
                continue
        soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'simu_prodetail_container'})
        baseInforTable=soup.find('div',attrs={'class':'simu_pro_info_wrap'}).find_all('li')
        self.name=baseInforTable[0].get_text().split('：')[-1]
        self.baseinfor=[]
        self.strategy=baseInforTable[-2].get_text().split('：')[-1].replace('\n','')
        for li in baseInforTable:
            self.baseinfor.append(li.get_text().split('：')[-1].replace('\n',''))
        pro_knowTable=soup.find('div',attrs={'class':'simu_pro_know_wrap'}).find_all('li')
        for li in pro_knowTable:
            self.baseinfor.append(li.get_text().split('：')[-1].replace('\n',''))
        try:
            table=soup.find('div',attrs={'class':'simu_pro_table_height'}).find('table').find_all('tr')
            self.history={}
            for tr in table:
                tds=tr.find_all('td')
                self.history[tds[0].get_text()]=tds[2].get_text()
        except:
            self.history={}

class Main():
    def __init__(self):
        self.label={'股票策略':1,'宏观策略':2,'管理期货':3,'事件驱动':4,'相对价值策略':5,'债券策略':6,'组合基金':7,'复合策略':8}
        self.sheet_table={'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0}
        self.col_table={'1':1,'2':1,'3':1,'4':1,'5':1,'6':1,'7':1,'8':1}
        self.excel_f=[]
        self.sheets=[]
        for num in range(8):
            excel=xlwt3.Workbook()
            self.excel_f.append(excel)
        for excel in self.excel_f:
            sheet=excel.add_sheet('0', cell_overwrite_ok=True)
            self.sheets.append(sheet)

    def run(self):
        page=1
        while page<=485:
            urls=get_products(page)
            threadings=[]
            for url in urls:
                work=Product_Infor(url)
                threadings.append(work)
            for work in threadings:
                work.setDaemon(True)
                work.start()
            for work in threadings:
                work.join()
            for work in threadings:
                try:
                    index=self.label[work.strategy]-1
                except:
                    index=2
                self.write(index,work.history,work.baseinfor)
            print(page,'----OK')
            page+=1
            if page%20==0:
                self.save()
        self.save()

    def write(self,index,history,baseinfor):
        col=self.col_table[str(index+1)]
        try:
            num=0
            for infor in baseinfor:
                self.sheets[index].write(num,col,infor)
                num+=1
            for key in history:
                try:
                    row=self.get_row(key)
                except:
                    continue
                if row>65533 or row<0:
                    continue
                self.sheets[index].write(row,col,history[key])
                self.sheets[index].write(row,0,key)
            self.col_table[str(index+1)]+=1
        except:
            self.col_table[str(index+1)]=1
            col=self.col_table[str(index+1)]
            self.sheet_table[str(index+1)]+=1
            self.sheets[index]=self.excel_f[index].add_sheet(str(self.sheet_table[str(index+1)]), cell_overwrite_ok=True)
            num=0
            for infor in baseinfor:
                self.sheets[index].write(num,col,infor)
                num+=1
            for key in history:
                try:
                    row=self.get_row(key)
                except:
                    continue
                if row>65533 or row<0:
                    continue
                self.sheets[index].write(row,col,history[key])
                self.sheets[index].write(row,0,key)
            self.col_table[str(index+1)]+=1

    def get_row(self,date):
        today=datetime.datetime.today()
        pre_day=datetime.datetime.strptime(date,'%Y.%m.%d')
        row=15+(today-pre_day).days
        return row

    def save(self):
        num=0
        for excel in self.excel_f:
            for key in self.label:
                if self.label[key]==num+1:
                    excel.save(key+'.xls')
            num+=1

main=Main()
main.run()
