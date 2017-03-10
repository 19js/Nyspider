#coding:utf-8

import requests
from bs4 import BeautifulSoup
import openpyxl
import time

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_plats():
    html=requests.get('http://shuju.wdzj.com/',headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('tbody',id='platTable').find_all('tr')
    result=[]
    for item in table:
        tds=item.find_all('td')
        line=[]
        for td in tds:
            text=td.get_text().replace('\r','').replace('\n','').replace('\t','')
            line.append(text)
        href=item.find('a').get('href')
        line.append(href)
        result.append(line)
    return result


def central_data(url):
    html=requests.get(url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'mod-area'}).find_all('ul',{'class':'xlist'})
    result=[]
    for ul in table:
        for li in ul.find_all('li'):
            try:
                value=li.find('div',{'class':'rate-data'}).get_text().replace('\r','').replace('\n','').replace(' ','').replace('\t','')
            except:
                value=''
            result.append(value)
    return result

def write_to_excel(result):
    date_today=time.strftime("%Y_%m_%d",time.localtime())
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in result:
        sheet.append(line)
    excel.save('result/%s.xlsx'%date_today)

def crawl():
    plats=get_plats()
    result=[]
    for plat in plats:
        try:
            line=central_data(plat[-1])
        except:
            line=[]
        result.append(plat+line)
        print(plat)
    write_to_excel(result)

if __name__=='__main__':
    crawl_time="10"#小时
    crawl_time=crawl_time+':'
    try:
        import os
        os.mkdir('result')
    except:
        pass
    while True:
        time_now=time.strftime("%H:%M",time.localtime())
        if crawl_time in time_now:
            try:
                crawl()
            except:
                print(time.strftime("%Y_%m_%d %H:%M",time.localtime()),'failed')
                continue
            print(time.strftime("%Y_%m_%d %H:%M",time.localtime()),'ok')
            time.sleep(3600)
        time.sleep(1800)
