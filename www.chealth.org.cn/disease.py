import requests
from bs4 import BeautifulSoup
import time
import openpyxl
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_type():
    html=requests.get('http://www.chealth.org.cn/mon/departments_disease/article/departments_disease.html',headers=headers).text.encode('iso-8859-1').decode('utf-8')
    table=BeautifulSoup(html,'lxml').find('div',id='sc_3').find_all('li')
    f=open('type.txt','w',encoding='utf-8')
    items=re.findall("javascript:loadRelatedDiseases\('(.*?)','(.*?)'\);",str(table))
    for item in items:
        f.write(item[1]+'|http://www.chealth.org.cn/mon/departments_disease/article/%s_1.html\n'%item[0])
    f.close()

def disease_list():
    f=open('urls.txt','w',encoding='utf-8')
    for line in open('type.txt','r',encoding='utf-8'):
        line=line.replace('\n','').split('|')
        try:
            disease_type=line[0]
            pageurl=line[1]
        except:
            continue
        page=1
        while True:
            html=requests.get(pageurl.replace('_1','_%s'%page),headers=headers).text.encode('iso-8859-1').decode('utf-8','ignore')
            table=BeautifulSoup(html,'lxml').find_all('li')
            if len(table)==0:
                break
            for li in table:
                try:
                    name=li.find('a').get_text()
                    url=li.find('a').get('href')
                    f.write(disease_type+'|'+name+'|'+url+'\n')
                except:
                    continue
            try:
                print(disease_type,page,'ok')
            except:
                pass
            page+=1
    f.close()

def disease_infor(name,disease_type,url):
    html=requests.get(url,headers=headers,timeout=30).text.encode('iso-8859-1').decode('utf-8','ignore')
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'overview'})
    titles=soup.find_all('h4')
    values=soup.find_all('p')
    data={'name':name,'type':disease_type}
    for index in range(len(titles)):
        key=titles[index].find('div').get_text()
        value=values[index].get_text()
        data[key]=value
    return data

def write_to_excel(result):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    keys=[ 'name', 'type', '概述', '病因', '症状','诊断','治疗', '预防', '并发症', '治愈性', '遗传性', '治疗综述']
    sheet.append(keys)
    for item in result:
        line=[]
        for key in keys:
            try:
                line.append(item[key])
            except:
                line.append('')
        sheet.append(line)
    excel.save('result.xlsx')

def main():
    result=[]
    disease_list()
    for line in open('urls.txt','r',encoding='utf-8'):
        line=line.replace('\n','')
        try:
            disease_type=line.split('|')[0]
            name=line.split('|')[1]
            url=line.split('|')[2]
        except:
            continue
        try:
            data=disease_infor(name,disease_type,url)
        except:
            failed=open('failed.txt','a',encoding='utf-8')
            failed.write(line+'\r\n')
            failed.close()
            continue
        result.append(data)
        try:
            print(name,'ok')
        except:
            pass
        if len(result)==10:
            break
    write_to_excel(result)

main()
