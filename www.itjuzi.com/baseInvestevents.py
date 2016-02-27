#coding:utf-8

import requests
from bs4 import BeautifulSoup
import xlwt3
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_infor(url):
    html=requests.get(url,headers=headers,timeout=50).text
    results=[]
    table=BeautifulSoup(html,'html.parser').find_all('ul',attrs={'class':'list-main-eventset'})[1].find_all('li')
    for li in table:
        item={}
        i=li.find_all('i')
        item['date']=i[0].get_text().replace('\n','').replace('\t','')
        spans=i[2].find_all('span')
        item['name']=spans[0].get_text().replace('\n','').replace('\t','')
        item['industry']=spans[1].get_text().replace('\n','').replace('\t','')
        item['local']=spans[2].get_text().replace('\n','').replace('\t','')
        item['round']=i[3].get_text().replace('\n','').replace('\t','')
        item['capital']=i[4].get_text().replace('\n','').replace('\t','')
        companys=i[5].find_all('a')
        Investmenters=''
        if(companys==[]):
            Investmenters=i[5].get_text().replace('\n','').replace('\t','')
        else:
            for a in companys:
                Investmenters+=a.get_text().replace('\n','').replace('\t','')+';'
        item['Investmenters']=Investmenters
        results.append(item)
    return results

def main():
    excel=xlwt3.Workbook()
    sheet=excel.add_sheet('sheet')
    count=0
    startpage=1
    keys=['date','name','industry','local','round','capital','Investmenters']
    while startpage<1143:
        try:
            results=get_infor('https://www.itjuzi.com/investevents?page=%s'%startpage)
        except:
            time.sleep(5)
            continue
        for item in results:
            num=0
            for key in keys:
                sheet.write(count,num,item[key])
                num+=1
            count+=1
        print(startpage,'--ok')
        startpage+=1
        time.sleep(3)
        excel.save('investevents.xls')
main()
