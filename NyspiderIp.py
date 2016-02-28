#coding:utf-8

import requests
import re

def get_ip():
    while True:
        ip=requests.get('http://qsdrk.daili666api.com/ip/?tid=559950660678689&num=1&delay=1&category=2&protocol=https&filter=on').text
        proxies={
        'http':'http://%s'%ip
        }
        if Test(proxies,ip):
            return proxies

def Test(proxies,ip):
    ip=ip.split(':')[0]
    ip_rel='\[(\d+\.\d+\.\d+\.\d+)\]'
    '''
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
    '''
    try:
        html=requests.get('http://1212.ip138.com/ic.asp',proxies=proxies,timeout=20).text.encode('ISO-8859-1').decode('gbk','ignore')
        result=re.findall(ip_rel,html)[0]
        if result==ip:
            print(result,'--ok')
            return True
        return False
    except:
        return False

get_ip()
