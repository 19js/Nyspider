import requests
from bs4 import BeautifulSoup
import time
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
import smtplib
import threading
import json
import re

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def get58Url():
    need_place=['http://sz.58.com/longgang/job/pn{}/?key=%E5%A4%96%E8%B4%B8&final=1&PGTID=0d302408-0071-561b-9682-75236fd6c681&ClickID=1','http://sz.58.com/longgang/job/pn{}/?key=%E4%BE%9B%E5%BA%94%E9%93%BE&PGTID=0d302408-0071-5bf1-d0ef-c597d1715d73&ClickID=1','http://sz.58.com/buji/job/pn{}/?key=%E5%A4%96%E8%B4%B8&final=1&PGTID=0d302408-0071-5829-664e-5a4f9b442c71&ClickID=2','http://sz.58.com/buji/job/pn{}/?key=%E4%BE%9B%E5%BA%94%E9%93%BE&PGTID=0d302408-0071-53ab-1247-c62456029960&ClickID=1','http://sz.58.com/pingshanxinqu/job/pn{}/?key=%E5%A4%96%E8%B4%B8&final=1&PGTID=0d302408-0073-fc8b-ad3a-e39e590852e1&ClickID=1','http://sz.58.com/pingshanxinqu/job/pn{}/?key=%E4%BE%9B%E5%BA%94%E9%93%BE&PGTID=0d302408-0073-fb5e-7456-0f96bf5dadfe&ClickID=1','http://sz.58.com/dapengxq/job/pn{}/?key=%E5%A4%96%E8%B4%B8&cmcskey=%E5%A4%96%E8%B4%B8&final=1&specialtype=gls&canclequery=isbiz%3D0&PGTID=0d302408-0000-4a23-69ad-d36695c21d3a&ClickID=1','http://sz.58.com/dapengxq/job/pn{}/?key=%E4%BE%9B%E5%BA%94%E9%93%BE&cmcskey=%E4%BE%9B%E5%BA%94%E9%93%BE&final=1&specialtype=gls&canclequery=isbiz%3D0&PGTID=0d302408-0000-4dfa-c958-c5330b285bf0&ClickID=1']
    try:
        exists=[line.replace('\n','') for line in open('58exists.txt','r',encoding='utf-8')]
    except:
        exists=[]
    result=[]
    for placeurl in need_place:
        page=1
        statue=True
        while statue:
            try:
                html=requests.get(placeurl.format(page),headers=headers,timeout=30).text
                table=BeautifulSoup(html,'lxml').find('div',id='infolist').find_all('dl')
                for item in table:
                    companyname=item.find('a',{'class':'fl'}).get('title')
                    url=item.find('a',{'class':'fl'}).get('href')
                    if companyname in exists:
                        continue
                    date=item.find_all('dd')[-1].get_text().replace('\r','').replace('\n','').replace(' ','')
                    if date!='精准' and date!='今天' and '小时' not in date and '分钟' not in date:
                        statue=False
                        break
                    com=[]
                    exists.append(companyname)
                    area=item.find_all('dd')[-2].get_text()
                    job=item.find('a').get_text()
                    com=[companyname,job,area,url]
                    result.append(com)
            except:
                break
            time.sleep(2)
            print('58','page',page,'--ok')
            page+=1
    f=open('58exists.txt','w',encoding='utf-8')
    for line in exists:
        f.write(line+'\n')
    f.close()
    return result

def company58Infor(url):
    html=requests.get(url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'basicMsg'})
    try:
        instro=table.find('div',{'class':'compIntro'}).get_text().replace('\r','').replace('\n','').replace(' ','')
    except:
        instro=''
    td=table.find_all('td')
    th=table.find_all('th')
    result=[]
    labels=['公司地址','公司性质','公司行业','公司规模','企业网址']
    for title in labels:
        text=''
        for index in range(len(th)):
            if th[index].get_text().replace('\r','').replace('\n','').replace(' ','')==title:
                text=td[index].get_text().replace('\r','').replace('\n','').replace(' ','').replace('查看地图','')
        result.append(text)
    result.append(instro)
    return result

