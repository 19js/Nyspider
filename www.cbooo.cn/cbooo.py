#coding:utf-8

import requests
import xlwt3
from bs4 import BeautifulSoup
import re

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_code():
    f=open('code.txt','w',encoding='utf-8')
    html=requests.get('http://www.cbooo.cn/movies').text
    table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'select01'}).find('select',id='selArea').find_all('option')
    for item in table:
        text=item.get_text()+'||'+item.get('value')
        f.write(text+'\n')
    f.close()

def get_url(code,page):
    results=[]
    html=requests.get('http://www.cbooo.cn/Mdata/getMdata_movie?area='+str(code)+'&type=0&year=2016&initial=%E5%85%A8%E9%83%A8&pIndex='+str(page),headers=headers).text
    data=eval(html)['pData']
    for item in data:
        text=item['MovieName']+'|| '+item['BoxOffice']+'||'+item['ID']
        results.append(text)
    return results


def main():
    f=open('urls.txt','a',encoding='utf-8')
    statue=True
    for line in open('code.txt','r').readlines():
        line=line.replace('\n','')
        code=line.split('||')[-1]
        page=1
        pre=[]
        '''
        if code!='80' and statue==True:
            continue
        statue=False
        '''
        while True:
            try:
                results=get_url(code, page)
            except:
                break
            if pre==results:
                break
            pre=results
            page+=1
            for item in results:
                f.write(line+'||'+item+'\n')
            print(code,'---',page)
    f.close()

def infor(text):
    html=requests.get('http://www.cbooo.cn/m/'+text.split('||')[-1],headers=headers,timeout=30).text
    soup=BeautifulSoup(html,'lxml')
    baseinfor=soup.find('div',attrs={'class':'ziliaofr'})
    baseinfor=str(baseinfor).replace('\r','').replace('\n','').replace(' ','')
    try:
        Type=re.findall('类型：(.*?)<',str(baseinfor))[0]
    except:
        Type='--'
    try:
        Date=re.findall('上映时间：(.*?)<',str(baseinfor))[0]
    except:
        Date='--'
    try:
        Zhishi=re.findall('制式：(.*?)<',str(baseinfor))[0]
    except:
        Zhishi='--'
    try:
        Area=re.findall('国家及地区：(.*?)<',str(baseinfor))[0]
    except:
        Area='--'
    text=text+'||'+Type+'||'+Date+'||'+Zhishi+'||'+Area
    table=soup.find('div',id='content').find('div',id='tabcont1').find('dl',attrs={'class':'dltext'}).find_all('dd')
    for item in table:
        infor=''
        for d in item.find_all('p'):
            infor+=d.find('a').get_text().replace('\r','').replace('\n','').replace(' ','')+'，'
        text+='||'+infor
    return text

def get_infor():
    f=open('data.txt','a',encoding='utf-8')
    statue=True
    for line in open('urls.txt','r').readlines():
        line=line.replace('\n','')
        if line!='美国||1||危情三日|| 2340||573698' and statue:
            continue
        statue=False
        print(line)
        try:
            line=infor(line)
        except:
            continue
        f.write(line+'\n')
    f.close()

def Excel():
    excel=xlwt3.Workbook()
    sheet=excel.add_sheet('sheet')
    count=0
    for line in open('data.txt','r').readlines():
        line=line.replace('，||','||').replace('||',' ||').replace('\n','')
        lists=line.split('||')
        num=0
        for i in lists:
            sheet.write(count,num,i)
            num+=1
        count+=1
    excel.save('data.xls')

main()
