import requests
from bs4 import BeautifulSoup
import time
import threading

headers = {
    'Host':"zhidao.baidu.com",
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
            self.data=self.question()
        except:
            self.status=False

    def question(self):
        html=requests.get(self.url,headers=headers,timeout=30).text.encode('ISO-8859-1').decode('gbk','ignore')
        table=BeautifulSoup(html,'lxml').find('article',id='qb-content')
        header=table.find('div',id='wgt-ask')
        title=header.find('span',{'class':'ask-title'}).get_text()
        try:
            des=header.find('span',{'class':'con'}).get_text()
        except:
            des='-'
        try:
            answer=table.find('div',{'class':['bd','answer']}).find('pre').get_text()
        except:
            try:
                answer=table.find('div',{'id':'wgt-answers'}).find('span',{'class':'con'}).get_text()
            except:
                answer='-'
        return [title,des,answer]

def main():
    f=open('result.txt','a')
    lines=[]
    count=0
    for line in open('./urls.txt','r'):
        line=line.replace('\n','')
        lines.append(line)
        if len(lines)<10:
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

main()