def Company58():
    urls=get58Url()
    print('58--',len(urls))
    result=[]
    for item in urls:
        try:
            company=company58Infor(item[-1])
        except:
            continue
        time.sleep(1)
        result.append(item+company)
    if len(result)==0:
        return
    count=0
    text=''
    keys=['龙岗','坪山','坑梓','大鹏']
    while True:
        try:
            Count=loademail()
            break
        except:
            pass
    for item in result:
        ok=False
        for key in keys:
            if key in str(item):
                ok=True
                break
        if not ok:
            continue
        for i in item:
            text+=i+'\n'
        text+='\n\n'+'--------------'*10+'\n'
        count+=1
        if count<10:
            continue
        try:
            sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 58',text)
        except:
            print('Send email Failed!')
        count=0
        text=''
    if text=='':
        return
    try:
        sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 58',text)
    except:
        print('Send email Failed!')

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def sendEmail(fromemail,passwd,toemail,subject,text):
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject']=subject
    msg['From'] = _format_addr(fromemail)
    msg['To'] = _format_addr(toemail)
    server=smtplib.SMTP_SSL('smtp.qq.com')
    server.ehlo('smtp.qq.com')
    server.login(fromemail,passwd)
    server.sendmail(fromemail, [toemail], msg.as_string())
    server.quit()

def loademail():
    f=open('Email.txt','r').read()
    f=f.replace('\r','').replace('\n','').replace(' ','').replace('\t','')
    result=f.split('---')
    return result


def get_company_urls():
    need_place=['http://search.51job.com/list/040000,000000,0000,00,9,99,%25E5%25A4%2596%25E8%25B4%25B8%252B%25E9%25BE%2599%25E5%25B2%2597,2,{}.html'
                ,'http://search.51job.com/list/040000,000000,0000,00,9,99,%25E5%25A4%2596%25E8%25B4%25B8%252B%25E5%259D%25AA%25E5%25B1%25B1,2,{}.html'
                ,'http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=040000%2C00&funtype=0000&industrytype=00&keyword=%E5%A4%96%E8%B4%B8%2B%E5%A4%A7%E9%B9%8F&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9']
    try:
        exists=[line.replace('\n','') for line in open('temp/51_exists.txt','r',encoding='utf-8')]
    except:
        exists=[]
    result=[]
    today=time.strftime('%m-%d',time.localtime(time.time()))
    for placeurl in need_place:
        page=1
        statue=True
        while statue:
            try:
                html=requests.get(placeurl.format(page),headers=headers,timeout=30).text.encode('ISO-8859-1').decode('gbk','ignore')
                table=BeautifulSoup(html,'lxml').find('div',id='resultList').find_all('div',attrs={'class':'el'})
                for item in table[1:]:
                    companyname=item.find('span',attrs={'class':'t2'}).find('a').get('title')
                    url=item.find('span',{'class':'t2'}).find('a').get('href')
                    if companyname in exists:
                        continue
                    date=item.find('span',{'class':'t5'}).get_text()
                    if date not in today:
                        continue
                    com=[]
                    exists.append(companyname)
                    area=item.find('span',{'class':'t3'}).get_text().replace('\r\n','').replace(' ','')
                    job=item.find('a').get_text().replace('\r\n','').replace(' ','')
                    com=[companyname,job,area,url]
                    result.append(com)
            except:
                break
            time.sleep(2)
            print('前程无忧','page',page,'--ok')
            page+=1
            if page==10:
                break
    f=open('51exists.txt','w',encoding='utf-8')
    for line in exists:
        f.write(line+'\n')
    f.close()
    return result

def company51Infor(url):
    html=requests.get(url,headers=headers,timeout=30).text.encode('ISO-8859-1').decode('gbk','ignore')
    table=BeautifulSoup(html,'lxml').find('div',{'class':'tCompany_center clearfix'})
    result=[]
    try:
        div=table.find('div',{'class':'tHeader tHCop'}).find('p',attrs={'class':'ltype'}).get_text().replace('\r','').replace('\n','').replace(' ','')
        result+=div.split('|')
    except:
        pass
    try:
        div=table.find('div',{'class':'tCompany_full'})
        instro=div.find('div',{'class':'in'}).get_text()
        result.append(instro)
        try:
            boot=div.find_all('div',{'class':'bmsg'})
            for item in boot:
                result.append(item.find('p').get_text())
        except:
            pass
    except:
        pass
    return [item.replace('\r','').replace('\n','').replace('\t','').replace('\xa0','') for item in result]

