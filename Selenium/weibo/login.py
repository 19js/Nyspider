#coding:utf-8

from selenium  import  webdriver
from bs4 import BeautifulSoup
import getpass
import time

def login(user,passwd):
    browser=webdriver.Firefox()
    browser.get('http://weibo.com/login.php')
    browser.find_element_by_name('username').send_keys(user)
    browser.find_element_by_name('password').send_keys(passwd)
    browser.find_elements_by_class_name('W_login_form').submit()
    return browser

def main():
    user='191081279@qq.com'
    passwd=getpass.getpass("Input passwd:")
    browser=login(user, passwd)

if __name__=='__main__':
    main()
