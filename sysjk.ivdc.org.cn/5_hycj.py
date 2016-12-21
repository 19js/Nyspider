import requests
import json
import threading
import time

lock=threading.Lock()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    'Host':'sysjk.ivdc.org.cn:8081',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def table_page(page):
    data={
    'start':page*20,
    'limit':20,
    'condList':'',
    'datatype':'all'
    }
    html=requests.post('http://sysjk.ivdc.org.cn:8081/cx/queryhyjdcjjg/queryhyjdcjjg.do', data=data,headers=headers).text
    data=json.loads(html)['rows']
    result=[]
    keys=['cpwh', 'jydw', 'spm', 'bcscqy', 'cjlb', 'rwly', 'yplb', 'itemid', 'jyjl', 'nd', 'bcydwmc','jd', 'bz', 'ph', 'cjhj', 'cpmc', 'yylb', 'shrq', 'byx', 'pjxpzlb', 'bhgxm', 'shr']
    for item in data:
        '''
        for key in item:
            keys.append(key)
        print(keys)
        return
        '''
        line=[]
        for key in keys:
            try:
                line.append(item[key])
            except:
                line.append('')
        result.append(line)
    return result

class Query(threading.Thread):
    def __init__(self,line):
        super(Query,self).__init__()
        self.line=line
        self.num=line[0]

    def run(self):
        data={
        'start':0,
        'limit':1,
        'condList':str([{"itemname":"regexp_replace(pzwh,'[^0-9]')","itemfieldname":"regexp_replace(pzwh,'[^0-9]')","itemval":self.num,"itemtype":"String","condType":"val","compareType":"equal"}])
        }
        try:
            html=requests.post('http://sysjk.ivdc.org.cn:8081/cx/querysycppzwh/querySycppzwhData.do', data=data,headers=headers,timeout=30).text
            data=json.loads(html)['rows']
            keys=['zt', 'zxbz', 'sxyy', 'yxq', 'qymc', 'slh', 'itemid', 'pzrq', 'bgqk', 'shr', 'spm', 'byx', 'pzwh', 'shrq', 'tym', 'gg']
            query_line=[]
            for item in data:
                for key in keys:
                    try:
                        query_line.append(item[key])
                    except:
                        query_line.append('')
        except:
            query_line=[]
        self.result=self.line+query_line
        global lock
        with lock:
            f=open('data/5_hycj.txt','a',encoding='utf-8')
            f.write(str(self.result)+'\n')
            f.close()

def main():
    page=1920
    while True:
        table=table_page(page)
        if table==[]:
            break
        for item in table:
            work=Query(item)
            work.setDaemon(True)
            work.start()
        time.sleep(2)
        print(page,'ok')
        page+=1

main()
