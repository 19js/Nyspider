#说明：此脚本是用于抓取合肥小区信息以及租房房价信息

import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import json
import random
from proxy import get_proxies
import logging

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_community():
    page=1
    while True:
        try:
            html=requests.get('http://hf.anjuke.com/community/p%s'%page,headers=headers,proxies=get_proxies(),timeout=10).text
            if '请输入图片中的验证码' in html:
                continue
        except:
            continue
        try:
            table=BeautifulSoup(html,'lxml').find('div',id='list-content').find_all('div',{'class':'li-itemmod'})
        except:
            break
        if table==[]:
            break
        f=open('urls.txt','a')
        for item in table:
            try:
                url=item.find('a').get('href')
                name=item.find('a').get('title')
            except:
                continue
            try:
                price=item.find('div',{'class':'li-side'}).find('strong').get_text()
            except:
                price='-'
            f.write(name+'|'+price+'|'+url+'\n')            
        f.close()
        print(page)
        page+=1
        if page==51:
            break

def community_infor(url):
    while True:
        try:
            html=requests.get('http://hf.anjuke.com/'+url,headers=headers,proxies=get_proxies(),timeout=10).text
            if '请输入图片中的验证码' in html:
                continue
            break
        except Exception as e:
            print('[community_infor]%s failed'%(url))
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'comm-basic-mod'})
    item={}
    try:
        detail=soup.find('dl',{'class':'basic-parms-mod'})
        tits=detail.find_all('dt')
        values=detail.find_all('dd')
        for index in range(len(tits)):
            item[tits[index].get_text().replace('\r','').replace('\n','').replace(' ','').replace('：','').replace('\xa0','')]=values[index].get_text().replace('\r','').replace('\n','').replace(' ','').replace('：','')
    except:
        pass
    while True:
        try:
            html=requests.get('http://hf.anjuke.com/ajax/communityext/?commid=%s&useflg=onlyForAjax'%url.split('/')[-2],headers=headers,proxies=get_proxies(),timeout=10).text
            break
        except Exception as e:
            print('[community_infor-json]%s failed'%(url))
    data=json.loads(html)['comm_propnum']
    try:
        item['saleNum']=data['saleNum']
    except:
        item['saleNum']='-'
    try:
        item['rentNum']=data['rentNum']
    except:
        item['rentNum']='-'
    keys=['saleNum','rentNum','所在版块','地址','总建面','总户数','建造年代','容积率','停车位','绿化率','出租率']
    line=''
    for key in keys:
        try:
            line+=str(item[key])+'|'
        except:
            line+='-|'
    return line

def base_infor():
    for line in open('urls.txt','r'):
        line=line.replace('\n','')
        try:
            infor=community_infor(line.split('|')[-1])
        except Exception as e:
            logging.exception(e)
            failed=open('failed.txt','a')
            failed.write(line+'\n')
            failed.close()
            continue
        f=open('community_infor.txt','a')
        f.write(line+'|'+infor+'\n')
        f.close()
        print(line)

def get_rentprice(url):
    result=[]
    page=1
    while True:
        html=requests.get('http://hf.anjuke.com/community/props/rent/%s/p%s/'%(url.split('/')[-2],page),headers=headers,timeout=30).text
        try:
            table=BeautifulSoup(html,'lxml').find('ul',{'class':'m-house-list'}).find_all('li',{'class':'m-rent-house'})
        except:
            break
        for item in table:
            try:
                price=item.find('p',{'class':'price'}).find('span').get_text()
                result.append(price)
            except:
                continue
        page+=1
    return result

def rentprice():
    for line in open('community_infor.txt','r'):
        line=line.replace('\n','')
        url=line.split('|')[1]
        try:
            price=get_rentprice(url)
        except:
            failed=open('price_failed.txt','a')
            failed.write(line+'\n')
            failed.close()
            continue
        f=open('result.txt','a')
        f.write(line+str(price)+'\n')
        f.close()
        print(line.split('|')[0])

def write2excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in open('result.txt','r'):
        line=line.split('|')
        try:
            price=eval(line[14])
        except:
            print(line)
            return
        price=sorted(price,reverse=True)
        try:
            price=price[int(len(price)/2)]
        except:
            price='-'
        sheet.append([price]+line)
    excel.save('result.xlsx')

def get_location(address,city):
    url='http://api.map.baidu.com/place/v2/search?query=%s&region=%s&city_limit=true&output=json&ak=fh980b9Ga64S8bl8QblSC3kq'%(address,city)
    html=requests.get(url).text
    try:
        data=json.loads(html)['results'][0]['location']
    except:
        return ''
    lng=data['lng']
    lat=data['lat']
    return '|'+str(lng)+'|'+str(lat)


if __name__=="__main__":
    get_community()
    base_infor()
