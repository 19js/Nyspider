import requests
from bs4 import BeautifulSoup
import time
import threading
from selenium import webdriver
import random

headers = {
    'Host':"wenda.so.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

class Ques(threading.Thread):
    def __init__(self,line):
        super(Ques,self).__init__()
        self.line=line
        self.url=line.split('||')[-1]
        self.word=line.split('||')[0]

    def run(self):
        self.status=True
        try:
            self.data=question(self.url)
        except:
            self.status=False

def thread():
    f=open('result.txt','a')
    lines=[]
    count=0
    for line in open('./urls.txt','r'):
        line=line.replace('\n','')
        lines.append(line)
        if len(lines)<5:
            continue
        threadings=[]
        for item in lines:
            work=Ques(item)
            threadings.append(work)
        for work in threadings:
            work.start()
        for work in threadings:
            work.join()
        for work in threadings:
            if work.status==False:
                failed=open('question_failed','a')
                failed.write(work.line+'\n')
                failed.close()
                continue
            count+=1
            print(count)
            f.write(str([work.word]+work.data)+'\n')
        lines.clear()
    threadings=[]
    for item in lines:
        work=Ques(item)
        threadings.append(work)
    for work in threadings:
        work.start()
    for work in threadings:
        work.join()
    for work in threadings:
        if work.status==False:
            failed=open('question_failed','a')
            failed.write(work.line+'\n')
            failed.close()
            continue
        f.write(str([work.word]+work.data)+'\n')
    f.close()

browser=webdriver.Firefox()
browser.get('http://wenda.so.com')

def question(url,proxies):
    #html=requests.get(url,headers=headers,proxies=proxies,timeout=30).text.encode('ISO-8859-1').decode('utf-8','ignore')
    #print(html)
    browser.get(url)
    browser.find_element_by_class_name('resolved-cnt')
    time.sleep(1)
    html=browser.page_source
    table=BeautifulSoup(html,'lxml').find('div',id='js-detail')
    header=table.find('div',{'class':'mod-q'})
    title=header.find('h2',{'class':'title'}).get_text()
    try:
        des=header.find('div',{'class':'q-cnt'}).get_text()
    except:
        des='-'
    try:
        answer=table.find('div',{'class':'resolved-cnt'}).get_text()
    except:
        try:
            answer=table.find('div',{'class':'answers'}).find('div',{'class':'other-ans-cnt'}).get_text()
        except:
            answer='-'
    return [title,des,answer]

def get_proxy():
    html=requests.get('http://115.159.49.85:9000/?page=1&num=300').text
    data=eval(html)
    index=random.randint(0,len(data)-1)
    ip=data[index]['ip']
    return {'http':'http://'+ip}

def main():
    count=0
    for line in open('./failed_urls','r'):
        #proxies=get_proxy()
        proxies=''
        line=line.replace('\n','')
        try:
            data=question(line.split('||')[-1],proxies)
        except:
            failed=open('question_failed','a')
            print('failed')
            failed.write(line+'\n')
            failed.close()
            continue
        time.sleep(1)
        f=open('result.txt','a')
        word=line.split('||')[0]
        f.write(str([word]+data)+'\n')
        print(word,'ok')
        f.close()

main()
