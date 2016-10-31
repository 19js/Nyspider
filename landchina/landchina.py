#coding:utf-8

import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}


def get_urls():
    #province={'山东':'37%','江苏':'32%','浙江':'33%','重庆':'50%','四川':'51%','湖北':'42%','河南':'41%','安徽':'34%','辽宁':'21%'}
    province={'浙江':'33%','辽宁':'21%'}
    try:
        os.mkdir('province')
    except:
        pass
    for key in province:
        f=open('province/%s.txt'%key,'a',encoding='utf-8')
        for date in ['2016-1-1~2016-4-7','2016-4-8~2016-9-7']:
            page=1
            while True:
                data={
                'hidComName':"default",
                'TAB_QueryConditionItem':'9f2c3acd-0256-4da2-a659-6949c4671a2a',
                'TAB_QueryConditionItem':"ec9f9d83-914e-4c57-8c8d-2c57185e912a",
                'TAB_QuerySubmitConditionData':"9f2c3acd-0256-4da2-a659-6949c4671a2a:{}|42ad98ae-c46a-40aa-aacc-c0884036eeaf:{}".format(date,province[key]),
                'TAB_QuerySubmitOrderData':"",
                'TAB_RowButtonActionControl':"",
                'TAB_QuerySubmitPagerData':page,
                'TAB_QuerySubmitSortData':""
                }
                try:
                    html=requests.post('http://www.landchina.com/default.aspx?tabid=263',data=data,headers=headers,timeout=30).text
                except:
                    continue
                table=BeautifulSoup(html,'lxml').find('table',id='TAB_contentTable').find_all('tr')
                if '没有检索到相关数据' in str(table):
                    break
                for item in table:
                    try:
                        line=[item.find('a').get('href')]
                    except:
                        continue
                    for td in item.find_all('td'):
                        try:
                            line.append(td.get_text().replace('\r','').replace('\n',''))
                        except:
                            line.append('')
                    f.write(str(line)+'\n')
                    print(line[-1])
                print(key,date,page,'ok')
                page+=1
        f.close()

get_urls()
