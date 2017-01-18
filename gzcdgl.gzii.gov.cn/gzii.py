import requests
import json
import openpyxl
import time
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate'}

def get_stations():
    html=requests.get("http://gzcdgl.gzii.gov.cn/GZChargeSystem/querycdz.action",headers=headers,timeout=30).text
    data=json.loads(html)
    return data

def get_time():
    timenow=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    return timenow

def write_to_excel(filename):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    keys=['CDZNAME','OPNAME','TEL','ADDRESS','YYSJ','SYLX','ZL_KX','ZLCNT','JL_KX','JLCNT','PRICE','MAPX','MAPY']
    sheet.append(keys)
    for line in open(filename+'.txt','r',encoding='utf-8'):
        try:
            sheet.append(eval(line))
        except:
            continue
    excel.save('result/'+filename+'.xlsx')

def main():
    try:
        os.mkdir('result')
    except:
        pass
    result=get_stations()
    f=open('result.txt','a',encoding='utf-8')
    keys=['CDZNAME','OPNAME','TEL','ADDRESS','YYSJ','SYLX','ZL_KX','ZLCNT','JL_KX','JLCNT','PRICE','MAPX','MAPY']
    timenow=get_time()
    for item in result:
        line=[timenow]
        for key in keys:
            try:
                line.append(item[key])
            except:
                line.append('')
        f.write(str(line)+'\n')
    f.close()
    write_to_excel("result")
    print(get_time(),'ok')

try:
    sleeptime=input("输入间隔时间(分钟):")
    sleeptime=int(sleeptime)
except:
    sleeptime=15
while True:
    main()
    print("sleep")
    time.sleep(sleeptime*60)
