#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re
import xlwt3
import time

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
            table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'outerBorrowList'}).find_all('ol',attrs={'class':'clearfix'})
            if len(table)==1 or table==[]:
                break
            urls=re.findall(re.compile(url_re),str(table).replace('\n','').replace(' ',''))
            users+=urls
            print(page)
            page+=1
            time.sleep(0.4)
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

def get_infor(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
    try:
        html=requests.get(url,headers=headers,timeout=50).text.encode('ISO-8859-1').decode('utf-8','ignore')
    except:
        return []
    soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'user_homepage_nav clearfix'})
    left=soup.find('div',attrs={'class':'my-f-left left_user_nav  fl'}).find('ul').find_all('li')
    userinfor=''
    lists=[]
    for item in left[1].find_all('p'):
        userinfor+=item.get_text().replace(' ','').replace('\r\n','').replace('\n','')+'|'
    for item in left[2].find_all('p'):
        userinfor+=item.get_text().replace(' ','').replace('\r\n','').replace('\n','')+'|'
    right=soup.find('div',id='memberinfocontent').find('div',id='div1').find_all('li')
    lists=[]
    for item in right:
        text=biao_deal(item)
        lists.append(userinfor+text)
    return lists

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
    print('获取ID')
    #ids+=get_id()
    ids=list(set(ids))
    file_id=open('ids.txt','w',encoding='utf-8')
    for id in ids:
        file_id.write(id+'\n')
    file_id.close()
    data_f=open('data.txt','w',encoding='utf-8')
    excel_f=xlwt3.Workbook(encoding='utf-8')
    sheet=excel_f.add_sheet('sheet')
    count=0
    for url in ids:
        print(url)
        try:
            lists=get_infor(url)
            time.sleep(0.5)
        except:
            continue
        for text in lists:
            lists_t=text.split('|')
            num=0
            for item in lists_t:
                try:
                    te=item.split('：')[1]
                except:
                    te=item
                sheet.write(count,num,te)
                num+=1
            count+=1
            data_f.write(text+'\n')
        excel_f.save('data.xls')
    data_f.close()
main()
