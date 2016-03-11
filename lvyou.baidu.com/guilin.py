#coding:utf-8

import requests
from bs4 import BeautifulSoup
import json
import xlwt3
import time


headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def get_place():
    excel=xlwt3.Workbook()
    sheet=excel.add_sheet('sheet')
    count=0
    page=1
    while page<17:
        html=requests.get('http://lvyou.baidu.com/destination/ajax/jingdian?format=ajax&cid=0&playid=0&seasonid=5&surl=guilin&pn=%s&rn=18'%page,headers=headers).text
        data=json.loads(html)['data']['scene_list']
        for item in data:
            sheet.write(count,0,item['sname'])
            count+=1
        excel.save('scene_list.xls')
        time.sleep(2)
        page+=1
        print(page)

def line_url():
    f=open('urls.txt','a',encoding='utf-8')
    startpn=0
    while startpn<=720:
        html=requests.get('http://lvyou.baidu.com/guilin/luxian/?day_cnt_low=&day_cnt_high=&avg_cost=&season=&time_type=&pn=%s&rn=15'%startpn,headers=headers).text.encode('ISO-8859-1').decode('utf-8','ignore')
        startpn+=15
        table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'path-info-container'}).find_all('li')
        for li in table:
            a=li.find('a',attrs={'class':'plan-title'})
            text=a.get_text()+'||http://lvyou.baidu.com'+a.get('href')
            f.write(text+'\n')
        print(startpn)
        time.sleep(1)
    f.close()

def get_line(url):
    html=requests.get(url,headers=headers).text.encode('ISO-8859-1').decode('utf-8','ignore')
    table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'plan-trip-main'}).find_all('div',attrs={'class':'inner-width'})
    results=[]
    for item in table:
        text=''
        text+=item.find('header').get_text().replace('\r',' ').replace('\n',' ')
        sections=item.find_all('div',attrs={'class':'J_card-block'})
        for section in sections:
            text+='||'+section.find('header').get_text().replace('\r',' ').replace('\n',' ')
            try:
                trafic=section.find('div',attrs={'class':'traffic-all'}).get_text().replace('\r',' ').replace('\n',' ')
            except:
                trafic=' '
            if not trafic==' ':
                text+=' {%s} '%trafic
        results.append(text.replace('  ',' ').replace('[查看交通]','').replace('预订','').replace('  ',' '))
    return results

def main():
    excel=xlwt3.Workbook()
    sheet=excel.add_sheet('sheet')
    count=0
    for line in open('urls.txt','r').readlines():
        lists=line.replace('\n','').split('||')
        title=lists[0]
        url=lists[-1]
        try:
            results=get_line(url)
        except:
            continue
        for item in results:
            sheet.write(count,0,title)
            num=1
            for i in item.split('||'):
                sheet.write(count,num,i)
                num+=1
            count+=1
        excel.save('results.xls')
        print(line)
        time.sleep(2)

main()
