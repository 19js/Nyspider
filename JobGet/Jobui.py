import requests
from bs4 import BeautifulSoup
import openpyxl
import time
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
import smtplib
import random
import os
import re

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

area_keys={'龙岗':['龙岗','坪山新区','坑梓','大鹏新区'],
            '深圳市区':['南山','罗湖','福田','盐田','前海'],
            '龙华新区':['龙华新区'],
            '宝安':['宝安','光明新区','公明']}
places=['龙岗','坪山','坑梓','大鹏','坪地','平湖','布吉','坂田','横岗']
random_int_from=5
random_int_to=20

try:
    os.mkdir('temp')
except:
    pass

def load_email():
    text=open('Email.txt','r',encoding='utf-8').read()
    text=text.replace('\r','').replace('\n','').replace(' ','').replace('\t','')
    result=text.split('---')
    return result

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_email(fromemail,passwd,toemail,subject,text):
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject']=subject
    msg['From'] = _format_addr(fromemail)
    msg['To'] = _format_addr(toemail)
    server=smtplib.SMTP_SSL('smtp.qq.com')
    server.ehlo('smtp.qq.com')
    server.login(fromemail,passwd)
    server.sendmail(fromemail, [toemail], msg.as_string())
    server.quit()

def get_company_urls():
    need_place=['http://www.jobui.com/jobs?jobKw=%E5%A4%96%E8%B4%B8&cityKw=%E6%B7%B1%E5%9C%B3&areaCode=190305&sortField=last&n={}']
    try:
        exists=[line.replace('\n','') for line in open('temp/jobui_exists.txt','r',encoding='utf-8')]
    except:
        exists=[]
    result=[]
    for placeurl in need_place:
        page=1
        state=True
        while state:
            try:
                html=requests.get(placeurl.format(page),headers=headers,timeout=30).text.replace('\t','')
            except:
                continue
            try:
                table=BeautifulSoup(html,'lxml').find('ul',{'class':'searcher-job-detail'}).find_all('li')
                for item in table:
                    if 'style="padding:10px 0"' in str(item):
                        continue
                    searchTitTxt=item.find('div',{'class':'searchTitTxt'})
                    job_name=searchTitTxt.find('a').get('title')
                    job_url=searchTitTxt.find('a').get('href')
                    company_name=item.find('a').get('title')
                    if company_name in exists:
                        continue
                    company_url=item.find('a').get('href')
                    try:
                        spans=searchTitTxt.find('div',{'class':'fs16 mb5'}).find_all('span')
                        update_time=spans[-1].get_text()
                        company_type=spans[-2].get_text()
                        company_type=re.sub('\d+次浏览','',company_type)
                    except:
                        update_time='-'
                        company_type='-'
                    if '天' in update_time or '5小时' in update_time or '6小时' in update_time:
                        state=False
                        break
                    try:
                        job_des=searchTitTxt.find('div',{'class':'gray6 mb5'}).get_text()
                    except:
                        job_des='-'
                    exists.append(company_name)
                    result.append(["【公司名称】:"+company_name,"【职位】:"+job_name,"【行业】:"+company_type,"【职位介绍】:"+job_des,"【更新时间】:"+update_time,'http://www.jobui.com/'+job_url,'http://www.jobui.com/'+company_url])
            except:
                break
            time.sleep(random.randint(random_int_from,random_int_to))
            print('职友集','Page',page,'--ok')
            page+=1
    f=open('temp/jobui_exists.txt','w',encoding='utf-8')
    for line in exists:
        f.write(line+'\n')
    f.close()
    return result

def get_company_info(company_url):
    html=requests.get(company_url,headers=headers,timeout=30).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'aleft'})
    result=[]
    try:
        des='【公司介绍】:'+soup.find('div',{'class':'intro'}).get_text()
    except:
        des='【公司介绍】:'
    address='【公司地址】:'
    contact='【联系我们】:'
    try:
        dls=soup.find_all('dl',{'class':'dlli fs16'})
        for dl in dls:
            text=dl.get_text()
            if '公司地址' in text:
                address=text.replace('公司地址','【公司地址】')
            elif '联系我们' in text:
                contact=text.replace('联系我们','【联系我们】')
    except:
        pass
    result=[des,address,contact]
    area=''
    for key in area_keys:
        for a_key in area_keys[key]:
            if a_key in address:
                area=key
                break
        if area!='':
            break
    result.append("【区域】:"+area)
    return result

def write_to_txt(result):
    f=open('temp/temp.txt','a',encoding='utf-8')
    today=time.strftime("%Y-%m-%d", time.localtime())
    for line in result:
        f.write(str([today]+line)+'\r\n')
    f.close()

def load_data_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in open('temp/temp.txt','r',encoding='utf-8'):
        try:
            line=eval(line)
            sheet.append(line)
        except:
            continue
    excel.save('result.xlsx')

def crawl():
    try:
        sleep_time=input("输入采集间隔(S):")
        sleep_time=int(sleep_time)
    except:
        sleep_time=600

    try:
        email_config=load_email()
    except Exception as e:
        return

    while True:
        jobs=get_company_urls()
        result=[]
        for job in jobs:
            try:
                info=get_company_info(job[-1])
            except Exception as e:
                time.sleep(random.randint(random_int_from,random_int_to))
                continue
            line=job+info
            result.append([str(i).replace('\r','').replace('\n','') for i in line])
            time.sleep(random.randint(random_int_from,random_int_to))
        if len(result)==0:
            print("Sleep")
            time.sleep(sleep_time)
            continue
        write_to_txt(result)
        email_text=''
        for line in result:
            text='\r\n'.join(line)+'\r\n'+'-----'*10+'\r\n\r\n'
            for key in places:
                if key in text:
                    email_text+=text
                    break
        now=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        try:
            send_email(email_config[0], email_config[1], email_config[2],"%s -- 职友集"%now, email_text)
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'Send Email OK')
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'Send Email Failed',e)
        print("Sleep")
        time.sleep(sleep_time)

def job_1001():
    switch=input("1.导出已采集数据.\n2.采集.\n")
    if switch=='1':
        load_data_to_excel()
    else:
        crawl()

job_1001()
