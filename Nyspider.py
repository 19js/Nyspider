#coding:utf-8

import requests
import os
import sqlite3
import xlwt3
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
import smtplib
import datetime

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_image(image_url,image_name):
    content=requests.get(image_url,headers=headers).content
    with open(image_name,'wb') as f:
        f.write(content)
        f.close

def to_Excel():
    for filename in os.listdir('.'):
        if(filename.endswith('txt')):
            f_d=open(filename,'r')
            f_ex=xlwt3.Workbook()
            sheet=f_ex.add_sheet('one')
            count=0
            for line in f_d.readlines():
                lists=line.split('|')
                try:
                    num=0
                    for text in lists:
                        sheet.write(count,num,text)
                        num+=1
                    count+=1
                except:
                    sheet=f_ex.add_sheet('two')
                    count=0
                    num=0
                    for text in lists:
                        sheet.write(count,num,text)
                        num+=1
                    count+=1
            f_ex.save(filename.replace('txt','xls'))

def send_email(email,subject,text,user,passwd):
    smtp_server='smtp.126.com'
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject']=subject
    msg['From'] = _format_addr(user)
    msg['To'] = _format_addr(email)
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(user, passwd)
    server.sendmail(user, [email], msg.as_string())
    server.quit()

def convert_html(html):
    return html.encode('ISO-8859-1').decode('utf-8','ignore')

def Duplicate():
    for filename in os.listdir('.'):
        if filename.endswith('txt'):
            lines=open(filename,'r').readlines()
            lines=list(set(lines))
            lines.sort()
            f=open(filename,'w')
            for line in lines:
                f.write(line)
            f.close()

def yesterday_get(today=datetime.datetime.now()):
    oneday = datetime.timedelta(days=1)
    yesterday = today- oneday
    return yesterday
