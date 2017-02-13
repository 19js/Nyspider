import requests
from bs4 import BeautifulSoup
import time
import json
import random
import threading


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
    page=1
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
    tables=BeautifulSoup(html,'lxml').find('div',id='center-bar-center-2').find_all('table',{'class':'tab-color-5'})
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

class Infor(threading.Thread):
    def __init__(self,item):
        super(Infor,self).__init__()
        self.item=item
        self.url='http://www.cpbz.gov.cn/standardProduct/showDetail/%s/%s.do'%(item['orgCode'],item['standardId'])

    def run(self):
        self.status=True
        try:
            self.result=companyinfor(self.url)
            for key in self.item:
                self.result[key]=self.item[key]
            self.result['url']=self.url
        except:
            self.status=False

def get_lines():
    lines=[]
    for line in open('./company_list.txt','r'):
        lines.append(eval(line))
        if len(lines)==10:
            yield lines
            lines.clear()
    yield lines

def main():
    count=0
    for lines in get_lines():
        threadings=[]
        for line in lines:
            work=Infor(line)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()
        for work in threadings:
            work.join()
        f=open('result.txt','a')
        for work in threadings:
            if work.status==False:
                failed=open('failed.txt','a')
                failed.write(str(work.item)+'\n')
                failed.close()
                continue
            f.write(str(work.result)+'\n')
            count+=1
        print(count,'ok')
        f.close()
company_list()
main()
