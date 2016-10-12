import requests
from bs4 import BeautifulSoup
import openpyxl
import time

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_terms():
    html=open('html.html','r').read()
    table=BeautifulSoup(html).find_all('span',{'class':'y-l'})
    urls=[]
    f=open('terms.txt','w')
    for item in table:
        try:
            term=item.find('h4').get_text()
            publishers=item.find_all('p')
            for p in publishers:
                publisher=p.get_text()
                links=p.find_all('a')
                for a in links:
                    url=a.get('href')
                    f.write(term+'|'+publisher+'|'+a.get_text()+'|'+url+'\n')
        except:
            continue
    f.close()

def get_article_url(term_url):
    html=requests.get('http://yuwen.chazidian.com'+term_url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',id='mulu').find_all('div',{'class':'mldy'})
    result=[]
    num=1
    for item in table:
        title=item.find('a').get_text()
        url=item.find('a').get('href').replace('kewen','kewendetail')
        line=str(num)+'|'+title+'|'+url
        result.append(line)
        num+=1
    return result

def get_urls():
    for line in open('terms.txt','r'):
        line=line.replace('\n','')
        url=line.split('|')[-1]
        result=get_article_url(url)
        f=open('urls.txt','a')
        for item in result:
            f.write(line+'|'+item+'\n')
        f.close()
        print(line)
        time.sleep(1)

def get_article_content(url):
    html=requests.get(url,headers=headers).text
    content=BeautifulSoup(html,'lxml').find('div',id='print_content').get_text()
    return content

def main():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in open('urls.txt','r'):
        line=line.replace('\n','')
        infor_list=line.split('|')
        url=infor_list[-1]
        try:
            content=get_article_content(url)
        except:
            failed=open('failed.txt','a')
            failed.write(line+'\n')
            failed.close()
            continue
        sheet.append(infor_list+[content])
        print(line)
        time.sleep(0.5)
    excel.save('result.xlsx')
main()