def Company51():
    urls=get51Url()
    print('前程无忧--',len(urls))
    result=[]
    for item in urls:
        try:
            company=company51Infor(item[-1])
        except:
            continue
        time.sleep(1)
        result.append(item+company)
    if len(result)==0:
        return
    count=0
    text=''
    keys=['龙岗','坪山','坑梓','大鹏']
    while True:
        try:
            Count=loademail()
            break
        except:
            pass
    for item in result:
        ok=False
        for key in keys:
            if key in str(item):
                ok=True
                break
        if not ok:
            continue
        for i in item:
            text+=i+'\n'
        text+='\n\n'+'--------------'*10+'\n'
        count+=1
        if count<10:
            continue
        try:
            sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 51job',text)
        except:
            print('Send email Failed!')
        count=0
        text=''
    if text=='':
        return
    try:
        sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 51job',text)
    except:
        print('Send email Failed!')

def getZhilianUrl():
    need_place=['http://sou.zhaopin.com/jobs/searchresult.ashx?jl=765&kw=%E5%A4%96%E8%B4%B8&sm=0&p={}&re=2042','http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=%E4%BE%9B%E5%BA%94%E9%93%BE&isadv=0&isfilter=1&p={}&re=2042','http://sou.zhaopin.com/jobs/searchresult.ashx?jl=765&kw=%E5%A4%96%E8%B4%B8&sm=0&isfilter=1&p={}&re=2043','http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=%E4%BE%9B%E5%BA%94%E9%93%BE&isadv=0&isfilter=1&p={}&re=2043','http://sou.zhaopin.com/jobs/searchresult.ashx?jl=765&kw=%E5%A4%96%E8%B4%B8&sm=0&isfilter=1&p={}&re=2362','http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=%E4%BE%9B%E5%BA%94%E9%93%BE&isadv=0&isfilter=1&p={}&re=2362']
    try:
        exists=[line.replace('\n','') for line in open('zhiexists.txt','r',encoding='utf-8')]
    except:
        exists=[]
    result=[]
    today=time.strftime('%m-%d',time.localtime(time.time()))
    for placeurl in need_place:
        page=1
        statue=True
        while statue:
            try:
                html=requests.get(placeurl.format(page),headers=headers,timeout=30).text#.encode('ISO-8859-1').decode('gbk','ignore')
                table=BeautifulSoup(html,'lxml').find('div',id='newlist_list_content_table').find_all('table',attrs={'class':'newlist'})
                if '抱歉，没有符合您要求的职位。以下职位也很不错，不妨试试' in html:
                    statue=False
                    break
                for item in table[1:]:
                    companyname=item.find('td',attrs={'class':'gsmc'}).find('a').get_text().replace('\r','').replace('\n','').replace(' ','')
                    url=item.find('td',attrs={'class':'gsmc'}).find('a').get('href')
                    if companyname in exists:
                        continue
                    date=item.find('td',{'class':'gxsj'}).get_text().replace('\r','').replace('\n','').replace(' ','')
                    if date not in today:
                        statue=False
                        break
                    com=[]
                    exists.append(companyname)
                    area=item.find('td',{'class':'gzdd'}).get_text().replace('\r\n','').replace(' ','')
                    job=item.find('a').get_text().replace('\r\n','').replace(' ','')
                    com=[companyname,job,area,url]
                    result.append(com)
            except:
                statue=False
                break
            time.sleep(2)
            print('智联','page',page,'--ok')
            page+=1
    f=open('zhiexists.txt','w',encoding='utf-8')
    for line in exists:
        f.write(line+'\n')
    f.close()
    return result

def companyZhilianInfor(url):
    html=requests.get(url,headers=headers,timeout=30).text#.encode('ISO-8859-1').decode('gbk','ignore')
    table=BeautifulSoup(html,'lxml').find('div',{'class':'mainLeft'})
    result=[]
    des=table.find('table',{'class':'comTinyDes'}).find_all('tr')
    for item in des:
        try:
            result.append(item.get_text())
        except:
            continue
    try:
        content=table.find('div',attrs={'class':'company-content'}).get_text()
        result.append(content)
    except:
        pass
    return [item.replace('\r','').replace('\n','').replace('\t','').replace('\xa0','') for item in result]


