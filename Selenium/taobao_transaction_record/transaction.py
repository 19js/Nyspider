#coding:utf-8

from selenium import webdriver
import time
import xlwt3
from bs4 import BeautifulSoup

def get_transaction(url):
    f=open('data.txt','a')
    driver=webdriver.Firefox()
    driver.get(url)
    time.sleep(3)
    driver.find_element_by_xpath('//li[@class="tb-last"]/a').click()
    time.sleep(3)
    items=html_parser(driver.page_source)
    for item in items:
        f.write(str(item)+'\n')
    while True:
        try:
            driver.find_element_by_xpath('//div[@class="tb-page-bottom"]/a[@class="J_TAjaxTrigger page-next"]').click()
            time.sleep(3)
        except:
            break
        items=html_parser(driver.page_source)
        for item in items:
            f.write(str(item)+'\n')
    f.close()
    driver.quit()

def html_parser(html):
    table=BeautifulSoup(html,'lxml').find('tbody',attrs={'class':'tb-list-body'}).find_all('tr')
    items=[]
    for tr in table:
        try:
            lists=tr.find_all('td')
            item={}
            item['buyer']=lists[0].find('span').get_text().replace('\r\n','').replace('\t','').replace('\n','').replace(' ','')
            try:
                item['grade']=lists[0].find('img').get('title')
            except:
                item['grade']=''
            item['price']=lists[1].get_text().replace('\r\n','').replace('\t','').replace('\n','').replace(' ','')
            item['count']=lists[2].get_text().replace('\r\n','').replace('\t','').replace('\n','').replace(' ','')
            item['date']=lists[3].get_text().replace('\r\n','').replace('\t','').replace('\n','')
            item['des']=lists[4].get_text().replace('\r\n','').replace('\t','').replace('\n','').replace(' ','')
            items.append(item)
        except:
            continue
    return items

if __name__=='__main__':
    url='https://item.taobao.com/item.htm?spm=a230r.1.14.17.Ujh8zA&id=44680207403&ns=1&abbucket=13#detail'
    get_transaction(url)
