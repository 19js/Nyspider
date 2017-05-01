import requests
from bs4 import BeautifulSoup
import time
import openpyxl
import re

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Host':'www.cbrc.gov.cn',
        'Accept-Encoding': 'gzip, deflate'}

def get_doc_urls():
    need_type=['http://www.cbrc.gov.cn/chinese/home/docViewPage/110002','http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//1.html','http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//2.html']
    for baseurl in need_type:
        page=1
        pre=[]
        while True:
            try:
                if '110002' in baseurl:
                    html=requests.get(baseurl+'&current='+str(page), headers=headers,timeout=30).text
                else:
                    html=requests.get(baseurl+'?current='+str(page), headers=headers,timeout=30).text
            except Exception as e:
                print(e)
                continue
            table=BeautifulSoup(html,'lxml').find('table',id='testUI').find_all('a')
            if table==pre:
                break
            pre=table
            f=open('urls.txt','a')
            for item in table:
                title=item.get('title')
                url=item.get('href')
                f.write(str([baseurl,title,url])+'\n')
            f.close()
            print(baseurl,page,'OK')
            page+=1

def get_doc_info(url):
    html=requests.get('http://www.cbrc.gov.cn'+url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('table',{'class':'MsoNormalTable'}).find_all('tr')
    result=[]
    for item in table:
        tds=item.find_all('td')
        try:
            result.append(tds[-1].get_text().replace('\n','').replace('\xa0',''))
        except:
            result.append('-')
    try:
        doc_from=re.findall('文章来源:(.*?)文章类型',BeautifulSoup(html,'lxml').get_text().replace('\r','').replace('\n','').replace('\t','').replace(' ',''))[0]
    except:
        doc_from='-'
    return [doc_from]+result

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in open('./result.txt','r'):
        line=eval(line)
        sheet.append(line)
    excel.save('result.xlsx')

def penalty():
    for line in open('./urls.txt','r'):
        line=eval(line)
        try:
            info=get_doc_info(line[-1])
        except Exception as e:
            print(e,line)
            failed=open('failed.txt','a')
            failed.write(str(line)+'\n')
            failed.close()
            continue
        f=open('result.txt','a')
        f.write(str(line+info)+'\n')
        f.close()
        print(line,'OK')

write_to_excel()
#penalty()
