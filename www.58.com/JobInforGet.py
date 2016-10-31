import requests
from bs4 import BeautifulSoup
import time
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
import smtplib

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
            print(page,'--ok')
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
    for item in result:
        for i in item:
            text+=i+'\n'
        text+='\n\n'
        count+=1
        if count<10:
            continue
        Count=loademail()
        try:
            sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 58',text)
        except:
            print('Send email Failed!')
        count=0
        text=''
    if text=='':
        return
    Count=loademail()
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


def get51Url():
    need_place=['http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=040000%2C00&funtype=0000&industrytype=00&keyword=%E5%A4%96%E8%B4%B8%2B%E9%BE%99%E5%B2%97&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9&curr_page={}','http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=040000%2C00&funtype=0000&industrytype=00&keyword=%E4%BE%9B%E5%BA%94%E9%93%BE%2B%E9%BE%99%E5%B2%97&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9&curr_page={}','http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=040000%2C00&funtype=0000&industrytype=00&keyword=%E5%A4%96%E8%B4%B8%2B%E5%9D%AA%E5%B1%B1&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9&curr_page={}','http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=040000%2C00&funtype=0000&industrytype=00&keyword=%E4%BE%9B%E5%BA%94%E9%93%BE%2B%E5%9D%AA%E5%B1%B1&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9&curr_page={}','http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=040000%2C00&funtype=0000&industrytype=00&keyword=%E5%A4%96%E8%B4%B8%2B%E5%A4%A7%E9%B9%8F&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9&curr_page={}','http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=040000%2C00&funtype=0000&industrytype=00&keyword=%E4%BE%9B%E5%BA%94%E9%93%BE%2B%E5%A4%A7%E9%B9%8F&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9&curr_page={}']
    try:
        exists=[line.replace('\n','') for line in open('51exists.txt','r',encoding='utf-8')]
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
                        statue=False
                        break
                    com=[]
                    exists.append(companyname)
                    area=item.find('span',{'class':'t3'}).get_text().replace('\r\n','').replace(' ','')
                    job=item.find('a').get_text().replace('\r\n','').replace(' ','')
                    com=[companyname,job,area,url]
                    result.append(com)
            except:
                break
            time.sleep(2)
            print(page,'--ok')
            page+=1
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
    for item in result:
        for i in item:
            text+=i+'\n'
        text+='\n\n'
        count+=1
        if count<10:
            continue
        Count=loademail()
        try:
            sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 51job',text)
        except:
            print('Send email Failed!')
        count=0
        text=''
    if text=='':
        return
    Count=loademail()
    try:
        sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 51job',text)
    except:
        print('Send email Failed!')

def getZhilianUrl():
    need_place=['http://sou.zhaopin.com/jobs/searchresult.ashx?jl=765&kw=%E5%A4%96%E8%B4%B8&sm=0&p={}&re=2042','http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=%E4%BE%9B%E5%BA%94%E9%93%BE&isadv=0&isfilter=1&p={}&re=2042','http://sou.zhaopin.com/jobs/searchresult.ashx?jl=765&kw=%E5%A4%96%E8%B4%B8&sm=0&isfilter=1&p={}&re=2043','http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=%E4%BE%9B%E5%BA%94%E9%93%BE&isadv=0&isfilter=1&p={}&re=2043','http://sou.zhaopin.com/jobs/searchresult.ashx?jl=765&kw=%E5%A4%96%E8%B4%B8&sm=0&isfilter=1&p={}&re=2362','http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=%E4%BE%9B%E5%BA%94%E9%93%BE&isadv=0&isfilter=1&p={}&re=2362']
    try:
        exists=[line.replace('\n','') for line in open('Zhilianexists.txt','r',encoding='utf-8')]
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
            print(page,'--ok')
            page+=1
    f=open('Zhilianexists.txt','w',encoding='utf-8')
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
    for item in result:
        for i in item:
            text+=i+'\n'
        text+='\n\n'
        count+=1
        if count<10:
            continue
        Count=loademail()
        try:
            sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 智联',text)
        except:
            print('Send email Failed!')
        count=0
        text=''
    if text=='':
        return
    Count=loademail()
    try:
        sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 智联',text)
    except:
        print('Send email Failed!')

def getCjUrl():
    need_place=['http://s.cjol.com/l200809-200805-200808-kw-%E5%A4%96%E8%B4%B8/?SearchType=1&KeywordType=3&page={}#utm_source=4','http://s.cjol.com/l200809-200805-200808-kw-%E4%BE%9B%E5%BA%94%E9%93%BE/?SearchType=3&KeywordType=3&page={}']
    try:
        exists=[line.replace('\n','') for line in open('cjolexists.txt','r',encoding='utf-8')]
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
            print(page,'--ok')
            page+=1
            if(page==20):
                break
    f=open('cjolexists.txt','w',encoding='utf-8')
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
    for item in result:
        for i in item:
            text+=i+'\n'
        text+='\n\n'
        count+=1
        if count<10:
            continue
        Count=loademail()
        try:
            sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 人才在线',text)
        except:
            print('Send email Failed!')
        count=0
        text=''
    if text=='':
        return
    Count=loademail()
    try:
        sendEmail(Count[0],Count[1],'2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 人才在线',text)
    except:
        print('Send email Failed!')

count=input("输入间隔时间(分钟)：")
try:
    count=int(count)
except:
    count=10
while True:
    Company58()
    Company51()
    CompanyZhilian()
    CompanyCj()
    print('Wait')
    time.sleep(count*60)
