import requests
from bs4 import BeautifulSoup
import time
import datetime
import openpyxl
import string
import json
import random


headers = {
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate'}

def get_city_list():
    url='http://m.dianping.com/citylist?c={}'
    for char in string.ascii_uppercase:
        html=requests.get(url.format(char),headers=headers).text
        table=BeautifulSoup(html,'lxml').find('ul',{'class':'J_citylist'}).find_all('a')
        f=open('city.txt','a')
        for item in table:
            try:
                f.write(str([item.get_text(),item.get('data-id'),item.get('href')])+'\n')
            except:
                continue
        f.close()
        print(char,'OK')

def load_province():
    soup=BeautifulSoup(open('./city.html','r').read(),'lxml').find_all('dl',{'class':'terms'})
    province={}
    for dl in soup:
        pro_name=dl.find('dt').get_text()
        for item in dl.find_all('a'):
            city_name=item.get_text().replace('\n','').replace(' ','')
            province[city_name]=pro_name
    f=open('result.txt','w')
    num=0
    for line in open('city.txt','r'):
        item=eval(line)
        try:
            pro_name=province[item[0]]
        except:
            failed=open('failed.txt','a')
            failed.write(line)
            failed.close()
            continue
        f.write(str([pro_name]+item)+'\n')
    f.close()

def get_shop_list(offset,cityid,categoryid):
    url='https://mapi.dianping.com/searchshop.json?start={}&regionid=0&categoryid={}&sortid=0&maptype=0&cityid={}&locatecityid={}'.format(offset,categoryid,cityid,cityid)
    res=requests.get(url,headers=headers,timeout=30)
    if res.status_code==451:
        return []
    html=res.text
    data=json.loads(html)['list']
    result=[]
    for item in data:
        try:
            line=[item['name'],item['branchName'],item['categoryName'],item['matchText'],item['priceText']]
            result.append(line)
        except:
            continue
    return result

def searchshop():
    filename={
        '210':'快餐简餐.txt',
        '238':'西餐简餐.txt'
    }
    for category in ['210','238']:
        for line in open('./city.txt','r'):
            line=eval(line)
            start=5000
            while True:
                try:
                    result=get_shop_list(start, line[-2], category)
                except Exception as e:
                    print(e,line,'failed')
                    time.sleep(10)
                    continue
                if len(result)==0:
                    break
                f=open(filename[category],'a')
                for item in result:
                    f.write(str(line+item)+'\n')
                f.close()
                print(line,category,start,'OK')
                start+=25
                time.sleep(random.randint(1,4))

searchshop()
