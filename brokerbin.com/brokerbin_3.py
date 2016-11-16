import requests
from bs4 import BeautifulSoup
import time
import re
import json
import chardet

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


email_template=open('email_template','r',encoding='utf-8').read()
filter_emails=[]

def get_chardet(filename):
    data=open(filename,'rb').read()
    coding=chardet.detect(data)
    encoding=coding['encoding']
    if encoding=='GB2312':
        encoding='GBK'
    return encoding

def load_filter():
    try:
        encoding=get_chardet('./filter/filter.txt')
    except:
        encoding='utf-8'
    global filter_emails
    for line in open('./filter/filter.txt','r',encoding=encoding):
        line=line.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
        filter_emails.append(line)

def login():
    f=open('./logindata.json','r',encoding='utf8')
    data=json.load(f)
    session=requests.session()
    session.post('http://members.brokerbin.com/',data=data,headers=headers,timeout=30)
    return session

def get_form(session):
    try:
        select=input("输入 1 采集 CISCO,2 采集 hp:")
    except:
        select=1
    if select=='2':
        platform='hp'
    else:
        platform='CISCO'
    html=session.get('http://members.brokerbin.com/main.php?platform={}&refresh=%27.%24submit.%27&loc=top100&view=1'.format(platform),headers=headers,timeout=30).text
    table=BeautifulSoup(html,'html.parser').find('table',{'class':'rowHighlight'}).find_all('tr',{'class':'pref_vendor'})
    result=[]
    for item in table:
        try:
            url='http://members.brokerbin.com/'+item.find('a').get('href')
            result.append(url)
        except:
            continue
    return result

def get_person(session,url):
    html=session.get(url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'html.parser').find('table',{'class':'nowrap'}).find_all('tr')
    exsits=[]
    result=[]
    for item in table:
        try:
            tds=item.find_all('td')
            if 'Hrs' not in tds[1].get_text():
                continue

            #忽略掉电话号码86和+86开头的
            phone_num=tds[5].get_text().replace('\r','').replace('\n','').replace('\t','').replace(' ','').replace('\xa0','')
            if phone_num.startswith('86') or phone_num.startswith('+86'):
                continue

            product=tds[2].get_text().replace('\t','').replace(' ','').replace('\xa0','')
            person_name=item.find('a').get_text()
            person_url=re.findall("newWindow\('(.*?)',\d",item.find('a').get('onclick'))[0]

            #去重
            if product+person_url in exsits:
                continue
            exsits.append(product+person_url)

            result.append({'product_name':product,'person_name':person_name,'person_url':person_url})
        except:
            continue
    return result

def get_email(session,url):
    html=session.get('http://members.brokerbin.com/'+url,headers=headers,timeout=30).text
    email=re.findall('"mailto:(.*?)"',html)[0]
    return email

def get_price(product_name):
    html=requests.get('http://telstraight-com.3dcartstores.com/search_quick.asp?q='+product_name,headers=headers,timeout=30).text
    data=json.loads(html)[0]['results']
    for item in data:
        if item[1]==product_name:
            return item
    return data[0]

def write_to_email_txt(item):
    text=email_template.format(name=item['person_name'],product_name=item['product_name']
        ,price=item['product'][3],product_url='http://telstraight-com.3dcartstores.com/'+item['product'][0])
    date=time.strftime('%Y%m%d')
    f=open(date+'.txt','a',encoding='utf-8')
    f.write('qoute for %s\r\n'%(item['product_name'])+'***'*4+'\r\n'+item['email']+'\r\n'+'***'*4+'\r\n'+text+'\r\n'+'---'*8+'\r\n\r\n')
    f.close()

def main():
    session=login()
    urls=get_form(session)
    load_filter()
    global filter_emails
    persons=[]
    for url in urls:
        result=get_person(session,url)
        persons+=result
        print(url,'ok')
    result=[]
    price={}
    count=0
    exists=[]
    for person in persons:
        try:
            email=get_email(session,person['person_url'])
        except:
            continue
        #按邮箱加产品名去重
        person['email']=email
        if person['email']+person['product_name'] in exists:
            continue
        exists.append(person['email']+person['product_name'])


        #过滤邮箱
        if email in filter_emails:
            continue
        if email.split('@')[-1] in filter_emails:
            continue

        line=[]
        try:
            product_price=price[person['product_name']]
            person['product']=product_price
            write_to_email_txt(person)
            count+=1
            print(count,'ok')
            continue
        except:
            pass
        try:
            product_price=get_price(person['product_name'])
        except:
            print(person['product_name'],'get price failed')
            failed=open('failed','a',encoding='utf-8')
            failed.write(str(person)+'\r\n')
            failed.close()
            continue
        count+=1
        print(count,'ok')
        price[person['product_name']]=product_price
        person['product']=product_price
        write_to_email_txt(person)

main()
print("OK")
time.sleep(60)
