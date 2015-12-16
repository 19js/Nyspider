#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re
import xlwt3
import threading

def get_id():
    users=[]
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
    urls=['http://invest.ppdai.com/loan/list_safe_s0_p','http://invest.ppdai.com/loan/list_payfor_s0_p','http://invest.ppdai.com/loan/list_riskmiddle_s0_p','http://invest.ppdai.com/loan/list_riskhigh_s0_p']
    bd_url='http://invest.ppdai.com/loan/list_bd'
    url_re='(http://www.ppdai.com/user/.*?)"'
    for url in urls:
        page=1
        while True:
            try:
                html=requests.get(url+str(page),headers=headers,timeout=50).text
            except:
                continue
            try:
                table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'outerBorrowList'}).find_all('ol',attrs={'class':'clearfix'})
            except:
                page+=1
                continue
            if len(table)==1 or table==[]:
                break
            urls=re.findall(re.compile(url_re),str(table).replace('\n','').replace(' ',''))
            users+=urls
            print(page)
            page+=1
        users=list(set(users))
    try:
        html=requests.get(bd_url,headers=headers,timeout=50).text
    except:
        return users
    table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'outerBorrowList'}).find_all('ol',attrs={'class':'clearfix'})
    urls=re.findall(re.compile(url_re),str(table).replace('\n','').replace(' ',''))
    users+=urls
    users=list(set(users))
    return users

class Get_infor(threading.Thread):
    def __init__(self,url):
        super(Get_infor,self).__init__()
        self.url=url
    def run(self):
        headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'}
        try:
            html=requests.get(self.url,headers=headers,timeout=50).text.encode('ISO-8859-1').decode('utf-8','ignore')
        except:
            self.lists=[]
            return
        try:
            soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'user_homepage_nav clearfix'})
            left=soup.find('div',attrs={'class':'my-f-left left_user_nav  fl'}).find('ul').find_all('li')
            userinfor=''
            self.lists=[]
            for item in left[1].find_all('p'):
                userinfor+=item.get_text().replace(' ','').replace('\r\n','').replace('\n','')+'|'
            for item in left[2].find_all('p'):
                userinfor+=item.get_text().replace(' ','').replace('\r\n','').replace('\n','')+'|'
            right=soup.find('div',id='memberinfocontent').find('div',id='div1').find_all('li')
            for item in right:
                text=biao_deal(item)
                self.lists.append(userinfor+text)
        except:
            self.lists=[]
            return

def biao_deal(item):
    soup=item.find('div',attrs={'class':'borrow_list'}).find('table').find_all('td')
    text=''
    for td in soup:
        text+=td.get_text().replace(' ','').replace('\r\n','').replace('\n','')+'|'
    return text[:-1]

def main():
    try:
        file_id=open('ids.txt','r')
        ids=[]
        for line in file_id.readlines():
            ids.append(line.replace('\n',''))
    except:
        ids=[]
    #ids+=get_id()
    ids=list(set(ids))
    file_id=open('ids.txt','w')
    for id in ids:
        file_id.write(id+'\n')
    file_id.close()
    data_f=open('data.txt','w')
    urls=[]
    for url in ids:
        urls.append(url)
        if len(urls)<1:
            continue
        get(data_f,urls)
        urls=[]
    get(data_f,urls)
    data_f.close()
    excel()

def get(data_f,urls):
    threadings=[]
    for url in urls:
        work=Get_infor(url)
        threadings.append(work)
    for work in threadings:
        work.start()
    for work in threadings:
        work.join()
    for work in threadings:
        for text in work.lists:
            data_f.write(text+'\n')
    print('ok')

def excel():
    file_d=open('data.txt','r')
    excel_f=xlwt3.Workbook()
    sheet=excel_f.add_sheet('sheet')
    count=0
    for line in file_d.readlines():
        lists=line.replace('\n','').split('|')
        num=0
        for item in lists:
            try:
                text=item.split('：')[1]
            except:
                text=item
            sheet.write(count,num,text)
            num+=1
        count+=1
    excel.save('data.xls')

main()
