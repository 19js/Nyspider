#coding:utf-8

import requests
import os
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate'}

def main():
    html=requests.get('https://www.tripadvisor.com/Attraction_Review-g294212-d325811-Reviews-Great_Wall_at_Mutianyu-Beijing.html#REVIEWS',headers=headers).text
    try:
        os.mkdir('page')
    except:
        pass
    count=0
    f=open('page'+str(count)+'.html','w')
    f.write(html)
    f.close()
    count+=1
    num=10
    while True:
        try:
            html=requests.get('https://www.tripadvisor.com/Attraction_Review-g294212-d325811-Reviews-or%s-Great_Wall_at_Mutianyu-Beijing.html#REVIEWS'%num,headers=headers).text
        except:
            continue
        f=open('page/'+str(count)+'.html','w')
        f.write(html)
        f.close()
        num+=10
        print(num)
        count+=1
        if(num==8490):
            break
        time.sleep(2)

main()
