#coding:utf-8

import requests
import threading
import os

class Qiandao(threading.Thread):
    def __init__(self,username,passwd):
        super(Qiandao,self).__init__()
        self.login_url='https://reg.163.com/logins.jsp'
        self.qian_url='http://dtws-fps.webapp.163.com/api_web/daily_sign?callback=jQuery16402961158982616814_1445990653586&_=1445990680677'
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
        self.data={
        'username':username,
        'password':passwd,
        'url':"http://asynclogin.webapp.163.com/url.html",
        'url2':"http://asynclogin.webapp.163.com/url.html",
        'product':"163",
        'type':"1",
        'savelogin':"0",
        'noRedirect':"1"
        }
        self.session=requests.session()

    def run(self):
        self.session.post(self.login_url,data=self.data,headers=self.headers)
        html=self.session.get(self.qian_url,headers=self.headers).text
        print(html)
class Main(object):
    """docstring for Main"""
    def __init__(self):
        self.f=open('data.txt','r')

    def run(self):
        lists=[]
        for line in self.f:
            item=line.split('----')
            lists.append(item)
        users=[]
        for item in lists:
            users.append(item)
            if len(users)<100:
                continue
            self.qiandao(users)
            users=[]
        self.qiandao(users)

    def qiandao(self,items):
        threadings=[]
        for item in items:
            work=Qiandao(item[0],item[1].replace('\n',''))
            threadings.append(work)
        for work in threadings:
            work.run()
        for work in threadings:
            work.start()
        for work in threadings:
            work.join()


if __name__=='__main__':
    work=Main()
    work.run()
