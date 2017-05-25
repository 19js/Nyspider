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
random_int_from=1
random_int_to=2

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
    need_place=['http://sz.58.com/longgang/job/pn{}/?key=%E5%A4%96%E8%B4%B8&final=1&PGTID=0d302408-0071-59c5-0976-c3b629d87a8c&ClickID=2'
                ,'http://sz.58.com/job/pn{}/?key=%E5%A4%96%E8%B4%B8%2B%E5%9D%AA%E5%B1%B1%E6%96%B0%E5%8C%BA&cmcskey=%E5%A4%96%E8%B4%B8%2B%E5%9D%AA%E5%B1%B1%E6%96%B0%E5%8C%BA&final=1&jump=1&specialtype=gls&PGTID=0d302408-0000-4a66-ba02-d183ded70960&ClickID=2'
                ,'http://sz.58.com/dapengxq/job/pn{}/?key=%E5%A4%96%E8%B4%B8%2B%E5%A4%A7%E9%B9%8F%E6%96%B0%E5%8C%BA&cmcskey=%E5%A4%96%E8%B4%B8%2B%E5%A4%A7%E9%B9%8F%E6%96%B0%E5%8C%BA&final=1&jump=1&specialtype=gls'
                ,'http://sz.58.com/buji/job/pn{}/?key=%E5%A4%96%E8%B4%B8%2B%E5%B8%83%E5%90%89&cmcskey=%E5%A4%96%E8%B4%B8%2B%E5%B8%83%E5%90%89&final=1&jump=1&specialtype=gls&PGTID=0d302408-0073-f545-264b-e6b7fc334ad9&ClickID=2']
    try:
        exists=[line.replace('\n','') for line in open('temp/58_exists.txt','r',encoding='utf-8')]
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
                    company_name=item.find('a',{'class':'fl'}).get('title').replace(' ','')
                    company_url=item.find('a',{'class':'fl'}).get('href')
                    if company_name in exists:
                        continue
                    date=item.find_all('dd')[-1].get_text().replace('\r','').replace('\n','').replace(' ','')
                    if date=='精准':
                        continue
                    if date!='精准' and date!='今天' and '小时' not in date and '分钟' not in date:
                        statue=False
                        break
                    exists.append(company_name)
                    area=item.find_all('dd')[-2].get_text()
                    job_name=item.find('a').get_text()
                    job_url=item.find('a').get('href')
                    line=["【公司名称】:"+company_name,company_url,"【商圈】:"+area,"【职位】:"+job_name,job_url,"【更新时间】:"+date]
                    result.append(line)
            except:
                break
            time.sleep(random.randint(random_int_from,random_int_to))
            print('58','Page',page,'-- OK')
            page+=1
    f=open('temp/58_exists.txt','w',encoding='utf-8')
    for line in exists:
        f.write(line+'\n')
    f.close()
    return result

def get_job_info(job_url):
    html=requests.get(job_url,headers=headers,timeout=30).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'con'})
    job_des=soup.find('div',{'class':'posDes'}).get_text()
    company_des=soup.find('div',{'class':'intro'}).get_text()
    join_num=soup.find('span',{'class':'item_num join58_num'}).get_text()
    company_address=soup.find('p',{'class':'detail_adress'}).get_text()
    area=''
    for key in area_keys:
        for a_key in area_keys[key]:
            if a_key in company_address:
                area=key
                break
        if area!='':
            break
    return ["【职位描述】:"+job_des,"【公司介绍】:"+company_des,"【加入58时间】:"+join_num,"【公司地址】:"+company_address,"【区域】:"+area]

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
                info=get_job_info(job[-2])
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
            send_email(email_config[0], email_config[1], email_config[2],"%s -- 58"%now, email_text)
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'Send Email OK')
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'Send Email Failed',e)
        print("Sleep")
        time.sleep(sleep_time)

def job_58():
    switch=input("1.导出已采集数据.\n2.采集.\n")
    if switch=='1':
        load_data_to_excel()
    else:
        crawl()

job_58()
