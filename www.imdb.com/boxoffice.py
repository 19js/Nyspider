#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_url(title):
    name=re.sub('\(.*?\)','',title)#.lower()#.replace(' ','')
    html=requests.get('http://www.boxofficemojo.com/search/?q=%s'%name,headers=headers).text.replace('\r','').replace('\n','').replace('\t','')
    rel='bgcolor=#FFFF99>(.*?)</tr>'
    tr=re.findall(rel,html)[0]#BeautifulSoup(html,'lxml').find('tr',attrs={'bgcolor':'#FFFF99'})
    tds=BeautifulSoup(str(tr),'lxml').find_all('td')
    #tds=tr.findall('td')
    url='http://www.boxofficemojo.com'+tds[0].find('a').get('href')
    de=tds[2].get_text()
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'mp_box_content'}).get_text().replace('\r','|').replace('\n','|')
    print(table)
    line=de
    rel='Worldwide:\|(.*?)\|'
    try:
        wl=re.findall(rel,table)[0]
    except:
        wl='-'
    line=de+'||'+wl
    return line

def main():
    f=open('data.txt','w')
    for line in open('new.txt','r').readlines():
        line=line.replace('\r','').replace('\n','')
        try:
            price=get_url(line)
        except:
            price='--||--'
        f.write(line+'||'+price+'\n')
        print(price)

main()
