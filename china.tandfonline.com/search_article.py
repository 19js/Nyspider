import requests
from bs4 import BeautifulSoup
import openpyxl
import time

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_articles():
    page=0
    while True:
        html=requests.get('http://china.tandfonline.com/action/doSearch?AllField=urban+design&Ppub=%5B20151107+TO+20161107%5D&content=standard&countTerms=true&target=default&sortBy=&pageSize=50&subjectTitle=&startPage='+str(page),headers=headers).text
        table=BeautifulSoup(html,'lxml').find('ol',{'class':'search-results'}).find_all('li')
        f=open('titles.txt','a')
        for item in table:
            title=item.find('article').get('data-title')
            f.write(title+'\n')
        f.close()
        page+=1
        print('抓取第',page,'页')
        #time.sleep(1)
        if page==267:
            break

def word_cut():
    text=open('./titles.txt','r').read()
    text=text.replace(':',' ').replace("?",' ').replace('.','').replace(')',' ').replace('(','').replace('+','').replace('“','').replace('”','').replace('\n','')
    words=text.split(' ')
    result={}
    for word in words:
        word=word.lower()
        try:
            result[word]+=1
        except:
            result[word]=1

    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for key in result:
        sheet.append([key,result[key]])
    excel.save('result.xlsx')

get_articles()
