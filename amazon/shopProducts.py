#coding:utf-8

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def get_products(browser):
    urls=[]
    while True:
        results=shopParser(browser.page_source)
        urls+=results
        try:
            browser.find_element_by_id('pagnNextLink').click()
        except:
            break
    return urls

def shopParser(html):
    table=BeautifulSoup(html,'lxml').find('div',id='atfResults').find_all('li')
    results=[]
    for item in table:
        url=item.find('a').get('href')
        results.append(url)
    return results

def inforParser(html):
    infor={}
    soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'a-container'})
    try：
        infor['title']=soup.find('DIV',id='title_feature_div ').find('span',id='productTitle').get_text()
    except:
        infor['title']='--'
    try:
        infor['commentsNumber']=soup.find('div',id='averageCustomerReviews_feature_div').find('span',attrs={'class':'a-declarative'}).get_text().replace('\r','').replace('\n','')
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





def main():
    browser=webdriver.Firefox()
    browser.implicitly_wait(5)
    input('在浏览器中输入店铺链接，待加载完成后确认')
    results=get_products(browser)
    print(results)

main()
