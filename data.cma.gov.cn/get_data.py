#coding:utf-8

import requests
from bs4 import BeautifulSoup
import time
import datetime
import os
import copy

class Get_data():
    def __init__(self):
        self.headers = {
            'Host':"data.cma.gov.cn",
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Cookie':"PHPSESSID=691mi3b3clbs8quddk4tfdmgc2; userLoginKey=3918efe8092ff7cec78d6bae7d957ec7; trueName=%E7%94%B0%E5%86%9B; userName=D7BAB9E7B4C031BA73D2CB5A9405258A",
            'Connection': 'keep-alive'}
        self.url='http://data.cma.gov.cn/data/search.html?dataCode=A.0012.0001'
        date=datetime.datetime.now().strftime("%Y-%m-%d")
        self.dateS=date+' 00'
        self.dateE=date+' 23'
        self.failed=[]
        self.login()

    def login(self):
        headers = {
            'Host':"data.cma.gov.cn",
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
        url='http://data.cma.gov.cn/user/Login.html'
        data={
        'userName':'aikesubi@gmail.com',
        'password':'Satpi&b8'
        }
        try:
            html=requests.post(url,data=data,headers=headers,timeout=30).text
        except:
            return
            
    def run(self):
        try:
            os.mkdir('data')
        except:
            print('...')
        f_txt=open('data.txt','r')
        lines=f_txt.readlines()
        for line in lines:
            self.get_data(line.replace('\n',''))
        self.get_failed(self.failed)

    def get_failed(self,failed):
        lists=copy.copy(failed)
        for code in lists:
            self.get_data(code)

    def get_data(self,code):
        data={
        'dateS':self.dateS,
        'dateE':self.dateE,
        'hidden_limit_timeRange':'7',
        'hidden_limit_timeRangeUnit':'Day',
        'isRequiredHidden[]':['dateE','dateS','station_ids[]'],
        'station_ids[]':code,
        'select':'on',
        'elements[]':['PRS','PRS_Sea','PRS_Max','PRS_Min','WIN_S_Max','WIN_S_Inst_Max','WIN_D_INST_Max','WIN_D_Avg_10mi','WIN_S_Avg_10mi','WIN_D_S_Max','TEM','TEM_Max','TEM_Min','RHU','VAP','RHU_Min','PRE_1h'],
        'isRequiredHidden[]':'elements[]',
        'dataCode':'A.0012.0001',
        'dataCodeInit':'A.0012.0001'}
        try:
            html=requests.post(self.url,headers=self.headers,data=data,timeout=30).text
            table=BeautifulSoup(html,'html.parser').find('div',id='divSearchData').find('table').find_all('tr')
        except:
            self.failed.append(code)
            return
        f_txt=open('data/'+code+'.txt','a')
        for item in table[1:]:
            text=''
            for td in item.find_all('td')[1:]:
                text+=td.get_text().replace('\r\n','').replace(' ','')+'\t'
            text+='\n'
            f_txt.write(text)
        f_txt.close()
        print(code+'---ok')

if __name__=='__main__':
    sleep_time=input('输入间隔时间(小时)：')
    while True:
        work=Get_data()
        work.run()
        time.sleep(float(sleep_time)*3600)
