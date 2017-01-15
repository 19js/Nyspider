import requests
import json
import threading
import time
from bs4 import BeautifulSoup

lock=threading.Lock()
lock_failed=threading.Lock()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def table_page(page):
    html=requests.get('http://ffip.cnca.cn/ffip/certquery/queryCert.action?startIndex=%s&sizePerPage=10&status=01'%(page*10),headers=headers).text
    data=json.loads(html)['model']['data']
    result=[]
    keys=['certnum','oentname','productdescription','avdate','statusShow','userOpDate','userUpDate']
    for item in data:
        line=[]
        for key in keys:
            try:
                line.append(item[key])
            except:
                if key=='statusShow':
                    line.append('有效')
                else:
                    line.append('')
        result.append(line)
    return result

class Query(threading.Thread):
    def __init__(self,line):
        super(Query,self).__init__()
        self.line=line
        self.num=line[0]

    def run(self):
        try:
            result=parser(self.num)
            with lock:
                f=open('certserch.txt','a',encoding='utf-8')
                f.write(str(self.line+result)+'\n')
                f.close()
        except:
            with lock_failed:
                failed_f=open('failed.txt','a',encoding='utf-8')
                failed_f.write(str(self.line)+'\n')
                failed_f.close()

def parser(certnum):
    html=requests.get('http://ffip.cnca.cn/ffip/ffdp/publicQueryCertAct.action?certNum=%s'%certnum,headers=headers,timeout=30).text
    tables=BeautifulSoup(html,'html.parser').find_all('table',{'class':'huitd'})
    data={}
    keys=['发证机构', '证书编号','企业信息码','产品编号', '行政区划', '获证企业名称', '证书截止日期', '证书状态']
    for item in tables[0].find_all('tr'):
        try:
            tds=item.find_all('td')
            name=tds[0].get_text().replace('\r','').replace('\n','').replace(' ','').replace('\xa0','')
            value=tds[1].get_text().replace('\r','').replace('\n','').replace(' ','').replace('\xa0','').replace('\t','')
            data[name]=value
        except:
            continue
    result=[]
    for key in keys:
        try:
            result.append(data[key])
        except:
            result.append('')
    try:
        result.append(str(tables[1]))
    except:
        pass
    return result

def main():
    page=0
    while True:
        table=table_page(page)
        if table==[]:
            break
        for item in table:
            work=Query(item)
            work.setDaemon(True)
            work.start()
        time.sleep(0.5)
        print(page,'ok')
        page+=1

main()
