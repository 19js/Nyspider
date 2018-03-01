from util import *
from bs4 import BeautifulSoup
import time
import re
import json

def parser_code_html(url):
    req=build_request(url)
    res_text=req.text.encode('iso-8859-1').decode('gbk','ignore')
    table=BeautifulSoup(res_text,'lxml').find('table',class_=re.compile('\w+table')).find_all('tr')
    result=[]
    for item in table:
        if '统计用区划' in str(item):
            continue
        tds=item.find_all('td')
        line=[]
        for td in tds:
            line.append(td.get_text())
        try:
            item_url=item.find('a').get('href')
            item_url=url.replace(url.split('/')[-1],item_url)
        except:
            item_url=''
        line.append(item_url)
        result.append(line)
    return result

def crawl():
    province_url='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/52.html'
    city_list=parser_code_html(province_url)
    county_list=[]
    for city in city_list:
        if city[-1]=='':
            county_list.append(city)
            continue
        items=parser_code_html(city[-1])
        county_list+=[city+item for item in items]
        print(city,'OK')
    town_list=[]
    for county in county_list:
        if county[-1]=='':
            town_list.append(county)
            continue
        items=parser_code_html(county[-1])
        town_list+=[county+item for item in items]
        print(county,'OK')
    village_list=[]
    for town in town_list:
        if town[-1]=='':
            village_list.append(town)
            continue
        items=parser_code_html(town[-1])
        village_list+=[town+item for item in items]
        print(town,'OK')
    write_to_excel(village_list,'result.xlsx')
crawl()

        
