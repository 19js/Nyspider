import requests
from bs4 import BeautifulSoup
import openpyxl
import re


headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def geturls():
    f=open('urls.txt','a')
    page=1
    while True:
        html=requests.get('http://xxgk.jl.gov.cn/zwdtSjgl/Directory/depListDir1.jsp?department_name=%CB%F9%D3%D0&pageNo='+str(page),headers=headers).text
        table=BeautifulSoup(html,'lxml').find_all('div',style='display:none;')
        for item in table:
            try:
                pid=item.get('id').replace('_text','')
                item=str(item).replace('</strong>','</strong><a>').replace('<br/>','</a>')
                items=BeautifulSoup(item,'lxml').find_all('a')
                title=items[2].get_text()
                date=items[3].get_text()
                line=title+'|| '+date+' ||'+pid
                f.write(line.replace('\r','').replace('\n','')+'\n')
            except:
                continue
        print(page,'ok')
        page+=1
        if page==937:
            break
    f.close()

def getinfor(pid):
    html=requests.get('http://xxgk.jl.gov.cn/zwdtSjgl/Directory/showDir.jsp?keyid='+pid,headers=headers,timeout=30).text
    tables=BeautifulSoup(html,'lxml').find_all('table',width=700)
    text=tables[0].get_text().replace('\r','').replace('\n','')
    try:
        location=re.findall('发布机构：(.*?)生成日期',text)[0]
    except:
        location='--'
    text=tables[1].get_text().replace('\r','').replace('\n','')
    return location+'||'+text

def main():
    f=open('result.txt','a')
    for line in open('urls.txt','r'):
        line=line.replace('\n','')
        try:
            result=getinfor(line.split('||')[-1].replace(' ',''))
        except:
            failed=open('failed','a')
            failed.write(line+'\n')
            failed.close()
            continue
        f.write(line+'||'+result+'\n')
        print(line)
    f.close()

main()
