from selenium import webdriver
from bs4 import BeautifulSoup
import time


def getBrowser(url):
    browser=webdriver.Firefox()
    browser.get(url)
    browser.implicitly_wait(10)
    return browser

def parser(html):
    text="发布者：%s\r\n发布时间：%s\r\n内容：%s\r\n\r\n\r\n"
    table=BeautifulSoup(html,'html.parser').find_all('td',{'class':['plc','postContent']})
    result=[]
    for item in table:
        try:
            postinfo=item.find('p',{'class':'postinfo'})
            name=postinfo.find('span',{'class':'gn'}).get_text()
            date=postinfo.find('span',{'class':'posttime'}).get('title')
            content=item.find('div',{'class':'pctmessage'}).get_text().replace('\r','').replace('\n','')
        except:
            continue
        result.append(text%(name,date,content))
        try:
            replaylist=item.find('div',{'class':'replaylist'}).find_all('div',{'class':'replayitem cl'})
        except:
            continue
        for reply in replaylist:
            name=reply.find('b').get_text()
            date=reply.find('span',{'class':'posttime'}).get_text()
            content=reply.find('div',{'class':'remessage'}).get_text().replace('\r','').replace('\n','')
            result.append(text%(name,date,content))
    return result


def main():
    browser=getBrowser('http://qgc.qq.com/313872977')
    while True:
        url=input("输入链接:")
        url=url.split('?')[0]
        browser.get(url)
        input("开始抓取？")
        time.sleep(3)
        startpage=1
        f=open('result.txt','a',encoding='utf-8')
        while True:
            startpage+=1
            result=parser(browser.page_source)
            if result==[]:
                break
            for item in result:
                f.write(item)
            browser.get(url+'?page=%s'%startpage)
            time.sleep(3)
        f.close()

main()
