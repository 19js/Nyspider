#coding:utf-8

import requests
from bs4 import BeautifulSoup
import xlwt3
import re

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_urls(url):
    try:
        html=requests.get(url,headers=headers,timeout=50).text
    except:
        return []
    rel='(http://shop.yhd.com/m-\d+.html)'
    urls=re.findall(rel,html)
    urls=list(set(urls))
    try:
        html=requests.get(url+'&isGetMoreProducts=1',headers=headers,timeout=50).text
        urls+=re.findall(rel,html)
        urls=list(set(urls))
    except:
        print('--')
    return urls

def get_infor(url):
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'shop-des'}).find_all('li')
    item={}
    item['url']=url
    try:
        item['name']=table[0].find('span').get_text()
    except:
        item['name']=''
    try:
        item['city']=table[1].find('span').get_text()
    except:
        item['city']=''
    try:
        item['tel']=table[2].find('span').get_text()
    except:
        item['tel']=''
    return item

def main():
    excel_f=xlwt3.Workbook()
    sheet=excel_f.add_sheet('sheet')
    count=0
    list_url=input("输入商铺链接:")
    list_url=list_url.replace('list.yhd.com/','list.yhd.com/searchPage/')
    page=1
    while True:
        urls=get_urls(re.sub('p\d','p'+str(page),list_url))
        if(urls==[]):
            break
        for url in urls:
            try:
                item=get_infor(url)
            except:
                continue
            sheet.write(count,0,item['name'])
            sheet.write(count,1,item['city'])
            sheet.write(count,2,item['tel'])
            sheet.write(count,3,item['url'])
            count+=1
            print(count)
            excel_f.save('data.xls')
        page+=1

main()
