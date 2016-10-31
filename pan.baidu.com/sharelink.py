import requests
import time
from bs4 import BeautifulSoup
import json
import re
from selenium import webdriver


headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
    'Accept':"image/png,image/*;q=0.8,*/*;q=0.5",
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate'}

browser=webdriver.Firefox()
browser.get('https://pan.baidu.com')
browser.implicitly_wait(10)
input("开始抓取？")

def search_from_tieba():
    url='http://tieba.baidu.com/mo/q/seekcomposite?pn=1&rn=10&is_ajax=1&sort=1&word=homepage'
    html=requests.get(url,headers=headers).text
    data=json.loads(html)['data']['data']['post']
    result=[]
    timenow=int("%d"%time.time())
    exists=[]
    for item in data:
        pub_time=int(item['time'])
        if timenow-pub_time>3600:
            continue
        urls=re.findall('(http://pan.baidu.com/.*?short=[a-zA-Z\d]+)',item['brief'])
        for url in urls:
            if url in exists:
                continue
            url=url.replace('&lt;em&gt;','').replace('&lt;/em&gt;','')
            exists.append(url)
            result.append(url)
    return result

def get_from_wangpan07():
    html=requests.get('http://m.wangpan007.com/wap/mbox',headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'search_list'}).find_all('li')
    result=[]
    for li in table:
        try:
            url=li.find('a',{'class':'ti_item'}).get('href')
            if '/redirect/mbox' in url:
                try:
                    timenow=li.find('div',{'class':'ti_time'}).get_text()
                except:
                    continue
                '''
                if '小时' in timenow:
                    continue
                '''
                result.append('http://m.wangpan007.com/'+url)
        except:
            continue
    return result

def is_ok(url):
    try:
        browser.get(url)
        time.sleep(2)
    except:
        return False
    html=browser.page_source
    url=browser.current_url.replace('#share/type=session','')
    try:
        table=BeautifulSoup(html,'lxml').find('div',{'class':'invite-group-dialog'})
    except:
        return False
    if '加入该群组' in str(table):
        return url
    else:
        return False

def write_to_txt(result):
    timenow=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    f=open('result/result.txt','a',encoding='utf-8')
    for line in result:
        f.write(timenow+'\t'+line+'\r\n')
    f.close()

try:
    sleep_time=input("输入刷新时间（s）：")
    sleep_time=int(sleep_time)
except:
    sleep_time=20
try:
    import os
    os.mkdir('result')
except:
    pass
while True:
    try:
        urls=search_from_tieba()
    except:
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'百度贴吧采集失败')
        urls=[]
    try:
        urls+=get_from_wangpan07()
    except:
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'网盘007采集失败')
    result=[]
    for url in urls:
        line=is_ok(url)
        if line==False:
            continue
        result.append(url)
    write_to_txt(result)
    print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'ok')
    time.sleep(sleep_time)
