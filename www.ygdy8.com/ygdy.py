import time
from bs4 import BeautifulSoup
import os
import requests
import random
import datetime
import json
import re


def get_headers():
    pc_headers = {
        "X-Forwarded-For": '%s.%s.%s.%s' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.ygdy8.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    return pc_headers


class NetWorkError(Exception):
    pass


def build_request(url, headers=None, data=None, json_data=None, timeout=15, try_times=5):
    if headers is None:
        headers = get_headers()
    for i in range(try_times):
        try:
            if data:
                response = requests.post(
                    url, data=data, headers=headers, timeout=timeout)
            elif json_data:
                headers['Content-Type'] = 'application/json'
                response = requests.post(
                    url, data=json.dumps(json_data), headers=headers, timeout=timeout)
            else:
                response = requests.get(url, headers=headers, timeout=timeout)
            return response
        except Exception as e:
            time.sleep(1)
            continue
    raise NetWorkError


def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def get_video_info(url):
    req = build_request(url)
    res_text = req.text.encode('iso-8859-1').decode('gbk', 'ignore')
    soup = BeautifulSoup(res_text, 'lxml').find('div', {'id': 'Zoom'})
    info = soup.get_text().replace('◎', '\r\n◎')
    download_info = []
    for item in soup.find_all('a'):
        try:
            title = item.get_text()
            url = item.get('href')
        except:
            continue
        download_info.append('标题:{}\r\n地址:{}'.format(title, url))
    info += '\r\n\r\n【下载信息】\r\n'+'\r\n\r\n'.join(download_info)
    info = info.replace('\n\n\n', '\n').replace('\r\n\r\n\r\n', '\r\n')
    return info


def get_video_list(url):
    req = build_request(url)
    res_text = req.text.encode('iso-8859-1').decode('gbk', 'ignore')
    table = BeautifulSoup(res_text, 'lxml').find(
        'div', {'class': 'co_content8'}).find('ul').find_all('b')
    result = []
    for item in table:
        try:
            a_item = item.find_all('a')[-1]
            title = a_item.get_text().replace('\r', '').replace('\n', '')
            url = 'http://www.ygdy8.com'+a_item.get('href')
            if 'color=' in str(a_item):
                continue
        except Exception as e:
            continue
        result.append([title, url])
    return result


def crawl_videos():
    types = [
        ['最新电影', 'http://www.ygdy8.com/html/gndy/dyzz/list_23_{}.html'],
        ['国内电影', 'http://www.ygdy8.com/html/gndy/china/list_4_{}.html'],
        ['欧美电影', 'http://www.ygdy8.com/html/gndy/oumei/list_7_{}.html'],
        ['日韩电影', 'http://www.ygdy8.com/html/gndy/rihan/list_6_{}.html'],
        ['华语电视', 'http://www.ygdy8.com/html/tv/hytv/list_71_{}.html'],
        ['日韩电视', 'http://www.ygdy8.com/html/tv/rihantv/list_8_{}.html'],
        ['欧美电视', 'http://www.ygdy8.com/html/tv/oumeitv/list_9_{}.html'],
        ['最新综艺', 'http://www.ygdy8.com/html/zongyi2013/list_99_{}.html'],
        ['旧版综艺', 'http://www.ygdy8.com/html/2009zongyi/list_89_{}.html'],
        ['动漫资源', 'http://www.ygdy8.com/html/dongman/list_16_{}.html'],
    ]
    try:
        os.mkdir('./files')
    except:
        pass

    for video_type, base_url in types:
        try:
            os.mkdir('./files/'+video_type)
        except:
            pass
        save_path = './files/'+video_type+'/'
        page = 1
        while True:
            try:
                videos = get_video_list(base_url.format(page))
            except:
                break
            if len(videos) == 0:
                break
            for video in videos:
                try:
                    video_info = get_video_info(video[-1])
                except:
                    continue
                try:
                    filename = save_path+video[0]+'.txt'
                    info_f = open(
                        filename, 'w', encoding='utf-8')
                    info_f.write(video_info)
                    info_f.close()
                    f = open('./目录.txt', 'a', encoding='utf-8')
                    f.write(filename+'\r\n')
                    f.close()
                except:
                    continue
            print(current_time(), video_type, '第{}页'.format(page), 'OK')
            page += 1


crawl_videos()