def CompanyZhilian():
    urls=getZhilianUrl()
    print('智联--',len(urls))
    result=[]
    for item in urls:
        try:
            company=companyZhilianInfor(item[-1])
        except:
            continue
        time.sleep(1)
        result.append(item+company)
    if len(result)==0:
        return
    count=0
    text=''
    keys=['龙岗','坪山','坑梓','大鹏']
    while True:
        try:
            Count=loademail()
            break
        except:
            pass
    for item in result:
        ok=False
        for key in keys:
            if key in str(item):
                ok=True
                break
        if not ok:
            continue
        for i in item:
            text+=i+'\n'
        text+='\n\n'+'--------------'*10+'\n'
        count+=1
        if count<10:
            continue
        try:
            sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 智联',text)
        except:
            print('Send email Failed!')
        count=0
        text=''
    if text=='':
        return
    try:
        sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 智联',text)
    except:
        print('Send email Failed!')

def getCjUrl():
    need_place=['http://s.cjol.com/l200809-200805-200808-kw-%E5%A4%96%E8%B4%B8/?SearchType=1&KeywordType=3&page={}#utm_source=4']
    try:
        exists=[line.replace('\n','') for line in open('cjexists.txt','r',encoding='utf-8')]
    except:
        exists=[]
    result=[]
    today=time.strftime('%m-%d',time.localtime(time.time()))
    for placeurl in need_place:
        page=1
        statue=True
        while statue:
            try:
                html=requests.get(placeurl.format(page),headers=headers,timeout=30).text#.encode('ISO-8859-1').decode('gbk','ignore')
                table=BeautifulSoup(html,'lxml').find('div',id='searchlist').find_all('ul',attrs={'class':'results_list_box'})
                for item in table:
                    companyname=item.find('li',attrs={'class':'list_type_second'}).find('a').get_text().replace('\r','').replace('\n','').replace(' ','')
                    url=item.find('li',attrs={'class':'list_type_second'}).find('a').get('href')
                    if companyname in exists:
                        continue
                    com=[]
                    exists.append(companyname)
                    area=item.find('li',{'class':'list_type_third'}).get_text().replace('\r\n','').replace(' ','')
                    job=item.find('a').get_text().replace('\r\n','').replace(' ','')
                    com=[companyname,job,area,url]
                    result.append(com)
            except:
                statue=False
                break
            time.sleep(1)
            print('人才在线','page',page,'--ok')
            page+=1
            if(page==30):
                break
    f=open('cjexists.txt','w',encoding='utf-8')
    for line in exists:
        f.write(line+'\n')
    f.close()
    return result

def companyCjInfor(url):
    html=requests.get(url,headers=headers,timeout=30).text#.encode('ISO-8859-1').decode('gbk','ignore')
    table=BeautifulSoup(html,'lxml').find('div',{'id':'inner_left_main_inner'})
    result=[]
    des=table.find('div',{'class':'company_detailedinfo'}).find_all('li')
    for item in des:
        try:
            result.append(item.get_text())
        except:
            continue
    try:
        content=table.find('div',attrs={'class':'common_linebox'}).get_text()
        result.append(content)
    except:
        pass
    return [item.replace('\r','').replace('\n','').replace('\t','').replace('\xa0','') for item in result]


def CompanyCj():
    urls=getCjUrl()
    print('人才在线--',len(urls))
    result=[]
    for item in urls:
        try:
            company=companyCjInfor(item[-1])
        except:
            continue
        time.sleep(0.5)
        result.append(item+company)
    if len(result)==0:
        return
    count=0
    text=''
    keys=['龙岗','坪山','坑梓','大鹏']
    while True:
        try:
            Count=loademail()
            break
        except:
            pass
    for item in result:
        ok=False
        for key in keys:
            if key in str(item):
                ok=True
                break
        if not ok:
            continue
        for i in item:
            text+=i+'\n'
        text+='\n\n'+'--------------'*10+'\n'
        count+=1
        if count<10:
            continue
        try:
            sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 人才在线',text)
        except:
            print('Send email Failed!')
        count=0
        text=''
    if text=='':
        return
    try:
        sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 人才在线',text)
    except:
        print('Send email Failed!')

