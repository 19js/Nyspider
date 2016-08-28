#coding:utf-8
import requests
import json
import time
import re


headers = {
    'Host':"map.baidu.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def citys():
    html=requests.get('http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=baidu&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%E6%B1%BD%E8%BD%A6%E7%BE%8E%E5%AE%B9%E5%BA%97&c=1&src=0&wd2=&sug=0&l=5&b=(7002451.220000001,1994587.88;19470675.22,7343963.88)&from=webmap&biz_forward={%22scaler%22:1,%22styles%22:%22pl%22}&sug_forward=&tn=B_NORMAL_MAP&nn=0&u_loc=12736591.152491,3547888.166124&ie=utf-8&t=1459951988807',headers=headers).text
    f=open('city_ids.txt','a')
    data=json.loads(html)
    for item in data['content']:
        #for city in item['city']:
            f.write(str(item)+'\n')
    f.close()

def get_infor(keyword,code,page):
    html=requests.get('http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=baidu&pcevaname=pc4.1&qt=con&from=webmap&c='+str(code)+'&wd='+keyword+'&wd2=&pn='+str(page)+'&nn='+str(page*10)+'&db=0&sug=0&addr=0&&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=12&tn=B_NORMAL_MAP&u_loc=12736591.152491,3547888.166124&ie=utf-8',headers=headers).text
    data=json.loads(html)['content']
    return data


def main():
    keys=['眼镜店','视光中心']
    for keyword in keys:
        f=open(keyword+'_tels.txt','a')
        for line in open('city_ids.txt','r').readlines():
            line=line.replace('\n','')
            code=eval(line)['code']
            page=1
            while True:
                try:
                    data=get_infor(keyword,code,page)
                except:
                    break
                if data==[]:
                    break
                for item in data:
                    f.write(str(item)+'\n')
                page+=1
                print(code,page)
                time.sleep(1)
        f.close()
main()
