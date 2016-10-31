#coding:utf-8

import requests
from bs4 import BeautifulSoup
import time
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_infor():
    urls=['https://www.dianping.com/search/category/2/10/r2588o2p','https://www.dianping.com/search/category/2/10/r1493o2p','https://www.dianping.com/search/category/2/10/r1490o2p']
    f=open('haidian.txt','a',encoding='utf-8')
    for url in urls:
        page=1
        while page<=50:
            try:
                html=requests.get(url+str(page),headers=headers,timeout=30).text
            except:
                continue
            table=BeautifulSoup(html,'lxml').find('div',id='shop-all-list').find_all('li')
            for li in table:
                try:
                    soup=li.find('div',attrs={'class':'txt'})
                    tit=soup.find('div',attrs={'class':'tit'})
                    comment=soup.find('div',attrs={'class':'comment'})
                    tag_addr=soup.find('div',attrs={'class':'tag-addr'})
                    text=tit.find('a').get_text().replace('\r','').replace('\n','')+'||'+comment.find('span').get('title')+'||'+comment.find('a',attrs={'class':'review-num'}).get_text().replace('\r','').replace('\n','')+'||'+comment.find('a',attrs={'class':'mean-price'}).get_text().replace('\r','').replace('\n','')+'||'+tag_addr.find('span',attrs={'class':'tag'}).get_text().replace('\r','').replace('\n','')+'||'+tag_addr.find('span',attrs={'class':'addr'}).get_text().replace('\r','').replace('\n','')+'||'
                    comment_list=soup.find('span',attrs={'class':'comment-list'}).find_all('span')
                    for i in comment_list:
                        text+='||'+i.get_text().replace('\r','').replace('\n','')
                    for i in tit.find('div',attrs={'class':'promo-icon'}).find_all('a'):
                        try:
                            text+='||'+i.get('class')
                        except:
                            text+='||'+i.get('class')[0]
                    f.write(text.replace(' ','')+'\n')
                except:
                    continue
            page+=1
            print(page)
            time.sleep(1)
    f.close()

get_infor()