def jobcnurls():
    page=1
    try:
        exists=[line.replace('\n','') for line in open('jobcnexists.txt','r',encoding='utf-8')]
    except:
        exists=[]
    result=[]
    status=True
    while status:
        try:
            data={
            'p.querySwitch':"0",
            'p.searchSource':"default",
            'p.keyword':"外贸",
            'p.keyword2':"",
            'p.keywordType':"2",
            'p.pageNo':page,
            'p.pageSize':"40",
            'p.sortBy':"postdate",
            'p.statistics':"false",
            'p.totalRow':"556",
            'p.cachePageNo':'1',
            'p.cachePosIds':"3513784,2542627,2175796,3203044,2996185,3614375,3395878,3571408,1231266,3601002,3516555,3274772,1959747,3109563,3332633,2170628,3615059,3595859,3587717,3535948,3291403,3621325,3461433,3472599,3472621,3578139,2706695,3616287,3493549,3607106,3616931,3439425,3280638,3578145,3270019,1916558,1228083,3524309,3465542,3486713,3486707,3601025,3391175,3321005,3320998,3320996,3320994,3306390,3365198,3533514,3533500,2811010,2425856,3623211,3583850,2717496,3358036,3246890,3534463,3527159,3511972,3369724,1374874,3535274,3284704,3567439,3608412,3528423,3077368,3075370,3623956,3623949,3623936,2163952,3584947,3599522,3599518,3582993,2532549,3415244,1834820,3490070,3377947,3479194,3330969,3572298,3256770,3217981,3544077,3517787,3409490,2799496,3593391,3402261,3417841,3253317,3570524,3393344,3610898,3610598,3603185,3610905,3610889,3610699,3610694,3610601,3610573,3022817,3605224,3193085,2992893,3555263,3027745,3572094,3471935,3436003,3605218,3587727,3591475,3577476,3533077,3006314,3501469,3495393,3496318,3568220,3567212,3552154,3616415,3616191,3616179,3546881,3519846,3400707,3482812,3458998,3458994,3458991,3458990,3457766,3612384,3388971,3567679,3558114,3015274,3289607,3587729,3587715,3565104,3613923,3613913,3573873,3541749,3613076,3613000,3491848,3429534,3309660,3308632,3612064,3612061,3612027,2999639,2799009,3330820,2658670,3442336,3606261,3577069,3546094,2732605,3494886,3449636,3551506,3455154,3528192,1995873,3476392,3398936,3398929,3501222,3479232,3598970,2390239,1931366,1830190,3606063,3556527,3553706,3546420,3410018,3250223,3480094,3605141,3604841,3573305,3472646,3511922,3511900,3374124",
            'p.cachePosUpddates':"201608152130,201608152105,201608152100,201608152047,201608152047,201608152036,201608152015,201608152000,201608151933,201608151925,201608151900,201608151857,201608151746,201608151505,201608151430,201608151412,201608151222,201608151222,201608151222,201608151214,201608151155,201608150934,201608150900,201608150859,201608150850,201608150259,201608150259,201608121855,201608121814,201608121744,201608121723,201608121652,201608121652,201608121620,201608121540,201608121540,201608121540,201608121520,201608121520,201608121455,201608121455,201608121414,201608121411,201608121411,201608121411,201608121411,201608121411,201608121411,201608121357,201608121117,201608121117,201608121052,201608121049,201608121038,201608121038,201608121034,201608120942,201608120939,201608120926,201608120926,201608120925,201608120925,201608120921,201608120858,201608120835,201608120828,201608120825,201608120813,201608120813,201608120813,201608120300,201608120300,201608120300,201608120259,201608111024,201608101528,201608101528,201608101528,201608101528,201608101402,201608101133,201608101022,201608101015,201608100934,201608100926,201608100829,201608091630,201608091630,201608091608,201608091608,201608091350,201608091036,201608090931,201608090852,201608081101,201608081008,201608080839,201608080839,201608071706,201608071706,201608071706,201608071705,201608071705,201608071705,201608071705,201608071705,201608071705,201608070941,201608070819,201608061746,201608061654,201608061144,201608061042,201608060921,201608051118,201608051118,201608051018,201608031109,201608030845,201608021919,201608021156,201608021156,201608021138,201608021025,201608011801,201608011125,201608011123,201608011122,201608010300,201608010300,201608010300,201607311127,201607311127,201607311014,201607311013,201607301706,201607301706,201607301706,201607301706,201607301706,201607291750,201607291750,201607291549,201607291549,201607291543,201607291542,201607291117,201607291117,201607291117,201607280300,201607280300,201607271124,201607271124,201607270300,201607270300,201607261642,201607261642,201607261640,201607261640,201607260300,201607260300,201607260300,201607251846,201607251846,201607251756,201607251756,201607251755,201607251638,201607241429,201607241429,201607241402,201607241200,201607241137,201607241011,201607191831,201607191542,201607191354,201607190259,201607181205,201607181205,201607181019,201607181018,201607170924,201607161542,201607161418,201607161417,201607160300,201607151729,201607151729,201607151536,201607151536,201607151448,201607151358,201607150300,201607140300,201607131547,201607131547,201607131035,201607131035,201607131035",
            'p.jobnature':"15",
            'p.JobLocationTown':"龙岗区;大鹏新区;坪山新区",
            'p.includeNeg':"0",
            'p.inputSalary':"-1",
            'p.workYear1':"-1",
            'p.workYear2':"11",
            'p.jobLocation':"广东;深圳",
            'p.jobLocationId':"3010",
            'p.degreeId1':"10",
            'p.degreeId2':"70",
            'p.posPostDate':"366",
            'p.salary':"-1",
            'p.otherFlag':"3"
            }
            html=requests.post('http://www.jobcn.com/search/result_servlet.ujson?s=search%2Ftop',headers=headers,data=data,timeout=30).text
            jsondata=json.loads(html)['rows']
            if len(jsondata)==0:
                break
            for row in jsondata:
                try:
                    comname=row['comName']
                    if comname in exists:
                        continue
                    exists.append(comname)
                    date=row['postDateDesc']
                    if '天' in date:
                        status=False
                        break
                    city=row['jobLoc4City']
                    address=row['address']
                    contactPerson=row['contactPerson']
                    email=row['email']
                    posDescription=row['posDescription']
                    comId=row['comId']
                    posId=row['posId']
                    result.append([comname,address,contactPerson,email,row['posName'],city,date,posDescription,comId,posId])
                except:
                    continue
        except:
            break
        print('卓博','page',page,'--ok')
        page+=1
        time.sleep(2)
        if page==10:
            break
    f=open('jobcnexists.txt','w',encoding='utf-8')
    for line in exists:
        f.write(line+'\n')
    f.close()
    return result

