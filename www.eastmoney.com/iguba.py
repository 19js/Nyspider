import requests
from bs4 import BeautifulSoup
import json
import time
import re
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
import smtplib

headers = {
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}


def load_urls():
    users=[]
    for line in open('data/users.txt','r',encoding='utf-8'):
        line=line.replace('\r','').replace('\n','')
        users.append(line.split('|')[-1].split('/')[-1])
    return users

def user_reply(uid):
    url='http://iguba.eastmoney.com/action.aspx?action=getuserreply&uid=%s'%uid
    count=0
    while True:
        try:
            html=requests.get(url,headers=headers,timeout=30).text
            break
        except:
            count+=1
            if count==3:
                return []
    result=[]
    data=json.loads(html)['re']
    for item in data:
        try:
            reply_id=item['id']
            content=item['te']
            name=item['nc']
            result.append([reply_id,name,content,''])
        except:
            continue
    return result

def user_article(uid):
    url='http://iguba.eastmoney.com/'+str(uid)
    count=0
    while True:
        try:
            html=requests.get(url,headers=headers,timeout=30).text
            break
        except:
            count+=1
            if count==3:
                return []
    data=re.findall('var itemdata = ({.*?});',html)[0]
    result=[]
    for item in eval(data)['re']:
        try:
            article_id=item['id']
            name=item['nc']
            title=item['tt']
            content=item['te']
            result.append([article_id,name,title,content])
        except:
            pass
    return result

def main():
    users=load_urls()
    cache={}
    for uid in users:
        cache[uid]={}
        try:
            articles=user_article(uid)
        except:
            articles=[]
        try:
            reply=user_reply(uid)
        except:
            reply=[]
        cache[uid]['article']=[]
        cache[uid]['reply']=[]
        for item  in articles:
            cache[uid]['article'].append(item[0])
        for item  in reply:
            cache[uid]['reply'].append(item[0])
    while True:
        for uid in users:
            try:
                articles=user_article(uid)
            except:
                articles=[]
            try:
                reply=user_reply(uid)
            except:
                reply=[]
            result=[]
            for item  in articles:
                if item[0] not in cache[uid]['article']:
                    result.append(item)
                    cache[uid]['article'].append(item[0])
            for item  in reply:
                if item[0] not in cache[uid]['reply']:
                    result.append(item)
                    cache[uid]['reply'].append(item[0])
            if result==[]:
                continue
            try:
                send(result)
            except:
                pass
        time.sleep(30)
        timenow=time.strftime("%y-%m-%d %H:%M:%S")
        print(timenow,'ok')

def send(result):
    try:
        data=open('data/email.txt','r',encoding='utf-8').read()
        data=eval(data)
    except:
        print("邮箱配置文件有误！")
        time.sleep(100)
        return False
    subject=result[0][1]+'--有更新'
    text=''
    for item in result:
        text+=item[2]+'\r\n'+item[3]+'\r\n\r\n'
    timenow=time.strftime("%y-%m-%d %H:%M:%S")
    try:
        sendEmail(data['email'],data['passwd'],subject,text)
        print(timenow,"发送成功")
    except:
        print(timenow,"发送失败")

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def sendEmail(fromemail,passwd,subject,text):
    toemail='advovo@126.com'
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject']=subject
    msg['From'] = _format_addr(fromemail)#.replace('foxmail','sailnetwork'))
    msg['To'] = _format_addr(toemail)
    server=smtplib.SMTP()
    #server.connect('smtp.qiye.163.com')
    server=smtplib.SMTP_SSL('smtp.qq.com')
    server.ehlo('smtp.qq.com')
    server.login(fromemail,passwd)
    server.sendmail(fromemail, [toemail], msg.as_string())
    server.quit()

main()
