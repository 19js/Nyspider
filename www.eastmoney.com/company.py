import requests
from bs4 import BeautifulSoup
import json
import time
import chardet
import urllib
import re
import openpyxl


headers = {
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}

def get_code(name):
    name=urllib.parse.quote(name.encode('gbk'))
    url='http://suggest.eastmoney.com/suggest/default.aspx?name=sData&input=%s&type='%name
    html=requests.get(url,headers=headers).text.replace(' ','')
    result=re.findall('varsData="(.*?)"',html)[0].split(';')[0].split(',')
    return result

def get_company_infor(code):
    url='http://f10.eastmoney.com/f10_v2/CompanySurvey.aspx?code='+code
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('table',id='Table0')
    ths=table.find_all('th')
    tds=table.find_all('td')
    data={}
    for i in range(len(ths)):
        key=ths[i].get_text()
        value=tds[i].get_text()
        data[key]=value
    result=[]
    keys=['董事长','电子信箱','公司网址']
    for key in keys:
        try:
            result.append(data[key])
        except:
            result.append('-')
    return result

def get_finance_analysis(code):
    url='http://f10.eastmoney.com/f10_v2/FinanceAnalysis.aspx?code='+code
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('table',id='AssetStatementTable').find_all('tr')
    data={}
    for item in table:
        try:
            key=item.find('th').get_text().replace('\xa0','')
            value=item.find('td').get_text().replace('\xa0','')
            data[key]=value
        except:
            continue
    result=[]
    keys=['总资产','流动资产']
    for key in keys:
        try:
            result.append(data[key])
        except:
            result.append('-')
    return result

def get_chardet(filename):
    data=open(filename,'rb').read()
    coding=chardet.detect(data)['encoding']
    if coding=='GB2312':
        coding='GBK'
    return coding

def load_company_names():
    encoding=get_chardet('data/companys.txt')
    names=[name.replace('\r','').replace('\n','') for name in open('data/companys.txt','r',encoding=encoding)]
    return names

def write_to_excel(result):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in result:
        sheet.append(line)
    timenow=time.strftime('%Y%m%d_%H%M%S')
    try:
        import os
        os.mkdir('result')
    except:
        pass
    excel.save('result/%s.xlsx'%(timenow))

def main():
    try:
        names=load_company_names()
    except:
        print("导入公司名称失败")
        return
    result=[]
    for name in names:
        code_text=get_code(name)
        if code_text==['']:
            result.append([name])
            continue
        if code_text[-2]=='1':
            code='sh'+code_text[1]
        elif code_text[-2]=='2':
            code='sz'+code_text[1]
        else:
            result.append([name])
            continue
        search_name=code_text[0]
        line=[name,search_name,code]
        try:
            infor=get_company_infor(code)
        except:
            infor=['-','-','-']
        try:
            finance=get_finance_analysis(code)
        except:
            finance=[]
        line+=infor+finance
        result.append(line)
        print(name,'ok')
        time.sleep(0.5)
    write_to_excel(result)
    print("完成")
    
main()