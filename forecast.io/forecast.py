#coding:utf-8

from selenium import webdriver
import xlwt
import time
from bs4 import BeautifulSoup

def Main():
    browser=webdriver.Firefox()
    browser.get('http://forecast.io/#/f/35.0000,105.0000/1262404800')
    excel=xlwt.Workbook()
    sheet=excel.add_sheet('sheet')
    count=0
    starttime=1262318400
    endtime=time.time()
    while starttime<endtime:
        browser.get('http://forecast.io/#/f/35.0000,105.0000/1262404800')
        time.sleep(2)
        result=parser(browser.page_source)
        sheet.write(count,0,timetostr(starttime))
        num=1
        for i in result:
            sheet.write(count,num,i)
            num+=1
        starttime+=86400
        count+=1
        time.sleep(2)
        excel.save('result1.xls')

def timetostr(timestr):
    date=time.localtime(timestr)
    return time.strftime("%Y-%m-%d %H:%M:%S", date)


def parser(html):
    table=BeautifulSoup(html,'html.parser').find('div',attrs={'class':'slider_details'})
    result=[]
    result.append(table.find('div',attrs={'class':'summary'}).get_text())
    for tr in table.find('tr',attrs={'class':'val'}).find_all('td'):
        result.append(tr.get_text())
    return result

Main()