def jobcn_infor(item):
    html=requests.get('http://www.jobcn.com/position/detail.xhtml?redirect=0&posId=%s&comId=%s&s=search/advanced&acType=1'%(item[-1],item[-2]),headers=headers,timeout=30).text
    soup=BeautifulSoup(html,'lxml')
    comdes=soup.find('div',id='menuHeader').find('div',{'class':'base'}).get_text().replace('\r','').replace('\n\n','')
    return comdes

def jobcn():
    urls=jobcnurls()
    print('卓博--',len(urls))
    result=[]
    for item in urls:
        try:
            companydes=jobcn_infor(item)
        except:
            continue
        time.sleep(1)
        result.append(item[:-2]+[companydes]+['http://www.jobcn.com/position/detail.xhtml?redirect=0&posId=%s&comId=%s&s=search/advanced&acType=1'%(item[-1],item[-2])])
    if len(result)==0:
        return
    count=0
    text=''
    keys=['龙岗','坪山','坑梓','大鹏']
    while True:
        try:
            Count=loademail()
            break
        except:
            pass
    for item in result:
        ok=False
        for key in keys:
            if key in str(item):
                ok=True
                break
        if not ok:
            continue
        for i in item[:-1]:
            text+=i+'\n'
        text+=item[-1]
        text+='\n\n'+'--------------'*10+'\n'
        count+=1
        if count<10:
            continue
        try:
            sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 卓博',text)
        except:
            print('Send email Failed!')
        count=0
        text=''
    if text=='':
        return
    try:
        sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 卓博',text)
    except:
        print('Send email Failed!')

