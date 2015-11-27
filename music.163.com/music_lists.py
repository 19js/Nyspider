#coding:utf-8

import requests
from bs4 import BeautifulSoup
import sqlite3
import threading
import json

class Get_list_id():
    def __init__(self):
        self.urls={
            '华语':'http://music.163.com/discover/playlist/?order=hot&cat=%E5%8D%8E%E8%AF%AD&limit=35&offset=',
            '欧美':'http://music.163.com/discover/playlist/?order=hot&cat=%E6%AC%A7%E7%BE%8E&limit=35&offset=',
            '日语':'http://music.163.com/discover/playlist/?order=hot&cat=%E6%97%A5%E8%AF%AD&limit=35&offset=',
            '韩语':'http://music.163.com/discover/playlist/?order=hot&cat=%E9%9F%A9%E8%AF%AD&limit=35&offset='
            }
        self.headers = {
            'Host':"music.163.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            'Referer':"http://music.163.com/",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
    def run(self):
        threadings=[]
        for key in self.urls:
            work=threading.Thread(target=self.get_lists,args=(key,))
            threadings.append(work)
        for work in threadings:
            work.start()
        for work in threadings:
            work.join()

    def get_lists(self,key):
        f=open(key+'.txt','a')
        count=35
        while True:
            html=requests.get(self.urls[key]+str(count),headers=self.headers).text
            try:
                table=BeautifulSoup(html,'html.parser').find('ul',id='m-pl-container').find_all('li')
            except:
                break
            ids=[]
            for item in table:
                ids.append(item.find('div',attrs={'class':'bottom'}).find('a').get('data-res-id'))
            count+=35
            f.write(str(ids)+'\n')

def get_id(list_id):
    url='http://music.163.com/api/playlist/detail?id='+str(list_id)
    data=requests.get(url).text
    data=json.loads(data)['result']
    if(data['playCount']>500000):
        return data
    return []

if __name__=='__main__':
    threadings=[]
    f=open('华语.txt','r')
    file_d=open('data.txt','a')
    for line in f.readlines():
        for id in eval(line.replace('\n','')):
            data=get_id(id)
            if data==[]:
                continue
            file_d.write(str(data)+'\n')
            print(id)
