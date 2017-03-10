#coding:utf-8

import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import os
import json

headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_headers(plat_id):
    json_headers = {
        'X-Requested-With':'XMLHttpRequest',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        'Host':'shuju.wdzj.com',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin':'http://shuju.wdzj.com',
        'Referer':'http://shuju.wdzj.com/plat-info-%s.html'%plat_id,
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
    return json_headers

def login():
    data={
        'username':'',#用户名
        'password':'',#密码
        'auto_login':1,
        'login_submit':1
    }
    session=requests.session()
    html=session.get('https://passport.wdzj.com/user/login',headers=headers).text
    csrf_test_name=BeautifulSoup(html,'lxml').find('input',{'name':'csrf_test_name'}).get('value')
    data['csrf_test_name']=csrf_test_name
    html=session.post('https://passport.wdzj.com/user/login', data=data,headers=headers).text
    return session

def write_to_excel(result,filename):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in result:
        try:
            sheet.append(line)
        except:
            continue
    excel.save(filename)

def get_plats():
    html=requests.get('http://shuju.wdzj.com/',headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('tbody',id='platTable').find_all('tr')
    result=[]
    for item in table:
        try:
            href=item.find('a')
            name=href.get_text().replace('\r','').replace('\n','').replace('\t','')
            plat_id=href.get('href').split('-')[-1].split('.')[0]
        except:
            continue
        result.append([name,plat_id])
    return result

def loan_num_and_average_time_limit(session,plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    'wdzjPlatId':plat_id,
    'type':1,
    'target1':9,
    'target2':10
    }
    html=session.post('http://shuju.wdzj.com/plat-info-target.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    data1=data['data1']
    data2=data['data2']
    result=[]
    result.append(['','借款标数','平均借款期限'])
    for index in range(len(date)):
        result.append([date[index],data1[index],data2[index]])
    write_to_excel(result,u"result/%s/借款标数and平均借款期限.xlsx"%(plat_name))

def need_repay_num_and_need_collect_num(session,plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    'wdzjPlatId':plat_id,
    'type':1,
    'target1':12,
    'target2':11
    }
    html=session.post('http://shuju.wdzj.com/plat-info-target.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    data1=data['data1']
    data2=data['data2']
    result=[]
    result.append(['','待还借款人数','待收投资人数'])
    for index in range(len(date)):
        result.append([date[index],data1[index],data2[index]])
    write_to_excel(result,u"result/%s/待还借款人数and待收投资人数.xlsx"%(plat_name))

def top10_rate(session,plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    'wdzjPlatId':plat_id,
    'type':3,
    'target1':18,
    'target2':1
    }
    html=session.post('http://shuju.wdzj.com/plat-info-target.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    data1=data['data1']
    data2=data['data2']
    result=[]
    result.append(['','前十大借款人待还金额占比','前十大土豪待收金额占比'])
    for index in range(len(date)):
        result.append([date[index],data2[index],data1[index]])
    write_to_excel(result,u"result/%s/前十大借款人待还金额占比and前十大土豪待收金额占比.xlsx"%(plat_name))

def top50_rate(session,plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    'wdzjPlatId':plat_id,
    'type':3,
    'target1':18,
    'target2':2
    }
    html=session.post('http://shuju.wdzj.com/plat-info-target.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    data1=data['data1']
    data2=data['data2']
    result=[]
    result.append(['','前五十借款人待还金额占比','前五十土豪待收金额占比'])
    for index in range(len(date)):
        result.append([date[index],data2[index],data1[index]])
    write_to_excel(result,u"result/%s/前五十借款人待还金额占比and前五十土豪待收金额占比.xlsx"%(plat_name))

def input_and_need_repay(session,plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    'wdzjPlatId':plat_id,
    'type':1,
    'target1':4,
    'target2':3
    }
    html=session.post('http://shuju.wdzj.com/plat-info-target.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    data1=data['data1']
    data2=data['data2']['y1']
    data3=data['data2']['y2']
    result=[]
    result.append(['','资金净流入','当日待还余额','当日待还余额(30日平均)'])
    for index in range(len(date)):
        result.append([date[index],data1[index],data2[index],data3[index]])
    write_to_excel(result,u"result/%s/资金净流入and当日待还余额.xlsx"%(plat_name))

def deep_data():
    try:
        os.mkdir('result')
    except:
        pass
    funcs=[loan_num_and_average_time_limit
            ,need_repay_num_and_need_collect_num
            ,top10_rate
            ,top50_rate
            ,input_and_need_repay]
    plats=get_plats()
    session=login()
    for plat in plats:
        try:
            os.mkdir(u'result/%s'%plat[0])
        except:
            pass
        for func in funcs:
            try:
                func(session,plat[1],plat[0])
            except:
                print(func,plat[1],'failed')
                continue
            time.sleep(1)
        print(plat[0],'ok')

if __name__=='__main__':
    deep_data()
