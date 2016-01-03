#coding:utf-8

from selenium import webdriver
import getpass
import time

def login(user,passwd):
    driver=webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://login.taobao.com/member/login.jhtml')
    driver.find_element_by_id('TPL_username_1').send_keys(user)
    driver.find_element_by_id('TPL_password_1').send_keys(passwd)
    driver.find_element_by_id('J_SubmitStatic').click()
    time.sleep(30)
    return driver

def main():
    user=input("Input user:")
    passwd=getpass.getpass("Input passwd:")
    browser=login(user,passwd)
    browser.get('https://www.taobao.com/')


if __name__=='__main__':
    main()
