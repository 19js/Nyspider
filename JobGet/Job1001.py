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
    need_place=['http://www.job1001.com/SearchResult.php?page={}&region_1=440300&region_2=440300&region_3=&keytypes=&jtzw=%CD%E2%C3%B3']
    try:
        exists=[line.replace('\n','') for line in open('temp/1001_exists.txt','r',encoding='utf-8')]
    except:
        exists=[]
    result=[]
    today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    for placeurl in need_place:
        page=0
        state=True
        while state:
            try:
                html=requests.get(placeurl.format(page),headers=headers,timeout=30).text#.encode('ISO-8859-1').decode('gbk','ignore')
                table=BeautifulSoup(html,'lxml').find('div',{'class':'search_data'}).find_all('ul',{'class':'search_result'})
                for item in table:
                    lis=item.find_all('li')
                    company_name=lis[1].find('a').get('title')
                    company_url=lis[1].find('a').get('href')
                    if company_name in exists:
                        continue
                    date=lis[3].get_text()
                    if today not in date:
                        state=False
                        break
                    exists.append(company_name)
                    job_name=item.find('a').get('title')
                    job_url=item.find('a').get('href')
                    area=lis[2].get_text()
                    result.append(["【公司名称】:"+company_name,"【职位】:"+job_name,"【工作地点】:"+area,'http://www.job1001.com'+job_url,'http://www.job1001.com'+company_url])
            except:
                break
            time.sleep(random.randint(random_int_from,random_int_to))
            print('一览英才','Page',page,'-- OK')
            if page==30:
                break
            page+=1
    f=open('temp/1001_exists.txt','w',encoding='utf-8')
    for line in exists:
        f.write(line+'\n')
    f.close()
    return result

def get_job_info(job_url):
    html=requests.get(job_url,headers=headers,timeout=30).text#.encode('ISO-8859-1').decode('gbk','ignore')
    soup=BeautifulSoup(html,'lxml')
    header=soup.find('div',id='header_c')
    result=[]
    try:
        company_address=header.find('div',{'class':'company_address'}).get_text()
    except:
        company_address=''
    try:
        follow_count=header.find('span',id='follow_count').get_text()
    except:
        follow_count=''
    try:
        job_info_detail=soup.find('div',{'class':'job_info_detail'}).find_all('li')
        for li in job_info_detail:
            line=li.get_text()
            for key in ['公司性质','公司规模','所属行业','所在地区','公司主页']:
                line=line.replace(key,'【%s】'%key)
            result.append(line)
    except:
        pass
    result.append("【关注数】:"+follow_count)
    result.append("【公司地址】:"+company_address)
    area=''
    for key in area_keys:
        for a_key in area_keys[key]:
            if a_key in company_address:
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
            send_email(email_config[0], email_config[1], email_config[2],"%s -- 一览英才"%now, email_text)
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
