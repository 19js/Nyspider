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
    'condList':''
    }
    html=requests.post('http://sysjk.ivdc.org.cn:8081/cx/querylcsysp/queryLcsysp.do', data=data,headers=headers).text
    data=json.loads(html)['rows']
    result=[]
    keys=['sqdwlxr', 'byx', 'nlcsydd', 'xmmc', 'yxqjz', 'yxqx', 'pjh', 'szcpph', 'shr', 'zsdwmc', 'sqdwmc', 'szcpsl', 'shrq', 'yxqks', 'slh', 'itemid']
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
        self.name=line[3]

    def run(self):
        data={
        'start':0,
        'limit':40,
        'condList':str([{"itemname":"xsymc","itemfieldname":"xsymc","itemval":self.name,"itemtype":"String","condType":"val"}])
        }
        try:
            html=requests.post('http://sysjk.ivdc.org.cn:8081/cx/querygnxsyzc/queryGnxsyzc.do', data=data,headers=headers,timeout=30).text
            data=json.loads(html)['rows']
            keys=['yzdw', 'itemid', 'ggh', 'shrq', 'shr', 'zsh', 'bz', 'syz', 'gg', 'byx', 'xsymc', 'ggrq', 'lb']
            query_lines=[]
            for item in data:
                '''
                for key in item:
                    keys.append(key)
                print(keys)
                return
                '''
                query_line=[]
                for key in keys:
                    try:
                        query_line.append(item[key])
                    except:
                        query_line.append('')
                query_lines.append(query_line)
        except:
            query_lines=[]
        global lock
        with lock:
            f=open('data/7_lcsy.txt','a',encoding='utf-8')
            for query_line in query_lines:
                f.write(str(self.line+query_line)+'\n')
            if query_lines==[]:
                f.write(str(self.line)+'\n')
            f.close()

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
        time.sleep(1)
        print(page,'ok')
        page+=1

main()
