#coding:utf-8

import requests

def get_ip():
    while True:
        ip=requests.get('http://qsdrk.daili666api.com/ip/?tid=559950660678689&num=1&delay=3&category=2&protocol=https&sortby=time&filter=on').text
        proxies={
        'http':'http://%s'%ip
        }
        if Test(proxies,ip):
            return proxies

def Test(proxies,ip):
    ip=ip.split(':')[0]
    try:
        html=requests.get('http://httpbin.org/ip',proxies=proxies,timeout=30).text
        result=eval(html)['origin']
        if ip!=result:
            print(html)
            return False
        print('--',result)
        return True
    except:
        return False

get_ip()
