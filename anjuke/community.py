import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import json
import random
import threading


switch_time=30

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_proxies():
    proxyHost = "proxy.abuyun.com"
    proxyPort = "9010"
    # 代理隧道验证信息
    proxyUser = ""
    proxyPass = ""

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }
    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }
    return proxies

def switch_ip():
    html=requests.get('http://proxy.abuyun.com/switch-ip',proxies=get_proxies()).text
    print("Switch ip ",html)
    global t
    global switch_time
    t=threading.Timer(switch_time,switch_ip)
    t.start()

def get_community():
    page=1
    while True:
        html=requests.get('http://hf.anjuke.com/community/p%s'%page,headers=headers).text
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
                f.write(name+'|'+url+'\n')
            except:
                continue
        f.close()
        print(page)
        page+=1
        time.sleep(1)

def community_infor(url):
    html=requests.get('http://hf.anjuke.com/'+url,headers=headers,proxies=get_proxies(),timeout=30).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'left-cont float-l'})
    item={}
    try:
        item['price']=soup.find('em',{'class':'comm-avg-price'}).get_text()
    except:
        item['price']='-'
    detail=soup.find('div',{'class':'border-info comm-detail'})
    tits=detail.find_all('dt')
    values=detail.find_all('dd')
    for index in range(len(tits)):
        item[tits[index].get_text().replace('\r','').replace('\n','').replace(' ','').replace('：','')]=values[index].get_text().replace('\r','').replace('\n','').replace(' ','').replace('：','')
    html=requests.get('http://hf.anjuke.com/ajax/communityext/?commid=%s&useflg=onlyForAjax'%url.split('/')[-2],headers=headers,proxies=get_proxies(),timeout=30).text
    data=json.loads(html)['comm_propnum']
    try:
        item['saleNum']=data['saleNum']
    except:
        item['saleNum']='-'
    try:
        item['rentNum']=data['rentNum']
    except:
        item['rentNum']='-'
    keys=['price','saleNum','rentNum','所在版块','地址','总建面','总户数','建造年代','容积率','停车位','绿化率','出租率']
    line=''
    for key in keys:
        try:
            line+=item[key]+'|'
        except:
            line+='-|'
    return line

def base_infor():
    for line in open('urls.txt','r'):
        line=line.replace('\n','')
        try:
            infor=community_infor(line.split('|')[-1])
        except:
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
        html=requests.get('http://hf.anjuke.com/community/props/rent/%s/p%s/'%(url.split('/')[-2],page),headers=headers,proxies=get_proxies(),timeout=30).text
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
        price=eval(line[-1])
        price=sorted(price,reverse=True)
        try:
            price=price[int(len(price)/2)]
        except:
            price='-'
        sheet.append(line+[price])
    excel.save('result.xlsx')

t=threading.Timer(switch_time,switch_ip)
t.setDaemon(True)
t.start()
rentprice()