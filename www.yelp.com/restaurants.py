import requests
from bs4 import BeautifulSoup
import time
import xlwt3

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}


def get_category():
    html=open('html.html','r').read()
    table=BeautifulSoup(html,'lxml').find('div',{'class':'all-category-browse-links'}).find_all('li')
    urls=[]
    for li in table:
        urls.append(li.find('a').get('href'))
    return urls

def get_restaurants(url):
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'search-results-content'}).find_all('li')
    result=[]
    if 'Try a different location.' in str(table):
        return []
    for item in table:
        media=item.find('div',{'class':'media-story'})
        try:
            title=media.find('a',{'class':'biz-name js-analytics-click'}).get_text()
        except:
            title='--'
        try:
            url=media.find('a',{'class':'biz-name js-analytics-click'}).get('href')
        except:
            url='--'
        try:
            star=media.find('div',{'class':'rating-large'}).find('i').get('title')
        except:
            star='--'
        try:
            reviews=media.find('span',{'class':'review-count rating-qualifier'}).get_text()
        except:
            reviews='--'
        try:
            category=media.find('div',{'class':'price-category'}).find('span',{'class':'category-str-list'}).get_text()
        except:
            category='--'
        try:
            address=item.find('address').get_text()
        except:
            address='--'
        try:
            phone=item.find('span',{'class':'biz-phone'}).get_text()
        except:
            phone='--'
        result.append(title+'||'+url+'||'+star+'||'+reviews+'||'+category+'||'+address+'||'+phone)
    return result

def main():
    urls=get_category()
    f=open('result.txt','a')
    for url in urls:
        start=0
        print(url)
        while True:
            pageurl='http://www.yelp.com'+url+'&start='+str(start)
            try:
                result=get_restaurants(pageurl)
            except:
                break
            if result==[]:
                break
            for item in result:
                item=item.replace('\n','')
                f.write(item+'\n')
            start+=10
            print(start)
            time.sleep(3)
    f.close()

def write_to_excel():
    excel=xlwt3.Workbook()
    sheet=excel.add_sheet('sheet')
    count=0
    for line in open('result.txt','r'):
        line=line.replace('\n','')
        if '/biz/' not in line:
            continue
        list=line.split('||')
        num=0
        for i in list:
            sheet.write(count,num,i)
            num+=1
        count+=1
    excel.save('result.xls')

write_to_excel()
