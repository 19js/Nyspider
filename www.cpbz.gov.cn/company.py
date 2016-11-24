import requests
from bs4 import BeautifulSoup
import time
import json
import random

def get_headers():
    headers = {
        "X-Forwarded-For":'%s.%s.%s.%s'%(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
        'Host':"www.cpbz.gov.cn",
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    return headers

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    'Host':'www.cpbz.gov.cn',
    'Referer':'http://www.cpbz.gov.cn/standardProduct/toAdvancedResult.do',
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def company_list():
    page=14550
    while True:
        data={
        'standardName':'',
        'enterpriseName':'',
        'standardCode':'',
        'standardStatus':'',
        'xzqh':'',
        'orgCode':'',
        'pageNum':page
        }
        try:
            html=requests.post('http://www.cpbz.gov.cn/standardProduct/anvancedQueryPaged.do',data=data,headers=get_headers(),timeout=30).text
        except:
            print(page,'failed')
            continue
        try:
            data=json.loads(html)['result']
        except:
            break
        if len(data)==0:
            break
        f=open('company_list.txt','a')
        for item in data:
            f.write(str(item)+'\n')
        f.close()
        print(page,'ok')
        page+=1

def companyinfor(url):
    html=requests.get(url,headers=get_headers(),timeout=30).text
    tables=BeautifulSoup(html,'lxml').find_all('table',{'class':'tab-color-5'})
    result={}
    for table in tables:
        if '企业基本信息' in str(table):
            baseinfor={}
            for tr in table.find_all('tr'):
                try:
                    right=tr.find_all('td',{'align':'right'})
                    left=tr.find_all('td',{'align':'left'})
                    for index in range(len(right)):
                        try:
                            key=right[index].get_text().replace('\xa0','').replace('\r','').replace('\n','').replace('\t','').replace('\xa0','')
                            value=left[index].get_text().replace('\xa0','').replace('\r','').replace('\n','').replace('\t','').replace('\xa0','')
                            baseinfor[key]=value
                        except:
                            continue
                except:
                    continue
            result['企业基本信息']=baseinfor
        elif '标准信息' in str(table):
            infor={}
            for tr in table.find_all('tr'):
                try:
                    right=tr.find_all('td',{'align':'right'})
                    left=tr.find_all('td',{'align':'left'})
                    for index in range(len(right)):
                        try:
                            key=right[index].get_text().replace('\r','').replace('\n','').replace('\t','').replace('\xa0','')
                            value=left[index].get_text().replace('\r','').replace('\n','').replace('\t','').replace('\xa0','')
                            infor[key]=value
                        except:
                            continue
                except:
                    continue
            try:
                url='http://www.cpbz.gov.cn/'+table.find('a').get('href')
            except:
                url=''
            infor['url']=url
            result['标准信息']=infor
        elif '执行该标准的产品信息' in str(table):
            products=[]
            for tr in table.find_all('tr'):
                try:
                    line=[]
                    tds=tr.find_all('td')
                    if len(tds)==0 or '产品名称' in str(tr) or '执行该标准的产品信息' in str(tr):
                        continue
                    for td in tds:
                        try:
                            line.append(td.get_text().replace('\r','').replace('\n','').replace('\t','').replace('\xa0',''))
                        except:
                            line.append('')
                    products.append(line)
                except:
                    continue
            result['产品信息']=products
        elif '技术指标' in str(table):
            numbers=[]
            for tr in table.find_all('tr'):
                try:
                    line=[]
                    tds=tr.find_all('td')
                    if len(tds)==0 or '指标名称' in str(tr):
                        continue
                    for td in tds:
                        try:
                            text=td.get_text().replace('\r','').replace('\n','').replace('\t','').replace('\xa0','')
                            try:
                                url=td.find('a').get('href')
                            except:
                                url=''
                            if url!='':
                                text+="(%s)"%url
                            line.append(text)
                        except:
                            line.append('')
                    numbers.append(line)
                except:
                    continue
            result['技术指标']=numbers
    return result

def main():
    for line in open('./company_list.txt','r'):
        item=eval(line)
        url='http://www.cpbz.gov.cn/standardProduct/showDetail/%s/%s.do'%(item['orgCode'],item['standardId'])
        try:
            result=companyinfor(url)
        except:
            failed=open('failed.txt','a')
            failed.write(line)
            f.close()
            continue
        for key in item:
            result[key]=item[key]
        f=open('result.txt','a')
        f.write(str(result)+'\n')
        f.close()
        print(item['orgCode'],'ok')

company_list()
