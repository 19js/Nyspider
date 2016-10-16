import requests
from bs4 import BeautifulSoup
import time
import os
import openpyxl
from proxy import *

headers = {
    'Host':"www.gamefaqs.com",
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_urls(pageurl):
    page=0
    result=[]
    while True:
        try:
            html=requests.get(pageurl+'?page='+str(page),headers=headers,proxies=get_proxies(),timeout=30).text
        except:
            switch_ip()
            continue
        try:
            table=BeautifulSoup(html,'lxml').find('table',{'class':'results'}).find_all('tr')
        except:
            switch_ip()
            continue
        for tr in table:
            try:
                name=tr.find('a').get_text()
                url='http://www.gamefaqs.com'+tr.find('a').get('href')
                result.append([name,url])
            except:
                continue
        page+=1
        print(pageurl,page,'ok')
        time.sleep(1)
        if page==5:
            break
    return result

def game_infor(gameurl):
    while True:
        try:
            session=requests.get(gameurl,headers=headers,proxies=get_proxies(),timeout=30)
        except:
            switch_ip()
            continue
        if str(session.status_code)=='401':
            switch_ip()
            continue
        else:
            html=session.text
            break
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'main_content'})
    gametype=''
    try:
        for li in soup.find('header').find('ol',{'class':'crumbs'}).find_all('li'):
            gametype+=li.get_text()+'>>'
    except:
        gametype=''
    try:
        des=soup.find('div',{'class':'desc'}).get_text()
    except:
        des=''
    try:
        imgurl=soup.find('div',{'class':'pod_gameinfo'}).find('img',{'class':'boxshot'}).get('src')
    except:
        imgurl=''
    try:
        box=soup.find('div',{'class':'pod_gameinfo'}).find('div',{'class':'body'}).find_all('li')
    except:
        box=[]
    developer=''
    publisher=''
    date=''
    for index in range(len(box)):
        li=box[index]
        if 'gamePlatform' in str(li):
            try:
                text=box[index+1].get_text().split('/')
            except:
                continue
            developer=text[0]
            publisher=text[-1]
        if 'Release:' in str(li):
            date=li.get_text().replace('Release:','')
    return [gametype,des,developer,publisher,date,imgurl]

def get_img(number,url):
    headers = {
        'Host':"img.gamefaqs.net",
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}
    url=url.replace('thumb.','front.')
    count=0
    while True:
        try:
            session=requests.get(url,headers=headers,timeout=30)
            if str(session.status_code)=='404':
                url=url.replace('front.','thumb.')
                continue
            content=session.content
            break
        except:
            count+=1
            if count==4:
                return False
    with open('images/%s.%s'%(number,url.split('.')[-1]),'wb') as f:
        f.write(content)
    return '%s.%s'%(number,url.split('.')[-1])

def write_to_excel(name,result):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in result:
        sheet.append(line)
    excel.save('%s.xlsx'%name)

def write_to_txt(result):
    f=open('result.txt','a')
    for line in result:
        f.write(str(line)+'\n')
    f.close()

def main():
    try:
        os.mkdir('images')
    except:
        pass
    url='http://www.gamefaqs.com/ps4/category/999-all'
    games=get_urls(url)
    result=[]
    imgnum=100000
    f=open('result.txt','a')
    for game in games:
        name=game[0]
        url=game[1]
        line=game_infor(url)
        imgurl=line[-1]
        if imgurl=='':
            result.append([name]+line+[''])
            f.write(str([name]+line+[''])+'\n')
            continue
        filename=get_img(imgnum,imgurl)
        if filename==False:
            result.append([name]+line+[''])
            f.write(str([name]+line+[''])+'\n')
        else:
            result.append([name]+line+[filename])
            f.write(str([name]+line+[filename])+'\n')
            imgnum+=1
        print(name,'ok')
        time.sleep(1)
    f.close()
    write_to_excel('ps4',result)

main()
