from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
import smtplib
import time
import os
import json


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def sendEmail(fromemail,passwd,toemail,subject,text):
    msg = MIMEText(text, 'html', 'utf-8')
    msg['Subject']=subject
    msg['From'] = _format_addr(fromemail.replace('foxmail','sailnetwork'))
    msg['To'] = _format_addr(toemail)
    server=smtplib.SMTP_SSL('smtp.qq.com')
    server.ehlo('smtp.qq.com')
    server.login(fromemail,passwd)
    server.sendmail(fromemail, [toemail], msg.as_string())
    server.quit()

def load_emails(filename):
    f=open('email/'+filename,'r',encoding='utf-8').read()
    emails=[]
    for item in f.split('---'*8):
        try:
            lines=item.split('***'*4)
            subject=lines[0].replace('\r\n','')
            email=lines[1].replace('\r\n','').replace(' ','')
            text=lines[2]
            emails.append([email,subject,text])
        except:
            continue
    return emails

def load_login():
    f=open('./email.json','r',encoding='utf8')
    data=json.load(f)
    return data

def main():
    try:
        data=load_login()
        fromemail=data['fromemail']
        passwd=data['passwd']
        toemail=data['toemail']
    except:
        print("帐号导入失败")
        return
    for filename in os.listdir('email'):
        try:
            emails=load_emails(filename)
        except:
            print(filename,'load failed')
        for i in range(len(emails)):
            try:
                email=emails[i]
                subject=email[1].replace('\r','').replace('\n','').replace('\t','').replace(' ','')+'\t'+email[0].replace('\r','').replace('\n','').replace('\t','').replace(' ','')
            except:
                continue
            try:
                sendEmail(fromemail,passwd,toemail,subject,email[2])
                time.sleep(2)
                print(subject,'send ok')
            except:
                print(subject,'failed')
    print(filename,'完成')
                
main()
time.sleep(60)
