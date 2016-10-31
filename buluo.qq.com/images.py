import requests
from bs4 import BeautifulSoup
import os
import json
import time


headers = {
    'X-Requested-With': 'XMLHttpRequest',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    'Referer': 'http://buluo.qq.com/mobile/barindex.html?_wv=1027&_bid=128&from=recentvisited&bid=15226',
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36"}

def get_page(bid,page):
    data={
    'bid':bid,
    'num':'10',
    'start':page*10,
    'bkn':''
    }
    html=requests.post('http://buluo.qq.com/cgi-bin/bar/post/get_post_by_page',headers=headers,data=data).text
    data=json.loads(html)['result']['posts']
    result=[]
    for item in data:
        try:
            title=item['title']
            pic_list=item['post']['pic_list']
        except:
            continue
        result.append([title,pic_list])
    return result

def save_image(filedir,filename,img_url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36"}
    content=requests.get(img_url,headers=headers,timeout=30).content
    with open('images/%s/%s.jpg'%(filedir,filename),'wb') as img:
        img.write(content)

def main():
    bid=input("输入bid:")
    try:
        startpage=input("起始页码:")
        startpage=int(startpage)-1
    except:
        startpage=0
    try:
        endpage=input("结束页码:")
        endpage=int(endpage)-1
    except:
        endpage=10
    filedir=1
    try:
        os.mkdir('images/')
    except:
        pass
    while startpage<=endpage:
        images=get_page(bid,startpage)
        for image in images:
            try:
                os.mkdir('images/'+str(filedir))
            except:
                pass
            f=open('images/%s/content.txt'%filedir,'a',encoding='utf-8')
            f.write(image[0])
            f.close()
            imgnum=1
            for img in image[1]:
                try:
                    save_image(filedir,imgnum,img['url'])
                except:
                    continue
                imgnum+=1
            print('page',startpage,filedir,'ok')
            filedir+=1
        startpage+=1
        print(startpage,'ok')
        time.sleep(2)

main()
