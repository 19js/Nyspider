#coding:utf-8

import requests
from bs4 import BeautifulSoup
import xlwt3
import re


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_url(page):
    html=requests.get('http://job.qiaosiwang.com/zhiwei.html?Colname=0&KeyWord=&PageNo=%s&s_hangye=0&s_gangwei=0&s_xueli=&s_didian=&s_xinzhi=&s_date=&s_qiyexingzhi=&s_daiyu=&key=0'%page,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',id='hover_bg').find_all('div',attrs={'class':'item'})
    urls=[]
    for item in table:
        url=item.find('a').get('href')
        urls.append(url)
    return urls


def get_infor(url):
    html=requests.get(url,headers=headers).text
    soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'left'})
    text=soup.get_text().replace('\r',' ').replace('\n',' ')
    re_lists=['公司名称：(.*?) ','职位类别：(.*?) ','工作地点：(.*?) ','工作经验：(.*?) ','月薪：(.*?) ','联系地址： (.*?) ','联系人： (.*?) ','联系电话： (.*?) ']
    results=[]
    for rel in re_lists:
        items=re.findall(rel,text)
        try:
            results.append(items[0].replace('\xa0\xa0\xa0\xa0查看附近租房信息', '').replace('职位描述',''))
        except:
            results.append('--')
    des=soup.find('div',attrs={'class':'mo_3'}).get_text().replace('\r','').replace('\n','')
    results.append(des)
    return results

def main():
    pagefrom=int(input('起始页：'))
    pageto=int(input('终止页：'))
    excel=xlwt3.Workbook()
    sheet=excel.add_sheet('sheet')
    count=0
    while pagefrom<=pageto:
        urls=get_url(pagefrom)
        for url in urls:
            results=get_infor(url)
            num=0
            for item in results:
                sheet.write(count,num,item)
                num+=1
            count+=1
            print(count)
        excel.save('data.xls')
        pagefrom+=1
    excel.save('data.xls')

main()
