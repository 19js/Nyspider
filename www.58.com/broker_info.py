import requests
from bs4 import BeautifulSoup
import openpyxl
import logging
import time
import os
from proxy import gen_proxies

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0"}

proxy = gen_proxies()


def get_house_url(base_url):
    start_page = 1
    result = []
    while True:
        page_url = base_url.format(start_page)
        try:
            html = requests.get(page_url, headers=headers, timeout=20).text
        except Exception as e:
            logging.exception(e)
            continue
        house_list = BeautifulSoup(html, 'lxml').find_all(
            'div', {'class': 'list-info'})
        if house_list == []:
            break
        for item in house_list:
            url = item.find('a').get('href')
            result.append(url)
        print('Page', start_page, 'OK')
        if start_page == 70:
            break
        start_page += 1
        time.sleep(1)
    return result


def get_house_url_from_chuzu(base_url):
    start_page = 1
    result = []
    while True:
        page_url = base_url.format(start_page)
        try:
            html = requests.get(page_url, headers=headers, timeout=20).text
        except Exception as e:
            logging.exception(e)
            continue
        house_list = BeautifulSoup(html, 'lxml').find_all(
            'div', {'class': 'des'})
        if house_list == []:
            break
        for item in house_list:
            url = item.find('a').get('href')
            result.append(url)
        print('Page', start_page, 'OK')
        if start_page == 70:
            break
        start_page += 1
        time.sleep(1)
    return result


def get_broker_info(url):
    while True:
        proxies = next(proxy)
        print(proxies)
        try:
            html = requests.get(url, headers=headers,
                                proxies=proxies, timeout=10).text
            if '访问过于频繁，本次访问做以下验证码校验' in html:
                continue
            break
        except:
            continue
    basic_item = BeautifulSoup(html, 'lxml').find(
        'div', {'class': 'house-basic-right'})
    broker_info = basic_item.find('span', {'class': 'f14 c_333 jjrsay'})
    if broker_info is None:
        return None
    broker_info_list = broker_info.get_text().replace(
        ' 说', '').replace(' ', '').split('-')
    if len(broker_info_list) == 1:
        company = ''
        name = broker_info_list[0]
    else:
        company = broker_info_list[0]
        name = broker_info_list[1]
    phone_num = basic_item.find('p', {'class': 'phone-num'}).get_text()
    return [company, name, phone_num]


def get_broker_info_from_chuzu(url):
    while True:
        proxies = next(proxy)
        print(proxies)
        try:
            html = requests.get(url, headers=headers,
                                proxies=proxies, timeout=10).text
            if '访问过于频繁，本次访问做以下验证码校验' in html:
                continue
            break
        except:
            continue
    basic_item = BeautifulSoup(html, 'lxml').find(
        'div', {'class': 'house-basic-right'})
    broker_info = basic_item.find('div', {'class': 'house-agent-info'})
    if broker_info is None:
        return None
    try:
        name = broker_info.find('p', {'class': 'agent-name'}).get_text()
    except:
        name = ''
    try:
        company = broker_info.find('p', {'class': 'agent-subgroup'}).get_text()
    except:
        company = ''
    phone_num = basic_item.find('span', {'class': 'house-chat-txt'}).get_text()
    return [company, name, phone_num]


def crawl_house_urls():
    try:
        os.mkdir('result')
    except:
        pass
    crawl_items = {
        #'商铺':'http://cs.58.com/shangpucz/1/pn{}/?PGTID=0d306b35-0019-e86b-5030-7e5735102e73&ClickID=2',
        '租房': 'http://cs.58.com/chuzu/1/pn{}/?PGTID=0d3090a7-0019-e341-c6a5-383216d97b49&ClickID=2',
        #'二手房':'http://cs.58.com/ershoufang/pn{}/?PGTID=0d300000-0000-01b0-4f40-479567e74208&ClickID=1'
    }
    for item in crawl_items.items():
        if item[0] == '租房':
            result = get_house_url_from_chuzu(item[1])
        else:
            result = get_house_url(item[1])
        with open('result/%s_urls.txt' % (item[0]), 'w') as f:
            for url in result:
                f.write(url + '\n')
        print(item, 'OK')


def crawl_broker_phone_num():
    crawl_items = ['商铺', '租房', '二手房']
    counter = 1
    for item in crawl_items:
        for line in open('result/%s_urls.txt' % item, 'r'):
            url = line.replace('\n', '')
            if item == '租房':
                func = get_broker_info_from_chuzu
            else:
                func = get_broker_info
            try:
                info = func(url)
            except:
                with open('result/failed.txt','a') as f:
                    f.write(str([item,url])+'\n')
                print(item, url, 'Failed')
                continue
            with open('result/result.txt', 'a') as f:
                f.write(str([item] + info) + '\n')
            print(counter, 'OK')
            counter += 1


if __name__ == '__main__':
    #crawl_house_urls()
    crawl_broker_phone_num()
