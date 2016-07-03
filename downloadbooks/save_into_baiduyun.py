from selenium import webdriver
import time

def get_browser():
    browser=webdriver.Firefox()
    browser.get('http://yun.baidu.com/#from=share_yun_logo')
    browser.implicitly_wait(10)
    time.sleep(2)
    return browser

def main():
    browser=get_browser()
    input('login?')
    for line in open('books.txt','r'):
        line=line.replace('\n','')
        url=line.split('||')[-1]
        if 'http://pan.baidu.com' not in url:
            continue
        browser.get(url)
        try:
            browser.find_element_by_id('emphasizeButton').click()
            time.sleep(3)
            browser.find_element_by_id('_disk_id_6').click()
            time.sleep(3)
        except:
            continue

main()
