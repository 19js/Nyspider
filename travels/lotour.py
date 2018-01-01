from util import *
from bs4 import BeautifulSoup
import re
import json
import logging


def get_travels():
    page=1
    while True:
        url='http://chengdu.lotour.com/dujiangyanjq/lvyouyouji-p{}'.format(page)
        res=build_request(url)
        res_text=res.text
        soup=BeautifulSoup(res_text,'lxml').find('div',{'class':'bd-jq-list'}).find_all('li')
        f=open('./lotour/urls.txt','a')
        for item in soup:
            title=item.find('h2',{'class':'jq-name'}).get_text()
            url=item.find('h2',{'class':'jq-name'}).find('a').get('href')
            publishTime=item.find('div',{'class':'gone-where'}).find('em').get_text()
            f.write(str([title,url,publishTime])+'\n')
        f.close()
        print(page,'OK')
        time.sleep(1)
        if page==2:
            break
        page+=1

def get_travel_content(url):
    res=build_request(url)
    res_text=res.text
    soup=BeautifulSoup(res_text,'lxml')
    try:
        viewnum=soup.find('span',{'class':'ia-num-like'}).get_text()
    except:
        viewnum=0
    try:
        commentnum=soup.find('h2',{'id':'commentNumH2'}).get_text().replace('\n','')
    except:
        commentnum=0
    content=soup.find('div',{'class':'ia-text'}).get_text().replace('\r', '').replace('\n', ' ').replace('\xa0','').replace('\u3000','')
    items=soup.find('div',{'class':'ia-text'}).find_all('img')
    img_list=[]
    for item in items:
        try:
            onload=item.get('onload')
            if 'resizePic' not in onload:
                continue
            img_url=item.get('data-original')
            img_list.append(img_url)
        except:
            continue
    result = {
            'content': content,
            'images': img_list,
            'viewnum':viewnum,
            'commentnum':commentnum
        }
    return result

def get_info():
    for line in open('./lotour/urls.txt', 'r'):
        line = eval(line)
        url = line[1]
        try:
            result = get_travel_content(url)
        except Exception as e:
            #logging.exception(e)
            with open('./lotour/failed.txt','a') as f:
                f.write(str(line)+'\n')
            print(url,'Failed')
            continue
        result['baseinfo'] = line+[result['viewnum'],result['commentnum']]
        f = open('lotour/travels.txt', 'a')
        str_line = json.dumps(result)
        f.write(str_line + '\n')
        f.close()
        print(url,len(result['images']), 'OK')
        time.sleep(0.5)

get_info()