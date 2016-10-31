import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
import json

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def login(username,password):
    browser=webdriver.PhantomJS('/home/nyloner/phantomjs/phantomjs')
    #browser=webdriver.Firefox()
    browser.get('https://passport.weibo.cn/signin/login?entry=mweibo&amp;res=wel&amp;wm=3349&amp;r=http%3A%2F%2Fm.weibo.cn%2F')
    browser.set_page_load_timeout(10)
    time.sleep(5)
    browser.find_element_by_id('loginName').send_keys(username)
    browser.find_element_by_id('loginPassword').send_keys(password)
    browser.find_element_by_id('loginAction').click()
    time.sleep(5)
    cookies=browser.get_cookies()
    result={}
    for item in cookies:
        try:
            result[item['name']]=item['value']
        except:
            continue
    f=open('cookies','w')
    f.write(str(result))
    f.close()
    return result

def weibo():
    if os.path.isfile('cookies'):
        cookies=eval(open('cookies','r').read())
    else:
        cookies=login('username','password')
    session=requests.session()
    session.cookies=requests.utils.cookiejar_from_dict(cookies)
    html=session.get('http://m.weibo.cn',headers=headers).text
    html=session.get('http://m.weibo.cn/index/feed?format=cards&page=1',headers=headers).text
    data=json.loads(html)[0]['card_group']
    result=[]
    for item in data:
        user=item['mblog']['user']['screen_name']
        text=item['mblog']['text']
        result.append({'user':user,'text':text})
    print(result)
    print(get_comments(session,'4013542757481643'))

def get_comments(session,weiboid):
    page=1
    html=session.get('http://m.weibo.cn/single/rcList?format=cards&id={weiboid}&type=comment&hot=0&page={page}'.format(weiboid=weiboid,page=page),headers=headers).text
    data=json.loads(html)[1]['card_group']
    comments=[]
    for item in data:
        comment={}
        comment['user']=item['user']['screen_name']
        comment['date']=item['created_at']
        comment['text']=item['text']
        comments.append(comment)
    return comments

weibo()
