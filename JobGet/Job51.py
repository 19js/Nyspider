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
import logging

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Host":"search.51job.com",
    "User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

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
    need_place=['http://search.51job.com/list/040000,000000,0000,00,9,99,%25E5%25A4%2596%25E8%25B4%25B8%252B%25E9%25BE%2599%25E5%25B2%2597,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=1&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
                ,'http://search.51job.com/list/040000,000000,0000,00,9,99,%25E5%25A4%2596%25E8%25B4%25B8%252B%25E5%259D%25AA%25E5%25B1%25B1,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=1&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
                ,'http://search.51job.com/list/040000,000000,0000,00,9,99,%25E5%25A4%2596%25E8%25B4%25B8%252B%25E5%25A4%25A7%25E9%25B9%258F,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=1&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']
    try:
        exists=[line.replace('\n','') for line in open('temp/51_exists.txt','r',encoding='utf-8')]
    except:
        exists=[]
    result=[]
    today=time.strftime('%m-%d',time.localtime(time.time()))
    for placeurl in need_place:
        page=1
        state=True
        while state:
            try:
                html=requests.get(placeurl.format(page),headers=headers,timeout=30).text.encode('ISO-8859-1').decode('gbk','ignore')
                table=BeautifulSoup(html,'lxml').find('div',id='resultList').find_all('div',attrs={'class':'el'})
                for item in table[1:]:
                    try:
                        company_name=item.find('span',{'class':'t2'}).get_text().replace(' ','')
                        company_url=item.find('span',{'class':'t2'}).find('a').get('href')
                        if company_name in exists:
                            continue
                        update_date=item.find('span',{'class':'t5'}).get_text()
                        if update_date not in today:
                            state=False
                            break
                        exists.append(company_name)
                        area=item.find('span',{'class':'t3'}).get_text().replace('\r\n','').replace(' ','')
                        job_name=item.find('a').get_text().replace('\r\n','').replace(' ','')
                        job_url=item.find('a').get('href')
                    except:
                        continue
                    result.append(["【公司名称】:"+company_name,"【职位】:"+job_name,"【商圈】:"+area,job_url,company_url])
            except Exception as e:
                break
            time.sleep(random.randint(random_int_from,random_int_to))
            print('前程无忧','Page',page,'-- OK')
            page+=1
    f=open('temp/51_exists.txt','w',encoding='utf-8')
    for line in exists:
        f.write(line+'\n')
    f.close()
    return result

def get_company_info(job_url):
    html=requests.get(job_url,headers=headers,timeout=30).text.encode('ISO-8859-1').decode('gbk','ignore')
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
        result.append("【公司介绍】:"+instro)
        try:
            boot=div.find_all('div',{'class':'bmsg'})
            for item in boot:
                result.append(item.find('p').get_text().replace('公司地址','【公司地址】').replace('公司官网','【公司官网】'))
        except:
            pass
    except:
        pass
    area=''
    for key in area_keys:
        for a_key in area_keys[key]:
            if a_key in result[-1]:
                area=key
                break
        if area!='':
            break
    result.append("【区域】:"+area)
    return [item.replace('\r','').replace('\n','').replace('\t','').replace('\xa0','') for item in result]

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
            send_email(email_config[0], email_config[1], email_config[2],"%s -- 前程无忧"%now, email_text)
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'Send Email OK')
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'Send Email Failed',e)
        print("Sleep")
        time.sleep(sleep_time)

def job_51():
    switch=input("1.导出已采集数据.\n2.采集.\n")
    if switch=='1':
        load_data_to_excel()
    else:
        crawl()

job_51()
