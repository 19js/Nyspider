import requests
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_memberlist():
    page=1
    while True:
        url='http://www.dianping.com/memberlist/4/10?pg='+str(page)
        html=requests.get(url,headers=headers).text
        table=BeautifulSoup(html,'lxml').find('table',{'class':'rankTable'}).find('tbody').find_all('tr')
        f=open('memberlist.txt','a')
        for item in table:
            try:
                tds=item.find_all('td')
                name=tds[0].find('a').get_text()
                url=tds[0].find('a').get('href')
                comment_num=tds[1].get_text()
                reply_num=tds[3].get_text()
                flower_num=tds[4].get_text()
                f.write(str([name,url,comment_num,reply_num,flower_num])+'\n')
            except:
                continue
        f.close()
        page+=1
        if page==7:
            break

def get_comments()
