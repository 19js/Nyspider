#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re
import time
import openpyxl

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_tels(url):
    html=requests.get(url,headers=headers).text
    try:
        table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'list'}).find_all('li')
    except:
        return []
    tels=[]
    for li in table:
        try:
            tel=li.find('div',attrs={'class':'list-r-area'}).find('p',attrs={'class':'tel'}).find('span').get_text()
        except:
            continue
        tels.append(tel)
    return tels


def main():
    url=input('输入链接：')
    url=re.sub('o\d+/','',url)
    if not url.startswith('http'):
        url='http://'+url
    page=1
    tels=[]
    while True:
        try:
            result=get_tels(url+'o'+str(page)+'/')
        except:
            continue
        if result==[]:
            break
        tels+=result
        print('第%s页--完成'%page)
        page+=1
        time.sleep(5)
    tels=list(set(tels))
    count=0
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for tel in tels:
        sheet.append([tel])
    excel.save('tels.xls')
    
main()
