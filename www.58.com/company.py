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

def getUrl():
    need_place=['http://sz.58.com/longgang/job/pn{}/?key=%E5%A4%96%E8%B4%B8&final=1&PGTID=0d302408-0071-58f4-3029-be8d66a87263&ClickID=1','http://sz.58.com/buji/job/pn{}/?key=%E5%A4%96%E8%B4%B8&final=1&PGTID=0d302408-0073-f61f-4c28-4b6858e1ad08&ClickID=2','http://sz.58.com/pingshanxinqu/job/pn{}/?key=%E5%A4%96%E8%B4%B8&final=1&PGTID=0d302408-02c5-3892-1dd5-f756b777b251&ClickID=1']
    try:
        exists=[line.replace('\n','') for line in open('exists.txt','r')]
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
    f=open('exists.txt','w')
    for line in exists:
        f.write(line+'\n')
    f.close()
    return result

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

def companyInfor(url):
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

def main():
    urls=getUrl()
    print('New--',len(urls))
    result=[]
    for item in urls:
        try:
            company=companyInfor(item[-1])
        except:
            continue
        time.sleep(1)
        result.append(item+company)
    if len(result)==0:
        return
    text=''
    for item in result:
        for i in item:
            text+=i+'\n'
        text+='\n\n'
    try:
        sendEmail('2678916720@qq.com','8yjgjeqsin','2786203719@qq.com',time.strftime("%Y-%m-%d %H:%M:%S")+'-- 58',text)
    except:
        print('Send email Failed!')

count=input("输入间隔时间(分钟)：")
try:
    count=int(count)
except:
    count=10
while True:
    main()
    print('Wait')
    time.sleep(count*60)
