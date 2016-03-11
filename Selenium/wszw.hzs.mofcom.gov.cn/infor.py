#coding:utf-8

from selenium import webdriver
from bs4 import BeautifulSoup

def infor():
    f=open('data_new.txt','a',encoding='utf-8')
    browser=webdriver.Firefox()
    browser.get('http://wszw.hzs.mofcom.gov.cn/fecp/fem/corp/fem_cert_stat_view_list.jsp?manage=0&check_dte_nian=1998&check_dte_nian2=2014&check_dte_yue=01&check_dte_yue2=12&CERT_NO=&COUNTRY_CN_NA=&CORP_NA_CN=&CHECK_DTE=1')
    '''
    results=parser(browser.page_source)
    for text in results:
        f.write(text+'\n')
    page=2
    '''
    input('271')
    while True:
        '''
        browser.find_element_by_name('Grid1toPageNo').clear()
        browser.find_element_by_name('Grid1toPageNo').send_keys(page)
        browser.find_element_by_class_name('buttonclass').click()
        time.sleep(1)
        '''
        try:
            browser.find_element_by_partial_link_text('后页').click()
        except:
            browser.back()
            continue
        results=parser(browser.page_source)
        for text in results:
            f.write(text+'\n')

def parser(html):
    table=BeautifulSoup(html,'lxml').find('table',attrs={'class':'listTableClass'}).find_all('tr',attrs={'class':'listTableBody'})
    results=[]
    for tr in table:
        text=''
        for td in tr.find_all('td'):
            text+=td.get_text().replace('\r','').replace('\n','')+'||'
        results.append(text)
    return results

infor()
