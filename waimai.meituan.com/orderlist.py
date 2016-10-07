import requests
from bs4 import BeautifulSoup
import time
import datetime
import json
import openpyxl

def get_login_data():
    f=open('login.json','r',encoding='utf-8')
    data=json.load(f)
    return data

def login():
    session=requests.session()
    data=get_login_data()
    headers = {
    'Accept':'*/*',
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    'X-Requested-With':'XMLHttpRequest',
    'Host':'e.waimai.meituan.com',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin':'http://e.waimai.meituan.com',
    'Referer':'http://e.waimai.meituan.com/logon',
    'Content-Length':'61',
    'Cookie':'_ga=GA1.3.1847404045.1474075466; __mta=146231947.1474075466051.1474075466051.1474075466051.1;device_uuid=ZTEwNjZjZWQtNWE3ZC00YWYyLWE2NzMtZWRmZmFjNzUzMGVi;shopCategory=food;__mta=146231947.1474075466051.1474075466051.1475645610512.2;',
    "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
    html=session.post('http://e.waimai.meituan.com/v2/logon/pass/step1/logon',data=data,headers=headers).text
    cookies=requests.utils.dict_from_cookiejar(session.cookies)
    f=open('cookies','w',encoding='utf-8')
    f.write(str(cookies))
    f.close()
    return cookies

def get_cookies():
    cookies=eval(open('cookies','r',encoding='utf-8').read())
    return cookies

def query(cookies,date_from,date_to):
    result=[]
    headers = {
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        'Host':'e.waimai.meituan.com',
        "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
    url='http://e.waimai.meituan.com/v2/order/history/r/query?getNewVo=1&wmOrderPayType=-2&wmOrderStatus=-2&sortField=1&startDate=%s&endDate=%s&pageNum=%s'
    page=1
    while True:
        get_url=url%(date_from,date_to,page)
        try:
            html=requests.get(get_url,cookies=cookies,headers=headers,timeout=30).text
        except:
            continue
        try:
            data=json.loads(html)['wmOrderList']
        except:
            break
        if data==[]:
            break
        for item in data:
            try:
                wm_poi_id=item['wm_poi_id']
                wmOrderId=item['id']
                phone=get_phone(cookies,wm_poi_id,wmOrderId)
                result.append({'infor':item['orderCopyContent'],'recipient_name':item['recipient_name'],'tel':phone})
            except:
                continue
            time.sleep(0.1)
        time.sleep(0.2)
        print(date_from,date_to,page,'ok')
        page+=1
    return result
    

def get_phone(cookies,wmPoiId,wmOrderId):
    headers = {
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        'Host':'e.waimai.meituan.com',
        "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
    url='http://e.waimai.meituan.com/v2/order/receive/processed/r/recipientPhone?wmPoiId=%s&wmOrderId=%s'%(wmPoiId,wmOrderId)
    html=requests.get(url,headers=headers,cookies=cookies).text
    phone=json.loads(html)['data']
    return phone


def day_get(d,num):
    oneday = datetime.timedelta(days=num)
    day=d-oneday
    day=str(day).split(' ')[0]
    return day

def is_ok(cookies):
    headers = {
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        'Host':'e.waimai.meituan.com',
        "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
    html=requests.get('http://e.waimai.meituan.com/',headers=headers,cookies=cookies).text
    if '首次登录新设备验证' in html:
        cookies=login()
        return cookies
    return cookies

def write_to_excel(result,filename):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for item in result:
        line=[]
        for key in ['recipient_name','tel','infor']:
            line.append(item[key])
        sheet.append(line)
    excel.save(filename)

def main():
    try:
        cookies=get_cookies()
    except:
        cookies=login()
    cookies=is_ok(cookies)
    '''
    date_today=time.strftime('%Y-%m-%d',time.localtime())
    d=datetime.datetime.strptime(date_today, "%Y-%m-%d")
    pre_date=day_get(d)
    '''
    date_today='2016-09-13'
    while True:
        d=datetime.datetime.strptime(date_today, "%Y-%m-%d")
        pre_date=day_get(d,6)
        result=query(cookies,pre_date,date_today)
        #write_to_excel(result,pre_date+'_'+date_today+'.xlsx')
        f=open('result.txt','a')
        for item in result:
            line=''
            for key in ['recipient_name','tel','infor']:
                try:
                    line+=item[key]+' ||'
                except:
                    continue
            f.write(line+'\n')
        f.close()
        d=datetime.datetime.strptime(pre_date, "%Y-%m-%d")
        date_today=day_get(d,1)
        print(date_today)

main()