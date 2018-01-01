from util import *
from bs4 import BeautifulSoup
import re
import json
import logging
import time

def get_travels():
    pn=0
    while True:
        url='https://lvyou.baidu.com/search/ajax/search?sid=5732784045d63412748e9cfb&format=ajax&word=%E9%83%BD%E6%B1%9F%E5%A0%B0&ori_word=%E9%83%BD%E6%B1%9F%E5%A0%B0&father_place=%E6%88%90%E9%83%BD&pn={}&sort_key=6&rn=6&t=1514730499138'.format(pn)
        res=build_request(url)
        res_data=json.loads(res.text)['data']
        f=open('./baidu/urls.txt','a')
        for item in res_data['search_res']['notes_list']:
            title=item['title']
            url=item['loc']
            viewnum=item['view_count']
            commentnum=item['common_posts_count']
            create_time=int(item['create_time'])
            create_time_str=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(create_time))
            start_time=int(item['start_time'])
            start_time_str=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(start_time))
            f.write(str([title,url,viewnum,commentnum,create_time_str,start_time_str])+'\n')
        f.close()
        print(pn,'OK')
        time.sleep(1)
        if pn==624:
            break
        pn+=6

def get_travel_content(url):
    res=build_request(url)
    res_text=res.text.encode('iso-8859-1').decode('utf-8','ignore')
    soup=BeautifulSoup(res_text,'lxml').find('article',{'class':'main-article'})
    content=''
    try:
        content+=soup.find('ul',{'class':'basic-info-container'}).get_text().replace('\r', '').replace('\n', ' ').replace('\xa0','')
    except:
        pass
    try:
        content+=soup.find('div',{'class':'catalog-wrapper'}).get_text().replace('\r', '').replace('\n', ' ').replace('\xa0','')
    except:
        pass
    items=soup.find('ul',{'class':'master-posts-list'}).find_all('li',{'class':'post-item'})
    img_list=[]
    for item in items:
        try:
            content_div=item.find('div',{'class':'content'})
            content+=content_div.get_text().replace('\r', '').replace('\n', ' ').replace('\xa0','')
            img_items=content_div.find_all('img',{'class':'notes-photo-img'})
            for img_item in img_items:
                try:
                    img_url ='http:' +img_item.get('data-src')
                except:
                    continue
                img_list.append(img_url)
        except:
            pass
    content=re.sub('ue\d+','',content)
    result = {
            'content': content.replace('\\',''),
            'images': img_list
        }
    return result

def get_info():
    for line in open('./baidu/urls.txt', 'r'):
        line = eval(line)
        url = line[1]
        try:
            result = get_travel_content(url)
        except Exception as e:
            #logging.exception(e)
            with open('./baidu/failed.txt','a') as f:
                f.write(str(line)+'\n')
            print(url,'Failed')
            continue
        result['baseinfo'] = line
        f = open('baidu/travels.txt', 'a')
        str_line = json.dumps(result)
        f.write(str_line + '\n')
        f.close()
        print(url,len(result['images']), 'OK')
        time.sleep(0.5)

get_info()