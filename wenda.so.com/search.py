import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver

headers = {
    'Host':"wenda.so.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

browser=webdriver.Firefox()
browser.get('http://wenda.so.com/')
browser.implicitly_wait(10)
def search(key):
    #html=requests.get('http://wenda.so.com/search/?q='+key,headers=headers,timeout=30).text
    browser.get('http://wenda.so.com/search/?q='+key)
    time.sleep(0.5)
    html=browser.page_source
    table=BeautifulSoup(html,'lxml').find_all('li',{'class':'item'})
    for item in table:
        try:
            url=item.find('a').get('href')
            if 'q/' in url:
                return 'http://wenda.so.com/'+url
        except:
            continue

def get_questions():
    for word in open('failed_words','r'):
        word=word.replace('\r','').replace('\n','')
        try:
            url=search(word)
        except:
            failed=open('failed.txt','a')
            failed.write(word+'\n')
            failed.close()
            continue
        if url==None:
            failed=open('failed.txt','a')
            failed.write(word+'\n')
            failed.close()
            continue
        f=open('question_','a')
        f.write(word+'||'+url+'\n')
        print(word,'ok')
        f.close()

get_questions()
