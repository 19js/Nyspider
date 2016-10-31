#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re
import threading

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

class Score(threading.Thread):
    def __init__(self,line):
        super(Score,self).__init__()
        self.line=line
        self.name=self.line.split('||')[0]

    def run(self):
        try:
            self.score=self.get_score(self.name)
        except:
            self.score='-'
        print(self.score)
        self.line=self.line+'||'+self.score

    def get_score(self,name):
        try:
            html=requests.get('http://www.rottentomatoes.com/search/?search=%s'%name.replace(' ','+'),headers=headers,timeout=40).text
        except:
            return self.get_score(name)
        try:
            table=BeautifulSoup(html,'lxml').find('ul',id='movie_results_ul').find_all('li')
        except:
            return score(html)
        url=''
        for li in table:
            title=li.find('div',attrs={'class':'nomargin media-heading bold'}).get_text().replace('\r','').replace('\n','').replace(' ','')
            if title.lower()==name.replace(' ','').lower():
                url='http://www.rottentomatoes.com'+li.find('a').get('href')
                break
        if(url==''):
            return '-'
        html=requests.get(url,headers=headers,timeout=40).text
        return score(html)

def score(html):
    text=BeautifulSoup(html,'lxml').find('div',id='scorePanel').get_text().replace('\r','').replace('\n','').replace(' ','')
    rel='AverageRating:(.*?)R'
    try:
        result=re.findall(rel,text)[0]
        return result
    except:
        return '-'


def main():
    f=open('movies_2013.txt','a')
    items=[]
    for line in open('data_movies2013.txt','r').readlines():
        line=line.replace('\n','')
        items.append(line)
        if(len(items)<40):
            continue
        threadings=[]
        for item in items:
            work=Score(item)
            threadings.append(work)
        for work in threadings:
            work.start()
        for work in threadings:
            work.join()
        for work in threadings:
            f.write(work.line+'\n')
        items=[]
        threadings=[]

    for item in items:
        work=Score(item)
        threadings.append(work)
    for work in threadings:
        work.start()
    for work in threadings:
        work.join()
    for work in threadings:
        f.write(work.line+'\n')
    f.close()

main()