def ganjiurls():
    need_place=['http://sz.ganji.com/zpbiaoqian/longgang/o{}/_%E5%A4%96%E8%B4%B8/zhaopin/','http://sz.ganji.com/zpbiaoqian/pingshanxinqu/o{}/_%E5%A4%96%E8%B4%B8/zhaopin/','http://sz.ganji.com/zpbiaoqian/dapengxinqu/o{}/_%E5%A4%96%E8%B4%B8/zhaopin/']
    try:
        exists=[line.replace('\n','') for line in open('ganjiexists.txt','r',encoding='utf-8')]
    except:
        exists=[]
    result=[]
    for placeurl in need_place:
        page=1
        statue=True
        while statue:
            try:
                html=requests.get(placeurl.format(page),headers=headers,timeout=30).text
                table=BeautifulSoup(html,'lxml').find('div',id='list-job-id').find_all('dl',{'class':'con-list-zcon'})
                for item in table:
                    try:
                        dds=item.find_all('dd')
                        companyname=dds[0].find('a').get('title')
                        companyurl=dds[0].find('a').get('href')
                        joburl=item.find('a').get('href')
                        if companyname in exists:
                            continue
                        date=dds[-1].get_text()
                        if '今天' not in date:
                            statue=False
                            break
                        com=[]
                        exists.append(companyname)
                        job=item.find('a').get_text().replace('\n','')
                        com=[companyname,date,companyurl,joburl]
                        result.append(com)
                    except:
                        continue
            except:
                break
            time.sleep(2)
            print('赶集','page',page,'--ok')
            page+=1
    f=open('ganjiexists.txt','w',encoding='utf-8')
    for line in exists:
        f.write(line+'\n')
    f.close()
    return result

def ganji_infor(company):
    html=requests.get('http://sz.ganji.com/'+company[-1],headers=headers,timeout=30).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'l-d-con'})
    title=soup.find('h1').get_text()
    text=soup.find('div',{'class':'d-c-left-age d-c-left-firm mt-30'}).get_text().replace('\r','').replace('\n','#').replace(' ','')
    try:
        place=re.findall('工作地点：(.*?)#',text)[0]
    except:
        place='--'
    jobdes=soup.find('div',{'class':'deta-Corp'}).get_text().replace('\r','').replace('\n','')
    html=requests.get(company[-2],headers=headers,timeout=30).text
    try:
        comdes=BeautifulSoup(html,'lxml').find('div',{'class':'l-d-con'}).find('div',{'class':'c-introduce'}).get_text()
    except:
        try:
            table=BeautifulSoup(html,'lxml').find_all('div',{'class':'content'})
            comdex='--'
            for item in table:
                if '公司名称：' in str(item):
                    comdes=item.get_text().replace('\r','').replace('\n\n','\n').replace(' ','')
                    break
        except:
            pass
    result=[comdes,title,place,jobdes,'http://sz.ganji.com/'+company[-1],company[-2]]
    return  result


def ganji():
    urls=ganjiurls()
    print('赶集--',len(urls))
    result=[]
    for item in urls:
        try:
            company=ganji_infor(item)
        except:
            continue
        time.sleep(1)
        result.append(company)
    if len(result)==0:
        return
    count=0
    text=''
    keys=['龙岗','坪山','坑梓','大鹏']
    while True:
        try:
            Count=loademail()
            break
        except:
            pass
    for item in result:
        ok=False
        for key in keys:
            if key in str(item):
                ok=True
                break
        if not ok:
            continue
        for i in item:
            text+=i.replace('\n\n','\n')+'\n'
        text+='\n\n\n'+'--------------'*10+'\n'
        count+=1
        if count<10:
            continue
        try:
            sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 赶集',text)
        except:
            print('Send email Failed!')
        count=0
        text=''
    if text=='':
        return
    try:
        sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 赶集',text)
    except:
        print('Send email Failed!')

