from util import *
from bs4 import BeautifulSoup
import re
import json
import logging


def get_travels():
    page=1
    while True:
        url='http://trips.tuniu.com/travels/index/ajax-list?queryKey=%E9%83%BD%E6%B1%9F%E5%A0%B0&page={}&limit=10'.format(page)
        res=build_request(url)
        res_data=json.loads(res.text)['data']
        f=open('./tuniu/urls.txt','a')
        for item in res_data['rows']:
            title=item['name']
            url='http://www.tuniu.com/trips/'+str(item['id'])
            viewnum=item['viewCount']
            commentnum=item['commentCount']
            publishTime=item['publishTime']
            f.write(str([title,url,viewnum,commentnum,publishTime])+'\n')
        f.close()
        print(page,'OK')
        time.sleep(1)
        if page==8:
            break
        page+=1

def get_travel_content(url):
    res=build_request(url)
    res_text=res.text
    soup=BeautifulSoup(res_text,'lxml').find('div',{'class':'detail-content'}).find('div',{'class':'content-left'})
    content=soup.get_text().replace('\r', '').replace('\n', ' ').replace('\xa0','')
    items=soup.find_all('div',{'class':'section-img'})
    img_list=[]
    for item in items:
        try:
            img_url=item.find('img').get('data-src')
            img_list.append(img_url)
        except:
            continue
    content=re.sub('<div.*','',content)
    result = {
            'content': content,
            'images': img_list
        }
    return result

def get_info():
    for line in open('./tuniu/urls.txt', 'r'):
        line = eval(line)
        url = line[1]
        try:
            result = get_travel_content(url)
        except Exception as e:
            #logging.exception(e)
            with open('./tuniu/failed.txt','a') as f:
                f.write(str(line)+'\n')
            print(url,'Failed')
            continue
        result['baseinfo'] = line
        f = open('tuniu/travels.txt', 'a')
        str_line = json.dumps(result)
        f.write(str_line + '\n')
        f.close()
        print(url,len(result['images']), 'OK')
        time.sleep(0.5)

get_info()