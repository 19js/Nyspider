import requests
from bs4 import BeautifulSoup
import Levenshtein
import re
import openpyxl
import chardet
import os
import time

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    'Host':"cn.bing.com",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def search(key,limit):
    html=requests.get('http://cn.bing.com/search?q='+key,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('ol',id="b_results").find_all('li')
    result=[]
    name=key.lower()
    replace_keys=[',','(',')','...','[',']']
    for punctuation in replace_keys:
        name=name.replace(punctuation,'')
    for li in table:
        h2=li.find('h2')
        if h2==None:
            continue
        try:
            url=h2.find('a').get('href')
            if 'http' not in url:
                continue
        except:
            continue
        str1=''
        for strong in h2.find_all('strong'):
            str1+=strong.get_text()+' '
        num=Levenshtein.ratio(str1.lower(),name)
        if num>limit:
            result.append([num,url])
    result=sorted(result,key=lambda x:x[0],reverse=True)
    return result[:3]

def get_chardet(filename):
    data=open(filename,'rb').read()
    coding=chardet.detect(data)
    return coding['encoding']

def main():
    try:
        os.mkdir('result')
    except:
        pass
    try:
        num=float(input("输入相似度(0.6~0.75比较合适):"))
    except:
        num=0.6
    for filename in os.listdir('data'):
        encoding=get_chardet('data/'+filename)
        if encoding=='GB2312':
            encoding='GBK'
        excel=openpyxl.Workbook(write_only=True)
        sheet=excel.create_sheet()
        for key in open('data/'+filename,'r',encoding==encoding):
            key=key.replace('\r','').replace('\n','')
            line=[key]
            if key.replace(' ','').replace('\t','')=='':
                continue
            try:
                result=search(key,num)
            except:
                print('采集失败')
                sheet.append(line)
                continue
            for item in result:
                line.append(item[1])
            sheet.append(line)
            time.sleep(0.5)
            try:
                print(key,'ok')
            except:
                pass
        excel.save('result/'+filename+'.xlsx')
main()
