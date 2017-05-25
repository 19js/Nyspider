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

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    'Host':'www.globalsources.com',
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

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

def get_type_list():
    url='http://www.globalsources.com/new-products/NL0/Listing.htm'
    html=requests.get(url,headers=headers,timeout=30).text
    soup=BeautifulSoup(html,'lxml').find_all('div',{'class':'margintop'})
    result=[]
    for item in soup:
        try:
            result.append('http://www.globalsources.com/'+item.find('a').get('href'))
        except:
            continue
    return result

def get_allow_company_urls(url):
    html=requests.get(url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find_all('div',{'class':'detail_supplierInfo'})
    result=[]
    for item in table:
        try:
            a=item.find('p',{'class':'detail_supName'}).find('a')
            title=a.get_text()
            if 'shenzhen' not in title.lower():
                continue
            url=a.get('href')
            memberSince=item.find('span',{'class':'detail_supYear'}).get_text()
            if '1st year' in memberSince:
                if [title,url] in result:
                    continue
                result.append([title,url])
        except Exception as e:
            #print('[Error][get_allow_company_urls]',e)
            continue
    return result

def get_company_info(url):
    html=requests.get(url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'VBinformaition'}).find_all('p')
    company_name=''
    address=''
    number=''
    for item in table:
        try:
            text=item.get_text().replace('\r','').replace('\n','').replace('\t','')
        except:
            continue
        if 'Registered Company:' in text:
            company_name=text.replace('Registered Company:','')
        if 'Business Registration Number:' in text:
            number=text.replace('Business Registration Number:','')
        if 'Company Registration Address:' in text:
            address=text.replace('Company Registration Address:','')
    area=''
    area_keys={'龙岗':['龙岗','坪山新区','坑梓','大鹏新区'],
                '深圳市区':['南山','罗湖','福田','盐田','前海'],
                '龙华新区':['龙华新区'],
                '宝安':['宝安','光明新区','公明']}
    for key in area_keys:
        for a_key in area_keys[key]:
            if a_key in address:
                area=key
                break
        if area!='':
            break
    return [company_name,number,address,area]

def get_contact_info(url):
    html=requests.get(url,headers=headers,timeout=30).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'contactUs'})
    table=soup.find('div',{'class':'proDetCont'}).find_all('div')
    need_keys=['Phone Number:','Mobile:','Other Homepage Address:','Homepage Address:','Address:']
    length=len(need_keys)
    result=['']*length
    for item in table:
        text=item.get_text().replace('\r','').replace('\n','').replace('\t','').replace("&nbsp;",'').replace('\xa0','')
        for index in range(length):
            if need_keys[index] in text:
                result[index]=text.replace(need_keys[index],'')
                break
    result[-1],result[-3]=result[-3],result[-1]
    try:
        contName=soup.find('p',{'class':'contName'}).get_text().replace('\r','').replace('\n','').replace('\t','').replace('\xa0',' ')
    except:
        contName=''
    result.insert(0,contName)
    return result

def write_to_txt(result):
    f=open('temp.txt','a',encoding='utf-8')
    today=time.strftime("%Y-%m-%d", time.localtime())
    for line in result:
        f.write(str([today]+line)+'\r\n')
    f.close()

def load_today_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in open('temp.txt','r',encoding='utf-8'):
        try:
            line=eval(line)
            sheet.append(line)
        except:
            continue
    excel.save('result.xlsx')

def load_exists():
    exists={}
    for line in open('temp.txt','r',encoding='utf-8'):
        try:
            line=eval(line)
            url=line[-1]
            exists[url]=1
        except:
            continue
    return exists

def crawl():
    try:
        sleep_time=input("输入采集间隔(S):")
        sleep_time=int(sleep_time)
    except:
        sleep_time=600

    try:
        types=get_type_list()
    except Exception as e:
        print('获取分类失败',e)
        return

    try:
        email_config=load_email()
    except Exception as e:
        print('获取Email失败',e)
        return

    try:
        exists=load_exists()
    except:
        exists={}
    while True:
        result=[]
        for type_url in types:
            try:
                companys=get_allow_company_urls(type_url)
            except Exception as e:
                #print('Error[company urls][%s]'%type_url,e)
                continue
            for company in companys:
                if company[1] in exists:
                    continue
                try:
                    base_info=get_company_info(company[1])
                    contact_info=get_contact_info(company[1].replace('Homepage','ContactUs'))
                except Exception as e:
                    continue
                exists[company[1]]=1
                try:
                    print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'Company: ',company[0])
                except:
                    pass
                result.append([company[0]]+base_info+contact_info+[company[1]])
                time.sleep(random.randint(5,20))
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),type_url.replace('http://www.globalsources.com//new-products/',''),'OK')
            time.sleep(random.randint(5,20))
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'抓取完成')
        if len(result)==0:
            print("Sleep")
            time.sleep(sleep_time)
            continue
        write_to_txt(result)
        text=''
        for line in result:
            text+='\r\n'.join(line)+'\r\n'+'-----'*10+'\r\n\r\n'
        now=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        try:
            send_email(email_config[0], email_config[1], email_config[2],"%s--公司信息"%now, text)
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'Send Email OK')
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'Send Email Failed',e)
        print("Sleep")
        time.sleep(sleep_time)

def globalsources():
    switch=input("1.导出今天采集数据.\n2.采集.\n")
    if switch=='1':
        load_today_to_excel()
    else:
        crawl()

globalsources()
