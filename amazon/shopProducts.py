#coding:utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
import re
import xlwt3
import time
from selenium.webdriver.support.ui import WebDriverWait

def get_products(browser):
    count=0
    urls=[]
    while True:
        try:
            results=shopParser(browser.page_source)
        except:
            try:
                time.sleep(4)
                browser.find_element_by_id('pagnNextLink').click()
            except:
                try:
                    browser.find_element_by_id('pagnNextString').click()
                except:
                    pass
            continue
        urls+=results
        time.sleep(3)
        try:
            browser.find_element_by_id('pagnNextLink').click()
        except:
            try:
                browser.find_element_by_id('pagnNextString').click()
            except:
                pass
            break
    urls=list(set(urls))
    return urls

def shopParser(html):
    table=BeautifulSoup(html,'lxml').find('div',id='atfResults').find_all('li')
    results=[]
    for item in table:
        try:
            url=item.find('a').get('href')
        except:
            continue
        results.append(url)
    return results

def inforParser(html):
    infor={}
    soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'a-container'})
    if soup==None:
        soup=BeautifulSoup(html,'lxml')
    try:
        title=soup.find('div',id='title_feature_div').get_text().replace('\r','').replace('\n','')
        infor['title']=title.replace('#energyEfficiencyTitleInformation { font-size: 19px !important;}','')
    except:
        infor['title']='--'
    try:
        infor['commentsNumber']=soup.find('div',id='averageCustomerReviews_feature_div').find('a',id='acrCustomerReviewLink').get_text().replace('\r','').replace('\n','')
    except:
        infor['commentsNumber']='--'
    try:
        table=soup.find('div',id='featurebullets_feature_div').find('ul',attrs={'class':'a-vertical a-spacing-none'}).find_all('li')
        text=''
        for li in table:
            text+=li.get_text()+'\n'
        infor['feature']=text
    except:
        infor['feature']='--'
    try:
        try:
            text=soup.find('li',id='SalesRank').get_text()
            try:
                style=soup.find('li',id='SalesRank').find('style').get_text()
            except:
                style=''
            text=text.replace(style,'')
        except:
            text=soup.find('tr',id='SalesRank').get_text()
            try:
                style=soup.find('tr',id='SalesRank').find('style').get_text()
            except:
                style=''
            text=text.replace(style,'')
        infor['Rank']=text.replace('\n','')
    except:
        infor['Rank']='--'
    try:
        infor['Des']=soup.find('div',id='descriptionAndDetails').find('div',id='productDescription').get_text()
    except:
        infor['Des']='--'
    try:
        text=soup.get_text().replace('\n','|').replace(' ','')
    except:
        text=BeautifulSoup(html,'lxml').get_text()
    asin_rel=['"ASIN":"(.*?)"','"asin":"(.*?)"','asin=(.*?);']
    date_re={'uk':'Datefirstavailable(.*?)\|','de':'ImAngebotvonAmazon.deseit(.*?)\|',
    'jp':'Amazon.co.jpでの取り扱い開始日(.*?)\|','com':'DatefirstavailableatAmazon.com(.*?)\|','fr':'DatedemiseenlignesurAmazon.fr(.*?)\|',
    'it':'DisponibilesuAmazon.itapartiredal(.*?)\|','es':'ProductoenAmazon.esdesde(.*?)\|'}
    try:
        for rel in asin_rel:
            try:
                asin=re.findall(rel,html.replace('\n','').replace(' ',''))[0]
                break
            except:
                continue
        infor['asin']=asin
    except:
        infor['asin']='--'
    try:
        for key in date_re:
            try:
                date=re.findall(date_re[key],text)[0]
                break
            except:
                continue
        infor['date']=date.replace(':','')
    except:
        infor['date']='--'
    return infor

def main():
    excel=xlwt3.Workbook()
    sheet=excel.add_sheet('sheet')
    count=0
    keys=['title','commentsNumber','asin','date','Rank','feature','Des']
    browser=webdriver.Firefox()
    browser.get('http://www.amazon.co.uk')
    input('在浏览器中输入店铺链接，待加载完成后确认')
    browser.implicitly_wait(10)
    results=get_products(browser)
    for url in results:
        browser.get(url)
        time.sleep(5)
        try:
            infor=inforParser(browser.page_source)
        except:
            continue
        num=0
        for key in keys:
            sheet.write(count,num,infor[key])
            num+=1
        print(count)
        count+=1
        excel.save('data.xls')

main()
