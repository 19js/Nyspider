import requests
from bs4 import BeautifulSoup
import time
import re
import openpyxl

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}

def get_names():
    page=1
    while page<21:
        html=requests.get('http://www.18ladys.com/cyzy/index.asp?page='+str(page),headers=headers).text.encode('iso-8859-1').decode('gbk')
        table=BeautifulSoup(html,'lxml').find('div',{'class':'tb1'}).find_all('a')
        f=open('names.txt','a')
        for item in table:
            try:
                name=item.get_text()
                url='http://www.18ladys.com/cyzy/'+item.get('href')
                f.write(name+'|'+url+'\n')
            except:
                continue
        f.close()
        print(page)
        page+=1

def get_infor(name,url):
    html=requests.get(url,headers=headers).text.encode('iso-8859-1').decode('gbk','ignore')
    text=BeautifulSoup(html,'lxml').find('dd',{'class':'f14 jl4'}).find('p').get_text().replace('【','||【').replace('\r','').replace('\n','')
    text=text.split('||')
    result={'name':name}
    for item in text:
        try:
            name_value=item.split('】')
            name=name_value[0].replace('【','')
            value=name_value[1]
            result[name]=value
        except:
            continue
    return result

def crawler():
    for line in open('names.txt','r'):
        line=line.replace('\n','')
        name=line.split('|')[0]
        url=line.split('|')[1]
        try:
            item=get_infor(name,url)
        except:
            failed=open('failed','a')
            failed.write(line+'\n')
            failed.close()
        f=open('result.txt','a')
        f.write(str(item)+'\n')
        f.close()
        print(line,'ok')

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    keys=['name','异名','别名','来源','植物形态','功用主治','用法与用量','炮制']
    sheet.append(keys)
    for line in open('result.txt','r'):
        item=eval(line)
        infor=[]
        for key in keys:
            try:
                infor.append(item[key])
            except:
                infor.append('')
        sheet.append(infor)
    excel.save('result.xlsx')

crawler()