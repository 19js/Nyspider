#coding:utf-8

import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import json
import os

def get_headers(plat_id):
    headers = {
        'X-Requested-With':'XMLHttpRequest',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        'Host':'shuju.wdzj.com',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin':'http://shuju.wdzj.com',
        'Referer':'http://shuju.wdzj.com/plat-info-%s.html'%plat_id,
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
    return headers

def get_plats():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
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

def write_to_excel(result,filename):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in result:
        try:
            sheet.append(line)
        except:
            continue
    excel.save(filename)

def initialize(plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    "wdzjPlatId":int(plat_id)
    }
    html=requests.post('http://shuju.wdzj.com/plat-info-initialize.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    amountValue=data['amountValue']#成交量
    result=[]
    for index in range(len(date)):
        result.append([date[index],amountValue[index]])
    write_to_excel(result,u"result/%s/成交量.xlsx"%(plat_name))

def income_rate(plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    'wdzjPlatId':plat_id,
    'type':1,
    'target1':2,
    'target2':0
    }
    html=requests.post('http://shuju.wdzj.com/plat-info-target.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    values=data['data1']
    result=[]
    for index in range(len(date)):
        result.append([date[index],values[index]])
    write_to_excel(result,u"result/%s/预期收益率.xlsx"%(plat_name))

def loan_level(plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    'wdzjPlatId':plat_id,
    'type':3,
    'target1':16,
    'target2':2
    }
    html=requests.post('http://shuju.wdzj.com/plat-info-target.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    y1=data['data1']['y5']
    y2=data['data1']['y6']
    y3=data['data1']['y7']
    y4=data['data1']['y8']
    result=[]
    result.append(['','1-10w','10-100w','100w-1000w','1000w-'])
    for index in range(len(date)):
        result.append([date[index],y1[index],y2[index],y3[index],y4[index]])
    write_to_excel(result,u"result/%s/借款人数分级.xlsx"%(plat_name))

def invest_level(plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    'wdzjPlatId':plat_id,
    'type':3,
    'target1':16,
    'target2':1
    }
    html=requests.post('http://shuju.wdzj.com/plat-info-target.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    y1=data['data1']['y1']
    y2=data['data1']['y2']
    y3=data['data1']['y3']
    y4=data['data1']['y4']
    result=[]
    result.append(['','0-1w','1-10w','10w-100w','100w-'])
    for index in range(len(date)):
        result.append([date[index],y1[index],y2[index],y3[index],y4[index]])
    write_to_excel(result,u"result/%s/投资人数分级.xlsx"%(plat_name))

def different_income_rate(plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    'wdzjPlatId':plat_id,
    'type':3,
    'target1':17,
    'target2':1
    }
    html=requests.post('http://shuju.wdzj.com/plat-info-target.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    y1=data['data1']['y1']
    y2=data['data1']['y2']
    y3=data['data1']['y3']
    y4=data['data1']['y4']
    y5=data['data1']['y5']
    result=[]
    result.append(['','天','1月','2月','3-6月','6月以上'])
    for index in range(len(date)):
        result.append([date[index],y1[index],y2[index],y3[index],y4[index],y5[index]])
    write_to_excel(result,u"result/%s/不同期限标预期收益率.xlsx"%(plat_name))

def filled_time_used(plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    'wdzjPlatId':plat_id,
    'type':3,
    'target1':17,
    'target2':2
    }
    html=requests.post('http://shuju.wdzj.com/plat-info-target.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    y1=data['data1']['y6']
    y2=data['data1']['y7']
    y3=data['data1']['y8']
    y4=data['data1']['y9']
    y5=data['data1']['y10']
    result=[]
    result.append(['','天','1月','2月','3-6月','6月以上'])
    for index in range(len(date)):
        result.append([date[index],y1[index],y2[index],y3[index],y4[index],y5[index]])
    write_to_excel(result,u"result/%s/不同期限标满标用时.xlsx"%(plat_name))

def average_amount(plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    'wdzjPlatId':plat_id,
    'type':1,
    'target1':7,
    'target2':8
    }
    html=requests.post('http://shuju.wdzj.com/plat-info-target.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    data1=data['data1']
    data2=data['data2']
    result=[]
    result.append(['','人均投资金额','人均借款金额'])
    for index in range(len(date)):
        result.append([date[index],data1[index],data2[index]])
    write_to_excel(result,u"result/%s/人均投资and人均借款金额.xlsx"%(plat_name))

def new_invest_num_and_old(plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    'wdzjPlatId':plat_id,
    'type':1,
    'target1':19,
    'target2':20
    }
    html=requests.post('http://shuju.wdzj.com/plat-info-target.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    data1=data['data1']
    data2=data['data2']
    result=[]
    result.append(['','新投资人数','老投资人数'])
    for index in range(len(date)):
        result.append([date[index],data1[index],data2[index]])
    write_to_excel(result,u"result/%s/新投资人数and老投资人数.xlsx"%(plat_name))

def new_invest_amount_and_old(plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    'wdzjPlatId':plat_id,
    'type':1,
    'target1':21,
    'target2':22
    }
    html=requests.post('http://shuju.wdzj.com/plat-info-target.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    data1=data['data1']
    data2=data['data2']
    result=[]
    result.append(['','新投资人总额','老投资人总额'])
    for index in range(len(date)):
        result.append([date[index],data1[index],data2[index]])
    write_to_excel(result,u"result/%s/新投资人总额and老投资人总额.xlsx"%(plat_name))

def average_time_limit(plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    'wdzjPlatId':plat_id,
    'type':1,
    'target1':10,
    'target2':23
    }
    html=requests.post('http://shuju.wdzj.com/plat-info-target.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    data1=data['data1']
    data2=data['data2']
    result=[]
    result.append(['','平均借款期限','行业平均期限'])
    for index in range(len(date)):
        result.append([date[index],data1[index],data2[index]])
    write_to_excel(result,u"result/%s/平均借款期限and行业平均期限.xlsx"%(plat_name))

def invert_num_and_load_num(plat_id,plat_name):
    headers=get_headers(plat_id)
    data={
    'wdzjPlatId':plat_id,
    'type':1,
    'target1':5,
    'target2':6
    }
    html=requests.post('http://shuju.wdzj.com/plat-info-target.html', data=data,headers=headers,timeout=30).text
    data=json.loads(html)
    date=data['date']
    data1=data['data1']
    data2=data['data2']
    result=[]
    result.append(['','投资人数','借款人数'])
    for index in range(len(date)):
        result.append([date[index],data1[index],data2[index]])
    write_to_excel(result,u"result/%s/投资人数and借款人数.xlsx"%(plat_name))

def table_data():
    funcs=[initialize,income_rate,loan_level,invest_level
        ,different_income_rate,filled_time_used,average_amount
        ,new_invest_num_and_old,new_invest_amount_and_old,average_time_limit,invert_num_and_load_num]
    plats=get_plats()
    try:
        os.mkdir('result')
    except:
        pass
    for plat in plats:
        try:
            os.mkdir(u'result/%s'%plat[0])
        except:
            pass
        for func in funcs:
            try:
                func(plat[1],plat[0])
            except:
                print(func,plat[1],'failed')
                continue
            time.sleep(1)
        print(plat[0],'ok')

if __name__=='__main__':
    table_data()
