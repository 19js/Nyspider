#coding:utf-8
import requests
from bs4 import BeautifulSoup
import xlwt3
import xlrd
import threading


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
class Get_infor(threading.Thread):
    def __init__(self,name):
        super(Get_infor,self).__init__()
        self.name=name
        self.url='http://finance.yahoo.com/q?s='+name
    def run(self):
        try:
            html=requests.get(self.url,headers=headers,timeout=30).text
            table=BeautifulSoup(html).find('table',id='table1').find_all('tr')
            self.infor={}
            for item in table:
                if item.find('th').get_text()=='Beta:':
                    self.infor['Beta']=item.find('td').get_text()
            table=BeautifulSoup(html).find('table',id='table2').find_all('tr')
            for item in table:
                if item.find('th').get_text()[0]=='P':
                    self.infor['PE']=item.find('td').get_text()
        except:
            self.infor={}
            self.infor['Beta']=''
            self.infor['PE']=''

class Main():
    def __init__(self):
        self.f=xlwt3.Workbook()
        self.sheet=self.f.add_sheet('sheet')
        self.count=0
    def run(self):
        file=open('data.txt','r')
        items=[]
        for line in file:
            data=line.strip().split(' ')
            items.append(data[1])
            if len(items)<10:
                continue
            threadings=[]
            for item in items:
                work=Get_infor(item)
                threadings.append(work)
            for work in threadings:
                work.run()
            for work in threadings:
                self.sheet.write(self.count,0,work.name)
                self.sheet.write(self.count,1,work.infor['Beta'])
                self.sheet.write(self.count,2,work.infor['PE'])
                self.count+=1
            self.f.save('data2.xls')
            items=[]
            print(self.count)


work=Main()
work.run()
