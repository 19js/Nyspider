from bs4 import BeautifulSoup
import time
from util import *
import json
import re


def load_category():
    html=open('./category.html','r').read()
    table=BeautifulSoup(html,'lxml').find_all('span',{'class':'wk-pointer-hand'})
    f=open('./files/types.txt','w')
    for item in table:
        id=item.get('data-id')
        name=item.get_text()
        f.write(str([name,id])+'\n')
    f.close()


def get_lecture(category_id,page):
    url='https://m.weike.fm/account/api_get_category_lecture?category={}&p={}'.format(category_id,page)
    cookies='__DAYU_PP=iyBAJ2A7frN6eyA3zfZA234a6f724dae; UM_distinctid=160ef71f28f241-0cb564bb3c435-32677403-13c680-160ef71f290a9b; sessionid=".eJyrVkoqLc7MSy0uji8tylGyUtJPTE7OL80r0U8syIxPTy2JT04sSU3PL6qMz8xLSa2wh3FtDZR0lKBqM1N0y4yVrEzMzIwszYxNagFXJx4d:1eaKiZ:fUn3Z9eUKg_UTmYBqvMighxBRvQ"; CNZZDATA1259942212=288688765-1515841740-%7C1515844972'
    req=build_request(url,cookies=cookies)
    res=json.loads(req.text)['data']['ret']
    return res

def weike():
    for line in open('./files/types.txt','r'):
        item=eval(line)
        page=1
        while True:
            try:
                result=get_lecture(item[1],page)
            except Exception as e:
                print(item,page,e)
                return
            if len(result)==0:
                break
            f=open('./files/result.txt','a')
            for lecture in result:
                lecture['baseinfo']=item
                f.write(json.dumps(lecture)+'\n')
            f.close()
            print(item,page,'OK')
            page+=1
            time.sleep(1)

def load_result():
    keys=['name','popular','lecture_money']
    for line in open('./files/result.txt','r'):
        item=json.loads(line)
        lecture=[item['baseinfo'][0]]
        for key in keys:
            try:
                value=item[key]
                lecture.append(value)
            except Exception as e:
                import logging
                logging.exception(e)
                lecture.append('')
        yield lecture

# weike()
write_to_excel(load_result(),'./files/result.xlsx',write_only=False)
        



        

