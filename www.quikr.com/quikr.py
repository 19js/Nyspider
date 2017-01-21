#coding:utf-8
import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import threading
import json
import re
import sys
import datetime


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

models={}

def get_proxies_abuyun():
    proxyHost = "proxy.abuyun.com"
    proxyPort = "9010"
    path=sys.path[0]
    # 代理隧道验证信息
    proxyUser = ''#填入阿布云代理信息
    proxyPass = ''

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
    html=requests.get('http://proxy.abuyun.com/switch-ip',proxies=get_proxies_abuyun()).text
    print("Switch ip")

def login():
    session=requests.session()
    session.get('http://www.quikr.com/MyQuikr',headers=headers)
    data={
    'GreetingName':"yangweitaohustntu@gmail.com",
    'Password':'QW5keTEyMw=='
    }
    session.post('http://www.quikr.com/SignIn?aj=1&for=login_popup', data=data,headers=headers)
    return session

def paser_page(pagenum):
    html=requests.get('http://www.quikr.com/Cars/y71?page='+str(pagenum),headers=headers,proxies=get_proxies_abuyun(),timeout=30).text
    soup=BeautifulSoup(html,'lxml').find_all("div",{'class':'thumbnail'})
    result=[]
    date=time.strftime("%Y-%m-%d",time.localtime())
    for div in soup:
        car={}
        car['Url']=div.find('a').get('href')
        car['Date']=date
        car['City']=car['Url'].split('.')[0].replace('http://','')
        title=div.find('h4').get('title')
        car['Title']=title
        brand_model_va=parser_title(title)
        car['Brand']=brand_model_va[0]
        car['Model']=brand_model_va[1]
        car['Variance']=brand_model_va[2]
        try:
            car['Year']=title.split('–')[1]
        except:
            car['Year']='NA'
        try:
            car['Price']=div.find('div',{'class':'price-txt'}).get_text().replace('\n','').replace(' ','')
        except:
            car['Price']='NA'
        try:
            car['Posted']=div.find('span',{'class':'posted'}).get_text()
        except:
            car['Posted']='NA'
        try:
            car['Converted_Posted_Date']=convert_posted(car['Posted'])
        except:
            car['Converted_Posted_Date']='NA'
        result.append(car)

    try:
        pages=re.findall('Page (\d+) of (\d+)',html)
        endpage=int(pages[0][1])
    except:
        endpage=10000
    return result,endpage

def convert_posted(posted):
    try:
        num=re.findall('(\d+)',posted)[0]
        num=int(num)
    except:
        return 'NA'
    today=day=datetime.datetime.now()
    if 'day' in posted:
        day=today-datetime.timedelta(days=num)
        return str(day).split(' ')[0]
    if 'month' in posted:
        day=today-datetime.timedelta(days=num*30)
        return str(day).split(' ')[0]
    return str(today).split(' ')[0]

def car_infor(car,session):
    try_count=0
    while True:
        try:
            html=session.get(car['Url'],headers=headers,timeout=20,proxies=get_proxies_abuyun()).text
            soup=BeautifulSoup(html,'lxml').find('div',{'class':'vappage container'})
            toparea=soup.find('div',id='car_description')
            soup=soup.find('div',{'class':'detailArea'})
            if soup==None:
                if try_count==5:
                    return
                switch_ip()
                try_count+=1
                continue
            break
        except:
            if try_count==5:
                return
            try_count+=1
            switch_ip()
    seller=toparea.find('div',{'class':'seller col-xs-12'}).find('li').get_text()
    table=soup.find('div',id='tab1').find_all('li')
    need={'Fuel Type':'Fuel','Kms Driven':'Miliage','Color':'Color','Owner':'Owner','Transmission':'Powertrain','Engine Capacity':'Engine','Ad ID:':'Ad_ID','Views:':'Views','Car Type':'Body_Type'}
    for li in table:
        for key in need:
            if key in str(li):
                try:
                    car[need[key]]=li.find_all('span')[-1].get_text().replace('\xa0','')
                except:
                    car[need[key]]=li.get_text().replace('Ad ID:','').replace('Views:','')
                break
    try:
        car['Rate']=soup.find('span',{'class':'rating-number'}).get_text()
    except:
        car['Rate']='NA'

def get_base_infor():
    page=1
    endpage=10000
    while page<=endpage:
        try:
            result,e_page=paser_page(page)
        except:
            result=[]
        if result==[]:
            print('page',page,'failed,retrying')
            switch_ip()
            continue
        if endpage==10000:
            endpage=e_page
        f=open('urls.txt','a',encoding='utf-8')
        for car in result:
            f.write(str(car)+'\n')
        f.close()
        print(page,'ok')
        page+=1

def load_models():
    global models
    for line in open('./models.txt','r',encoding='utf-8'):
        item=eval(line)
        for key in item:
            models[key]=item[key]

def parser_title(title):
    global models
    if 'I want to sell' in title or 'All scrap junk condition' in title:
        return ['NA','NA','NA']
    title_list=title.split(' ')
    result=[]
    for key in models:
        if title_list[0] in key:
            result.append(key)
            text=''
            for model in models[key]:
                if model in title:
                    if len(model)>len(text):
                        text=model
            result.append(text)
            text=title.split('–')[0].replace(result[0],'').replace(result[1],'')
            result.append(text)
            return result
    return ['NA','NA','NA']

def get_detail_infor():
    session=login()
    for line in open('./urls.txt','r',encoding='utf-8'):
        car=eval(line)
        try:
            car_infor(car, session)
        except:
            failed=open('failed.txt','a',encoding='utf-8')
            failed.write(str(car))
            failed.close()
            continue
        f=open('result.txt','a',encoding='utf-8')
        f.write(str(car)+'\n')
        f.close()
        try:
            print(car['Title'],'ok')
        except:
            pass
    write_to_excel()

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    keys=['Url','City','Brand','Model','Variance','Year','Title','Price','Date','Posted','Converted_Posted_Date','Rate','Fuel','Miliage','Color','Owner','Powertrain','Engine','Views','Body_Type','Ad_ID']
    sheet.append(keys)
    for line in open('./result.txt','r',encoding='utf-8'):
        car=eval(line)
        line=[]
        for key in keys:
            try:
                value=car[key]
                if value.replace('\r','').replace('\n','').replace('\t','').replace(' ','')=='':
                    value='NA'
                line.append(value)
            except:
                line.append('NA')
        sheet.append(line)
    excel.save('result.xlsx')

if __name__=='__main__':
    load_models()
    get_base_infor()
    get_detail_infor()