def jobuiurls():
    need_place=['http://www.jobui.com/jobs?jobKw=%E5%A4%96%E8%B4%B8&cityKw=%E6%B7%B1%E5%9C%B3&areaCode=190305&n={}&sortField=last']
    try:
        exists=[line.replace('\n','') for line in open('jobuiexists.txt','r',encoding='utf-8')]
    except:
        exists=[]
    result=[]
    for placeurl in need_place:
        page=1
        statue=True
        while statue:
            try:
                html=requests.get(placeurl.format(page),headers=headers,timeout=30).text
                table=BeautifulSoup(html,'lxml').find('ul',{'class':'searcher-job-detail j-recommendJob'}).find_all('li')
                for item in table:
                    try:
                        companyname=item.find('a').get('title')
                        companyurl=item.find('a').get('href')
                        jobname=item.find('h2').find('a').get_text()
                        joburl=item.find('h2').find('a').get('href')
                        if companyname in exists:
                            continue
                        date=item.find('span',{'class':'fr'}).get_text()
                        if '天' in date:
                            statue=False
                            break
                        com=[]
                        exists.append(companyname)
                        com=[companyname,jobname,date,'http://www.jobui.com/'+companyurl,'http://www.jobui.com/'+joburl]
                        result.append(com)
                    except:
                        continue
            except:
                break
            time.sleep(2)
            print('职友集','page',page,'--ok')
            page+=1
    f=open('jobuiexists.txt','w',encoding='utf-8')
    for line in exists:
        f.write(line+'\n')
    f.close()
    return result

def jobui_infor(company):
    html=requests.get(company[-1],headers=headers,timeout=30).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'j-job-detail'}).find('div',{'class':'cfix'})
    jobdes=''
    try:
        jobdes=soup.find('div').get_text().replace('\r','').replace('\t','').replace('\n','').replace(' ','')
    except:
        pass
    try:
        jobdes+=soup.find('dl').get_text().replace('：\n','：')
    except:
        pass
    try:
        url='http://www.jobui.com/'+soup.find('p',{'class':'j-job-option'}).find('a',{'class':'fs12 j-valaber'}).get('href')
        jobdes+='源网站:'+url+'\n'
    except:
        pass
    try:
        html=requests.get(company[-2],headers=headers,timeout=30).text
        soup=BeautifulSoup(html,'lxml').find('div',{'class':'aleft'})
        comdes=''
        try:
            comdes+=soup.find('div',id='cmp-intro').get_text()
        except:
            pass
        try:
            comdes+='\n'+soup.find_all('div',{'class':'jk-box jk-matter'})[1].find('dl').get_text()
        except:
            pass
    except:
        comdes=''
    comdes=comdes.replace('\n\n','').replace('：\n','：')
    comdes=re.sub('\d+张公司照片','',comdes)
    result=[comdes,'职位要求:'+jobdes]+company
    return result

def jobui():
    urls=jobuiurls()
    print('职友集--',len(urls))
    result=[]
    for item in urls:
        try:
            company=jobui_infor(item)
        except:
            continue
        time.sleep(1)
        result.append(company)
    if len(result)==0:
        return
    count=0
    text=''
    keys=['龙岗','坪山','坑梓','大鹏']
    while True:
        try:
            Count=loademail()
            break
        except:
            pass
    for item in result:
        ok=False
        for key in keys:
            if key in str(item):
                ok=True
                break
        if not ok:
            continue
        for i in item:
            text+=i+'\n'
        text+='\n\n'+'--------------'*10+'\n'
        count+=1
        if count<10:
            continue
        try:
            sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 职友集',text)
        except:
            print('Send email Failed!')
        count=0
        text=''
    if text=='':
        return
    try:
        sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 职友集',text)
    except:
        print('Send email Failed!')

count=input("输入间隔时间(分钟)：")
try:
    count=int(count)
except:
    count=10

functions=[Company58,Company51,CompanyZhilian,CompanyCj,jobcn,ganji,jobui]
while True:
    works=[]
    for func in functions:
        work=threading.Thread(target=func)
        works.append(work)
    for work in works:
        work.setDaemon(True)
        work.start()
    for work in works:
        work.join()
    print('Wait')
    time.sleep(count*60)
