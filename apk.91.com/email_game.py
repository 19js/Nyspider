#coding:utf-8
import requests
from bs4 import BeautifulSoup
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
import smtplib
import random
import sqlite3
import time

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def get_urls(url):
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html).find('ul',id='rptSoft').find_all('li')
    items=[]
    for item in table:
        infor={}
        a=item.find('h4').find('a')
        infor['name']=a.get_text()
        infor['url']='http://apk.91.com'+a.get('href')
        items.append(infor)
    return items

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def get_email(item):
    html=requests.get(item['url'],headers=headers,timeout=50).text
    table=BeautifulSoup(html).find('div',attrs={'class':'s_intro_txt clearfix fr p_r'}).find('ul',attrs={'class':'s_info'}).find_all('li')
    email=''
    for i in table:
        if i.get_text()[:4]=='联系邮箱':
            try:
                email=i.find('a').get_text()
            except:
                email=''
    item['email']=email
    return item

class Send_email():
    def __init__(self):
        self.smtp_server = 'smtp.126.com'
        self.get_users()
        self.get_text()

    def get_users(self):
        f=open('email_A.txt','r')
        self.email_A=[]
        for line in f.readlines():
            usr={}
            item=line.split('---')
            usr['user']=item[0].replace(' ','')
            usr['passwd']=item[1].replace('\r\n','').replace('\n','').replace(' ','')
            self.email_A.append(usr)
        f.close()
        f=open('email_B.txt','r')
        self.email_B=[]
        for line in f.readlines():
            usr={}
            item=line.split('---')
            try:
                usr['user']=item[0].replace(' ','')
                usr['passwd']=item[1].replace('\r\n','').replace('\n','').replace(' ','')
            except:
                continue
            self.email_B.append(usr)
        f.close()

    def get_text(self):
        self.text_A=open('text_A.txt','r').read()
        self.text_B=open('text_B.txt','r').read()

    def send_email_a(self,email,subject):
        try:
            index=random.randint(0,len(self.email_A)-1)
            msg = MIMEText(self.text_A, 'plain', 'utf-8')
            msg['Subject']=subject
            msg['From'] = _format_addr(self.email_A[index]['user'])
            msg['To'] = _format_addr(email)
            server = smtplib.SMTP(self.smtp_server, 25)
            server.set_debuglevel(1)
            server.login(self.email_A[index]['user'], self.email_A[index]['passwd'])
            server.sendmail(self.email_A[index]['user'], [email], msg.as_string())
            server.quit()
        except:
            return

    def send_email_b(self,email,subject):
        try:
            index=random.randint(0,len(self.email_B)-1)
            msg = MIMEText(self.text_B, 'plain', 'utf-8')
            msg['Subject']=subject
            msg['From'] = _format_addr(self.email_B[index]['user'])
            msg['To'] = _format_addr(email)
            server = smtplib.SMTP(self.smtp_server, 25)
            server.set_debuglevel(1)
            server.login(self.email_B[index]['user'], self.email_B[index]['passwd'])
            server.sendmail(self.email_B[index]['user'], [email], msg.as_string())
            server.quit()
        except:
            return


class Main():
    def __init__(self):
        self.conn=sqlite3.connect('urls.db')
        self.cursor=self.conn.cursor()
        self.cursor.execute("create table if not exists urls(url TEXT primary key)")
        self.voted_count=0
        self.send_email=Send_email()
        self.game_f=open('game.txt','a',encoding='utf-8')
        self.soft_f=open('soft.txt','a',encoding='utf-8')

    def run(self):
        self.game()
        self.game_f.close()
        self.soft_f.close()
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def game(self):
        page=0
        while(page<20):
            page+=1
            try:
                items=get_urls('http://apk.91.com/game/0_'+str(page)+'_5')
            except:
                time.sleep(30)
                continue
            for item in items:
                time.sleep(5)
                if(self.voted_count==10):
                    return
                ok=self.is_voted(item['url'])
                try:
                    text=get_email(item)
                except:
                    time.sleep(30)
                    text['email']=''
                self.game_f.write(text['name']+'---'+text['email']+'\r\n')
                if(text['email']==''):
                    continue
                if(ok):
                    self.send_email.send_email_a(text['email'],text['name'])
                else:
                    self.send_email.send_email_b(text['email'],text['name'])
        self.voted_count=0

    def is_voted(self,url):
        try:
            self.cursor.execute("insert into urls(url) values(?)",(url,))
            self.conn.commit()
            self.voted_count=0
            return True
        except:
            self.voted_count+=1
            return False

work=Main()
work.run()
