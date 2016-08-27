import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import re
import os

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def baseinfor(url):
    html=requests.get(url,headers=headers,timeout=30).text
    soup=BeautifulSoup(html,'lxml').find('div',id='doc')
    title=soup.find('h1').get_text()
    author=soup.find('div',{'class':'atl-info'}).find('a').get_text()
    author_url=soup.find('div',{'class':'atl-info'}).find('a').get('href')
    comments=parser(html)
    result={}
    result['title']=title
    result['author']=author
    result['author_url']=author_url
    result['url']=url
    result['comments']=comments
    return result

def parser(html):
    try:
        soup=BeautifulSoup(html,'lxml').find('div',{'class':'atl-main'}).find_all('div',{'class':'atl-item'})
        comments=[]
        for item in soup:
            try:
                author=item.find('div',{'class':'atl-info'}).find('a').get_text()
                text=item.find('div',{'class':'bbs-content'}).get_text().replace('\r','').replace('\n','').replace('\t','')
            except:
                continue
            comments.append([author,text])
            try:
                ul=item.find('div',{'class':'ir-list'}).find_all('li')
            except:
                continue
            for li in ul:
                try:
                    author=li.get('_username')
                    try:
                        text=li.find('span',{'class':'ir-content'}).get_text().replace('\r','').replace('\n','').replace('\t','')
                    except:
                        text=li.get_text().replace('\r','').replace('\n','').replace('\t','')
                    comments.append([author,text])
                except:
                    continue
        return comments
    except:
        return []

def main():
    while True:
        try:
            url=input("输入帖子链接:")
        except:
            print('Failed!')
        try:
            infor=baseinfor(url)
            break
        except:
            print("请检查链接是否正确，或者不支持抓起该网页!")
    page=2
    comments=infor['comments']
    while True:
        try:
            url=re.sub('-\d+.s','-%s.s'%page,url)
            html=requests.get(url,headers=headers).text
            result=parser(html)
            if result==comments or result==[]:
                break
            comments=result
            infor['comments']+=result
            print(page,'ok')
            page+=1
        except:
            break
        time.sleep(2)
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    sheet.append([infor['title'],infor['url'],infor['author'],infor['author_url']])
    for comment in infor['comments']:
        sheet.append(comment)
    filename=time.strftime('%Y%m%d_%H%M%S',time.localtime())+'.xlsx'
    try:
        os.mkdir('result')
    except:
        pass
    excel.save('result/'+filename)
    print('OK')
    time.sleep(50)

main()
