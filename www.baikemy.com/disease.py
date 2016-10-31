import requests
from bs4 import BeautifulSoup
import time
import openpyxl


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def disease_list():
    page=1
    f=open('urls.txt','w',encoding='utf-8')
    while True:
        try:
            html=requests.get('http://www.baikemy.com/disease/list/0/0?pageIndex='+str(page),headers=headers,timeout=30).text
        except:
            continue
        table=BeautifulSoup(html,'lxml').find('div',{'class':'ccjb_jbli'}).find_all('li')
        for li in table:
            try:
                name=li.find('a').get_text()
                url='http://www.baikemy.com/'+li.find('a').get('href').replace('view','detail')+'/1/'
                f.write(name+'|'+url+'\n')
            except:
                pass
        if len(table)==1:
            break
        print('page %s urls get'%page)
        page+=1
    f.close()

def disease_infor(name,url):
    html=requests.get(url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'lemma-main'}).find_all('div',{'class':'lemma-main-content'})
    result=[name]
    for item in table:
        try:
            key=item.find('span',{'class':'headline-content'}).get_text()
            value=item.find('div',{'class':'para'}).get_text()
            result.append(key+':\t   '+value)
        except:
            continue
    return result

def write_to_excel(result):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in result:
        try:
            sheet.append(line)
        except:
            pass
    excel.save('result.xlsx')

def main():
    disease_list()
    result=[]
    for line in open('urls.txt','r',encoding='utf-8'):
        line=line.replace('\n','')
        try:
            name=line.split('|')[0]
            url=line.split('|')[1]
        except:
            continue
        try:
            data=disease_infor(name,url)
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
    write_to_excel(result)
    print('完成')


main()
time.sleep(60)
