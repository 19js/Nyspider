import requests
from bs4 import BeautifulSoup
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
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0"}

def search(key,need_urls):
    html=requests.get('http://cn.bing.com/search?q='+key.replace(' ','+')+'&go=Search&qs=bs&form=QBRE',headers=headers).text
    table=BeautifulSoup(html,'lxml').find('ol',id="b_results").find_all('li')
    result=[]
    name=key.lower()
    replace_keys=[',','(',')','...','[',']','?','!','/','*','&','^','%','$'
                ,'#','@','<','>','.',',','~','`',"'",'_','+','=','？','。','，','；','：','|']
    for punctuation in replace_keys:
        name=name.replace(punctuation,'').replace(' ','')
    names=name.split('-')
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
            str1+=strong.get_text()
        str1=str1.lower().replace(' ','')
        for punctuation in replace_keys:
            str1=str1.replace(punctuation,'').replace(' ','')
        status=True
        for key in names:
            if key.replace(' ','') not in str1:
                status=False
        if not status:
            continue
        for need in need_urls:
            if need in url:
                result.append(url)
                break
    return result[:3]

def get_chardet(filename):
    data=open(filename,'rb').read()
    coding=chardet.detect(data)
    return coding['encoding']

def load_needurls():
    encoding=get_chardet('urls.txt')
    if encoding=='GB2312':
        encoding='GBK'
    urls=[]
    for line in open('urls.txt','r',encoding=encoding):
        line=line.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
        urls.append(line)
    return urls

def main():
    try:
        os.mkdir('result')
    except:
        pass
    try:
        need_urls=load_needurls()
    except:
        print('导入urls.txt 失败')
        return
    for filename in os.listdir('data'):
        encoding=get_chardet('data/'+filename)
        if encoding=='GB2312':
            encoding='GBK'
        excel=openpyxl.Workbook(write_only=True)
        sheet=excel.create_sheet()
        for key in open('data/'+filename,'r',encoding=encoding):
            key=key.replace('\r','').replace('\n','').replace('\t','')
            line=[key]
            if key.replace(' ','').replace('\t','')=='':
                continue
            count=0
            while True:
                try:
                    result=search(key,need_urls)
                    if result==[] and count<10:
                        count+=1
                        continue
                    break
                except:
                    if count==10:
                        sheet.append(line+['失败'])
                        result==False
                    count+=1
            if result==False:
                continue
            for item in result:
                line.append(item)
            sheet.append(line)
            time.sleep(0.5)
            try:
                print(key,'ok')
            except:
                pass
        excel.save('result/'+filename+'.xlsx')
    print("完成")

main()
time.sleep(60)
