#coding:utf-8
import requests
from bs4 import BeautifulSoup
import xlwt3



headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_infor(name):
    url='http://finance.yahoo.com/q?s='+name
    try:
        html=requests.get(url,headers=headers).text
        table=BeautifulSoup(html).find('table',id='table1').find_all('tr')
        infor={}
        for item in table:
            if item.find('th').get_text()=='Beta:':
                infor['Beta']=item.find('td').get_text()
        table=BeautifulSoup(html).find('table',id='table2').find_all('tr')
        for item in table:
            if item.find('th').get_text()[0]=='P':
                infor['PE']=item.find('td').get_text()
        return infor
    except:
        infor={}
        infor['Beta']=''
        infor['PE']=''
        return infor

class Main():
    def __init__(self):
        self.f=xlwt3.Workbook()
        self.sheet=self.f.add_sheet('sheet')
        self.count=0
    def run(self):
        file=open('data.txt','r')
        for line in file:
            data=line.strip().split(' ')
            infor=get_infor(data[1])
            self.sheet.write(self.count,0,data[1])
            self.sheet.write(self.count,1,infor['Beta'])
            self.sheet.write(self.count,2,infor['PE'])
            self.count+=1
            self.f.save('data.xls')
            print(self.count)

work=Main()
work.run()
