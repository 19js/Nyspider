from util import *
from bs4 import BeautifulSoup
import re
import json
import logging

def get_travels():
    page=1
    while True:
        url='http://www.mafengwo.cn/search/s.php?q=%E9%83%BD%E6%B1%9F%E5%A0%B0&p={}&t=info&kt=1'.format(page)
        res=build_request(url)
        res_text=res.text
        soup=BeautifulSoup(res_text,'lxml').find('div',{'class':'att-list'}).find_all('div',{'class':'ct-text'})
        print(len(soup),page)
        f=open('./mafengwo/urls.txt','a')
        for item in soup:
            title=item.find('h3').get_text()
            url=item.find('a').get('href')
            seg_info_list=item.find('ul',{'class':'seg-info-list'}).find_all('li')
            viewnum=''
            commentnum=''
            date_str=''
            for li in seg_info_list:
                if '浏览' in str(li):
                    viewnum=li.get_text().replace('\r','').replace('\n','').replace(' ','')
                if '评论' in str(li):
                    commentnum=li.get_text().replace('\r','').replace('\n','').replace(' ','')
                if '年' in str(li):
                    date_str=li.get_text().replace('\r','').replace('\n','').replace(' ','')
            f.write(str([title,url,viewnum,commentnum,date_str])+'\n')
        f.close()
        print(page,'OK')
        time.sleep(0.5)
        if page==50:
            break
        page+=1

def get_travel_content(url):
    res = build_request(url)
    res_text = res.text
    try:
        soup = BeautifulSoup(res_text, 'lxml').find('div', {'class': 'vc_article'})
        img_list = []
        content = soup.get_text().replace('\r', '').replace('\n', ' ').replace('\xa0','')
        items = soup.find_all('div', {'class': 'add_pic _j_anchorcnt _j_seqitem'})
        for item in items:
            try:
                img_url = item.find('img').get('data-src')
            except:
                continue
            img_list.append(img_url)
        result = {
            'content': content,
            'images': img_list
        }
        return result
    except:
        soup=BeautifulSoup(res_text,'lxml').find('div',{'id':'pnl_contentinfo'})
        img_list = []
        content = soup.get_text().replace('\r', '').replace('\n', ' ').replace('\xa0','')
        items = soup.find_all('img')
        for item in items:
            try:
                img_url = item.get('data-src')
            except:
                continue
            img_list.append(img_url)
        result = {
            'content': content,
            'images': img_list
        }
        return result

def get_info():
    for line in open('./mafengwo/urls.txt', 'r'):
        line = eval(line)
        url = line[1]
        try:
            result = get_travel_content(url)
        except Exception as e:
            #logging.exception(e)
            with open('./mafengwo/failed.txt','a') as f:
                f.write(str(line)+'\n')
            print(url,'Failed')
            continue
        result['baseinfo'] = line
        f = open('mafengwo/travels.txt', 'a')
        str_line = json.dumps(result)
        f.write(str_line + '\n')
        f.close()
        print(url,len(result['images']), 'OK')
        time.sleep(0.5)

get_info()
