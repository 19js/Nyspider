#coding:utf-8

import requests
from bs4 import BeautifulSoup
import time
import datetime
import os
import copy
import json

from suds.client import Client
import base64
import zlib


class Get_data():
    def __init__(self):
        self.headers = {
            'Host':"data.cma.cn",
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
        self.url='http://data.cma.cn/data/search.html?dataCode=A.0012.0001'
        self.session=requests.session()
        date=datetime.datetime.now().strftime("%Y-%m-%d ")
        hour=datetime.datetime.now().strftime("%H")
        sd_hour=int(hour)-18
        ed_hour=int(hour)-8
        if ed_hour>=0:
            if ed_hour<10:
                self.dateE=date+'0'+str(ed_hour)
            else:
                self.dateE=date+str(ed_hour)
        else:
            now_time = datetime.datetime.now()
            yes_time = now_time + datetime.timedelta(days=-1)
            yes_time_nyr = yes_time.strftime('%Y-%m-%d ')
            self.dateE=yes_time_nyr+str(24+ed_hour)
        if sd_hour>=0:
            if sd_hour<10:
                self.dateS=date+'0'+str(sd_hour)
            else:
                self.dateS=date+str(sd_hour)
        else:
            now_time = datetime.datetime.now()
            yes_time = now_time + datetime.timedelta(days=-1)
            yes_time_nyr = yes_time.strftime('%Y-%m-%d ')
            self.dateS=yes_time_nyr+str(24+sd_hour)
        print(self.dateS,self.dateE)
        self.failed=[]
        statue=False
        while not statue:
            statue=self.login()
            if not statue:
                print('Login failed')
            else:
                print('Login OK')

    def GetStrImg(self):
        image=open('captcha.png','rb').read()
        image=base64.b64encode(image)
        #image=base64.encodestring(zlib.compress(image))
        client=Client('http://yanzhengma.gotoip2.com/Service1.asmx?WSDL')
        data=client.service.GetStrImg(image.decode())
        return data

    def login(self):
        headers = {
            'Host':"data.cma.cn",
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
        try:
            url='http://data.cma.cn/user/toLogin.html'
            self.session.get(url,headers=headers)
            html=self.session.get('http://data.cma.cn/user/captcha/refresh/1.html',headers=headers).text
            imgurl='http://data.cma.cn/'+json.loads(html)['url']
            with open('captcha.png','wb') as img:
                imgcontent=self.session.get(imgurl,headers=headers).content
                img.write(imgcontent)
            imgstr=self.GetStrImg()
            data={
            'userName':'aikesubi@gmail.com',
            'password':'Satpi&b8',
            'verifyCode':imgstr
            }
        except:
            return False
        try:
            html=self.session.post('http://data.cma.cn/user/Login.html',data=data,headers=headers,timeout=30).text
            statue=json.loads(html)['status']
            if statue==100:
                return True
            else:
                return False
        except:
            return False

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
            #pass
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
            html=self.session.post(self.url,headers=self.headers,data=data,timeout=30).text
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
    work=Get_data()
    work.run()
