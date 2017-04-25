import time
import os
import re
import json
import datetime
import tushare
from tqdm import tqdm

def day_get(d):
    oneday = datetime.timedelta(days=1)
    day = d + oneday
    day = str(day).split(' ')[0].replace('-','.')
    return day

def get_volume(code,date):
    df=tushare.get_tick_data(code.replace('SZ','').replace('SH',''),date)
    line=re.findall('(09:25.*?盘)',str(df))[0]
    line=re.sub('\s+',' ',line).split(' ')
    return [code,date,line[3]]

def crawl(date_from):
    print('Date ',date_from)
    pbar = tqdm(total=3223)
    for line in open('./codes.txt','r',encoding='utf-8'):
        code=line.replace('\r','').replace('\n','').replace('\t','')
        try:
            pbar.update(1)
        except:
            pass
        try:
            result=get_volume(code,date_from.replace('.','-'))
        except:
            continue
        f=open('result/%s.txt'%date_from.replace('.','_'),'a',encoding='utf-8')
        f.write('\t'.join(result)+'\r\n')
        f.close()
    pbar.close()


def tushare_volume():
    try:
        os.mkdir('result')
    except:
        pass
    try:
        date=input("输入需采集的日期区间(如:2017.03.01-2017.03.31):")
        line=date.split('-')
        date_from=line[0]
        date_to=line[1]
    except Exception as e:
        print("输入时间格式不正确")
        return
    while True:
        current_date=datetime.datetime.strptime(date_from, "%Y.%m.%d")
        if current_date.weekday()!=5 and current_date.weekday()!=6:
            crawl(date_from)
        if date_from==date_to:
            break
        date_from=day_get(current_date)

while True:
    tushare_volume()
