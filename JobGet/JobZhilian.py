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
    need_place=['http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=%E5%A4%96%E8%B4%B8&sb=0&sm=0&re=2042&isfilter=1&fl=765&isadv=0&p={}'
                ,'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=%E5%A4%96%E8%B4%B8&isadv=0&isfilter=1&p={}&re=2362'
                ,'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=%E5%A4%96%E8%B4%B8&isadv=0&isfilter=1&p={}&re=2043']
    try:
        exists=[line.replace('\n','') for line in open('temp/zhilian_exists.txt','r',encoding='utf-8')]
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
                    company_name=item.find('td',attrs={'class':'gsmc'}).find('a').get_text().replace('\r','').replace('\n','').replace(' ','')
                    company_url=item.find('td',attrs={'class':'gsmc'}).find('a').get('href')
                    if company_name in exists:
                        continue
                    date=item.find('td',{'class':'gxsj'}).get_text().replace('\r','').replace('\n','').replace(' ','')
                    if '今天' not in date and '小时' not in date and '刚刚' not in date and '分钟' not in date:
                        statue=False
                        break
                    exists.append(company_name)
                    area=item.find('td',{'class':'gzdd'}).get_text().replace('\r\n','').replace(' ','')
                    job_name=item.find('a').get_text().replace('\r\n','').replace(' ','')
                    job_url=item.find('a').get('href')
                    result.append(["【公司名称】:"+company_name,"【职位】:"+job_name,"【工作地点】:"+area,'【时间】:'+date,job_url,company_url])
            except Exception as e:
                statue=False
                break
            time.sleep(random.randint(random_int_from,random_int_to))
            print('智联','Page',page,'-- OK')
            page+=1
    f=open('temp/zhilian_exists.txt','w',encoding='utf-8')
    for line in exists:
        f.write(line+'\n')
    f.close()
    return result

def get_company_info(company_url):
    html=requests.get(company_url,headers=headers,timeout=30).text#.encode('ISO-8859-1').decode('gbk','ignore')
    table=BeautifulSoup(html,'lxml').find('div',{'class':'mainLeft'})
    result=[]
    des=table.find('table',{'class':'comTinyDes'}).find_all('tr')
    for item in des:
        try:
            line=item.get_text().replace('\n','')
            for key in ['公司性质','公司规模','公司行业','公司地址','公司网站']:
                line=line.replace(key,'【%s】'%key)
            result.append(line)
        except:
            continue
    area=''
    for key in area_keys:
        for a_key in area_keys[key]:
            if a_key in str(result):
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
            send_email(email_config[0], email_config[1], email_config[2],"%s -- 智联招聘"%now, email_text)
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'Send Email OK')
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'Send Email Failed',e)
        print("Sleep")
        time.sleep(sleep_time)

def job_zhilian():
    switch=input("1.导出已采集数据.\n2.采集.\n")
    if switch=='1':
        load_data_to_excel()
    else:
        crawl()

job_zhilian()
