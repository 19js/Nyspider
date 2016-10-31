import requests
from bs4 import BeautifulSoup
import time
import os

headers = {
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}

def news_list(baseurl):
    result=[]
    urls=[]
    url=baseurl
    used=[]
    exists=[]
    while True:
        try:
            html=requests.get(url,headers=headers).text.encode('iso-8859-1').decode('gbk','ignore')
        except:
            url=urls.pop()
            continue
        items=BeautifulSoup(html,'lxml').find_all('a')
        for item in items:
            url=item.get('href')
            if url==None:
                continue
            if baseurl not in url:
                continue
            urls.append(url)
            if url in exists:
                continue
            if 'index' in url or '_' in url:
                continue
            if '2016' not in url and '2015' not in url:
                continue
            title=item.get_text().replace('\n','')
            if title.replace(' ','')=='':
                continue
            result.append([title,url])
            exists.append(url)
        if len(result)>1200:
            break
        while True:
            url=urls.pop()
            if url in used:
                continue
            used.append(url)
            break
        print(len(result))
    return result

def get_urls():
    needs=[['财经','http://business.sohu.com/'],['军事','http://mil.sohu.com/']
        ,['科技','http://it.sohu.com/'],['体育','http://sports.sohu.com/'],['教育','http://learning.sohu.com/']
        ,['娱乐','http://yule.sohu.com/'],['旅游','http://travel.sohu.com/']]
    for item in needs:
        newstype=item[0]
        baseurl=item[1]
        result=news_list(baseurl)
        f=open('urls.txt','a',encoding='utf-8')
        for news in result:
            line=newstype+'|'+news[0]+'|'+news[1]
            f.write(line.replace('\r','').replace('\n','')+'\n')
        f.close()
        print(newstype,'ok')

def article(url):
    html=requests.get(url,headers=headers).text.encode('iso-8859-1').decode('gbk','ignore')
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'content-wrapper'})
    title=soup.find('h1').get_text()
    table=soup.find('div',id='contentText').find_all('p')
    content=''
    for item in table:
        content+=item.get_text()
    return title,content

def social_news():
    urls=[]
    page=10842
    while True:
        html=requests.get('http://news.sohu.com/shehuixinwen_%s.shtml'%page,headers=headers).text.encode('iso-8859-1').decode('gbk','ignore')
        try:
            table=BeautifulSoup(html,'lxml').find('div',{'class':'new-article'}).find_all('div',{'class':'article'})
        except:
            break
        for item in table:
            url=item.find_all('a')[-1].get('href')
            if url in urls:
                continue
            urls.append(url)
        if len(urls)>1200:
            break
        page-=1
    print(len(urls))
    num=20000
    newstype='社会'
    for url in urls:
        try:
            title,content=article(url)
        except:
            continue
        try:
            os.mkdir(newstype)
        except:
            pass
        f=open(newstype+'/%s.txt'%num,'w',encoding='utf-8')
        f.write(title+'\r\n\r\n'+content)
        f.close()
        print(newstype,title)
        num+=1
        print(num)

def main():
    num=10000
    for line in open('urls.txt','r',encoding='utf-8'):
        line=line.replace('\n','')
        newstype=line.split('|')[0]
        url=line.split('|')[-1]
        try:
            title,content=article(url)
        except:
            continue
        try:
            os.mkdir(newstype)
        except:
            pass
        f=open(newstype+'/%s.txt'%num,'w',encoding='utf-8')
        f.write(title+'\r\n\r\n'+content)
        f.close()
        print(newstype,title)
        num+=1
        print(num)

social_news()