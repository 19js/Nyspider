import requests
from bs4 import BeautifulSoup
import threading
import time
from selenium import webdriver


def parser_detail(html):
    table=BeautifulSoup(html,'html.parser').find('table',{'class':'Detail'}).find_all('tr')
    data={}
    keys=['CVCC', '产品规格', '产品名称', '产品价格', '产品用途', '保存条件', '产品分类', '产品包装', '产品单位','是否有货']
    for item in table:
        names=item.find_all('td',{'align':'right'})
        values=item.find_all('td',{'align':'left'})
        for i in range(len(names)):
            data[names[i].get_text().replace('：','').replace('\n','')]=values[i].get_text().replace('\xa0','')
    result=[]
    for key in keys:
        try:
            result.append(data[key])
        except:
            result.append('')
    return result

def parser_page(html):
    soup=BeautifulSoup(html,'html.parser')
    table=soup.find('table',id='ctl00_ContentPlaceHolder1_GridView1').find_all('tr')
    result=[]
    for item in table:
        try:
            tds=item.find_all('td')
            if len(tds)==0:
                continue
            line=[]
            for td in tds:
                try:
                    line.append(td.get_text().replace('\r','').replace('\n','').replace('\t',''))
                except:
                    line.append('')
            result.append(line)
        except:
            continue
    return result

def main():
    browser=webdriver.Chrome('../chromedriver')
    browser.get('http://222.35.47.118/web/shopcart/Dianosticum.aspx')
    browser.implicitly_wait(10)
    while True:
        items=parser_page(browser.page_source)
        index=0
        while index<len(items):
            while True:
                try:
                    if index+2<10:
                        browser.find_element_by_id('ctl00_ContentPlaceHolder1_GridView1_ctl0%s_LinkButton1'%(index+2)).click()
                    else:
                        browser.find_element_by_id('ctl00_ContentPlaceHolder1_GridView1_ctl%s_LinkButton1'%(index+2)).click()
                    break
                except:
                    print('failed')
                    continue
            time.sleep(1)
            line=parser_detail(browser.page_source)
            f=open('data/10_2.txt','a',encoding='utf-8')
            f.write(str(items[index]+line)+'\n')
            f.close()
            browser.back()
            time.sleep(1)
            index+=1
            print(index,len(items))
        browser.find_element_by_link_text('[下页]').click()
        time.sleep(1)

main()
