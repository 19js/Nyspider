from util import *
from bs4 import BeautifulSoup
import re
import json


def get_travels():
    page = 1
    while True:
        url = 'http://you.ctrip.com/travels/qingchengshan143879/t3-p{}.html'.format(page)
        res = build_request(url)
        res_text = res.text
        table = BeautifulSoup(res_text, 'lxml').find(
            'div', {'class': 'journalslist'}).find_all('a', {'class': 'journal-item'})
        f = open('ctrip/urls.txt', 'a')
        for item in table:
            url = 'http://you.ctrip.com/' + item.get('href')
            try:
                title = item.find('dt', {'class': 'ellipsis'}).get_text()
            except:
                title = '-'
            try:
                date_str = item.find('dd', {'class': 'item-user'}).get_text()
                date_str = re.sub('.*?发表于', '', date_str)
            except:
                date_str = '-'
            try:
                numview = item.find('i', {'class': 'numview'}).get_text()
            except:
                numview = '-'
            try:
                want = item.find('i', {'class': 'want'}).get_text()
            except:
                want = '-'
            try:
                numreply = item.find('i', {'class': 'numreply'}).get_text()
            except:
                numreply = '-'
            line = [title, url, date_str, numview, numreply, want]
            f.write(str(line) + '\n')
        f.close()
        print(len(table), page, 'OK')
        if page == 71 or len(table) == 0:
            break
        time.sleep(2)
        page += 1


def get_travel_content(url):
    res = build_request(url)
    res_text = res.text
    content_items = BeautifulSoup(res_text, 'lxml').find_all('div', {'class': 'ctd_content'})
    content=''
    img_list = []
    for soup in content_items:
        content += soup.get_text().replace('\r', '').replace('\n', ' ')
        content = re.sub('作者推荐住宿.*?发表于', '', content)
        items = soup.find_all('div', {'class': 'img'})
        for item in items:
            try:
                img_url = item.find('img').get('data-original')
            except:
                continue
            img_list.append(img_url)
        items = soup.find_all('div', {'class': 'w_img '})
        for item in items:
            try:
                img_url = item.find('img').get('data-original')
            except:
                continue
            img_list.append(img_url)
    result = {
        'content': content,
        'images': img_list
    }
    return result


def get_info():
    for line in open('./ctrip/urls.txt', 'r'):
        line = eval(line)
        url = line[1]
        result = get_travel_content(url)
        result['baseinfo'] = line
        f = open('ctrip/travels.txt', 'a')
        str_line = json.dumps(result)
        f.write(str_line + '\n')
        f.close()
        print(url, 'OK')
        time.sleep(0.5)

get_info()
