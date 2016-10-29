import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import re

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def login():
    session=requests.session()
    html=session.get('http://www.cofeed.com/palmoil/16101738241.html',headers=headers).text
    logincode=BeautifulSoup(html,'html.parser').find('input',{'name':'LoginCode'}).get('value')
    data={
    'Cofeed_Name':"lilieddove",
    'cofeed_PWD':"abcde12345",
    'remember':"1",
    'act':"LoginOk",
    'LoginCode':logincode
    }
    session.post('http://www.cofeed.com/WebUser/UserChckLogin.asp',data=data,headers=headers)
    return session

def get_urls(date_from,date_to):
    date_from=date_from.split('-')
    int_from=int(date_from[0])*100+int(date_from[1])
    date_to=date_to.split('-')
    int_to=int(date_to[0])*100+int(date_to[1])
    page=1
    result=[]
    while True:
        url='http://www.cofeed.com/search.asp?pagnum={}&keywords=%E6%B1%87%E6%80%BB%E8%A1%A8&catalogid=59'.format(page)
        html=requests.get(url,headers=headers).text
        table=BeautifulSoup(html,'html.parser').find('div',{'class':'channel_items'}).find_all('div',{'class':'channel_item'})
        if len(table)==0:
            break
        for item in table:
            title=item.find('a').get('title')
            try:
                date=re.findall('汇总表：(\d+)月(\d+)日国内各地棕榈油价格及库存统计',title)[0]
            except:
                continue
            int_date=int(date[0])*100+int(date[1])
            if int_date<int_from:
                return result
            if int_date>int_to:
                continue
            result.append([date,'http://www.cofeed.com'+item.find('a').get('href')])
        page+=1
    return result

def parser(url,session):
    html=session.get(url,headers=headers).text
    soup=BeautifulSoup(html,'html.parser').find('div',id='infocontent')
    result=[]
    for tr in soup.find('table',id='datatble').find_all('tr'):
        line=[]
        for td in tr.find_all('td'):
            try:
                line.append(td.get_text())
            except:
                line.append('')
        result.append(line)
    try:
        des=soup.find('p').get_text()
    except:
        des=''
    result.append([des])
    return result

def main():
    date_from=input("输入起始日期(如：9-10)：")
    date_to=input("输入结束日期(如：10-10)：")
    urls=get_urls(date_from,date_to)
    session=login()
    try:
        import os
        os.mkdir('result')
    except:
        pass
    for item in urls:
        result=parser(item[1],session)
        excel=openpyxl.Workbook(write_only=True)
        sheet=excel.create_sheet()
        for line in result:
            sheet.append(line)
        filename='result/%s月%s日国内各地棕榈油价格及库存统计.xlsx'%(item[0][0],item[0][1])
        excel.save(filename)
        print(filename,'ok')
main()
