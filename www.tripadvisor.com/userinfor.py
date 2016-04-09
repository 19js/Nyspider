#coding:utf-8

import requests
from bs4 import BeautifulSoup
import threading


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate'}


class Infor(threading.Thread):
    def __init__(self,line):
        super(Infor,self).__init__()
        self.line=line
        self.uid=self.line.split('||')[1].split('-')[0].replace('UID_','')

    def run(self):
        try:
            html=requests.get('https://www.tripadvisor.com/MemberOverlay?uid=%s&c=&fus=false&partner=false&LsoId='%self.uid,headers=headers,timeout=50).text
        except:
            self.result='--'
            self.line+='||'+self.result
            return
        try:
            self.result=BeautifulSoup(html,'lxml').find('ul',attrs={'class':'memberdescription'}).find_all('li')[1].get_text().replace('\r','').replace('\n','')
        except:
            self.result='--'
        self.line+='||'+self.result


def main():
    f=open('re_data.txt','a')
    threadings=[]
    lines=[]
    count=0
    for line in open('result.txt','r'):
        line=line.replace('\n','')
        lines.append(line)
        if(len(lines)<20):
            continue
        for line in lines:
            work=Infor(line)
            threadings.append(work)
        for work in threadings:
            work.start()
        for work in threadings:
            work.join()
        for work in threadings:
            f.write(work.line+'\n')
        count+=1
        print(count,'--ok')
        threadings.clear()
        lines.clear()

main()
