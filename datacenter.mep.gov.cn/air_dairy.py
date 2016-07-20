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


def get_table(url):
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'html.parser').find('table',id='report1').find_all('tr')
    result=[]
    for tr in table[2:-3]:
        item=''
        for td in tr.find_all('td'):
            item+=td.get_text()+'|'
        result.append(item)
    return result

def main():
    text_f=open('2014_2016.txt','a')
    pagestart=1
    while pagestart<=12702:
        url='http://datacenter.mep.gov.cn/report/air_daily/air_dairy.jsp?city=&startdate=2012-07-01&enddate=2016-07-19&page='%pagestart
        try:
            items=get_table(url)
        except:
            time.sleep(2)
            print(pagestart,'-failed')
            continue
        for item in items:
            text_f.write(item+'\n')
        print(pagestart,'-ok')
        pagestart+=1
    text_f.close()

main()
