import json
import re
import time
from bs4 import BeautifulSoup
import requests
import openpyxl
import random
import threading
import os


def get_headers():
    pc_headers = {
        "X-Forwarded-For": '%s.%s.%s.%s' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    return pc_headers


def get_proxies_abuyun():
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"
    # 代理隧道验证信息
    proxyUser = ''
    proxyPass = ''

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies


class NetWorkError(Exception):
    pass


def build_request(url, headers=None, proxies=None):
    if headers is None:
        headers = get_headers()
    for i in range(5):
        try:
            response = requests.get(
                url, headers=headers, timeout=15)
            return response
        except Exception as e:
            if '429' in str(e):
                time.sleep(random.randint(0, 1000)/1000.0)
            continue
    raise NetWorkError


def write_to_excel(lines, filename, write_only=True):
    excel = openpyxl.Workbook(write_only=write_only)
    sheet = excel.create_sheet()
    for line in lines:
        sheet.append(line)
    excel.save(filename)


def current_time():
    now_time = time.strftime('%Y-%m-%d %H:%M:%S')
    return now_time


def get_products():
    base_urls = [
        'https://www.converse.com.cn/men-sneakers/category.htm?attributeParams=&propertyCode=&sort=showOrder&pageNo={}&isPaging=false',
        'https://www.converse.com.cn/men-clothing/category.htm?attributeParams=&propertyCode=&sort=showOrder&pageNo={}&isPaging=false',
        'https://www.converse.com.cn/men-accessories/category.htm?attributeParams=&propertyCode=&sort=showOrder&pageNo={}&isPaging=false',
        'https://www.converse.com.cn/women-sneakers/category.htm?attributeParams=&propertyCode=&sort=showOrder&pageNo={}&isPaging=false',
        'https://www.converse.com.cn/women-clothing/category.htm?attributeParams=&propertyCode=&sort=showOrder&pageNo={}&isPaging=false',
        'https://www.converse.com.cn/kids-sneakers/category.htm?attributeParams=&propertyCode=&sort=showOrder&pageNo={}&isPaging=false'
    ]
    result = []
    for base_url in base_urls:
        page = 1
        while True:
            try:
                req = build_request(base_url.format(page))
            except Exception as e:
                print(current_time(), '[get_products][request error]', url, e)
                continue
            table = BeautifulSoup(req.text, 'lxml').find_all('dl')
            if len(table) == 0:
                break
            for dl in table:
                try:
                    sku_code = dl.get('skucode')
                    name = dl.find('a').get('alt')
                    try:
                        pre_price = dl.find(
                            'dd', {'class': 'p-l-price linethrough'}).get_text()
                    except:
                        pre_price = '-'
                    real_price = dl.find_all(
                        'dd', {'class': 'p-l-price'})[-1].get_text()
                    url = 'https://www.converse.com.cn/all_star/{}/item.htm'.format(
                        sku_code)
                    result.append([name, sku_code, url, pre_price, real_price])
                except:
                    continue
            print(current_time(), '[get_products]',
                  'Url', base_url.format(page), 'OK')
            page += 1
            time.sleep(1)
    return result


def parser_info(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        color = soup.find('div', {'class': 'product-info'}).get_text()
        color = color.split('型号')[0].replace('\r', '').replace(
            '\n', '').replace(' ', '').replace('\t', '')
    except:
        color = ''
    try:
        if '本产品已经售完' in soup.find("div", {'class': 'sold-out-tips'}).get_text():
            return [[color, '本产品已经售完']]
    except:
        pass
    size_select = soup.find('select', {'id': 'size-select'}).find_all('option')
    result = []
    for item in size_select:
        skusize = item.get('skusize')
        inventory = item.get('inventory')
        if skusize is None:
            continue
        result.append([color, skusize, inventory])
    return result


def get_product_info(url):
    for i in range(3):
        try:
            req = build_request(url)
            result = parser_info(req.text)
            return result
        except:
            time.sleep(0.5)
            continue
    raise NetWorkError


class ConverseProduct(threading.Thread):
    def __init__(self, product):
        super(ConverseProduct, self).__init__()
        self.product = product
        self.pdp_url = self.product[2]
        self.daemon = True

    def run(self):
        try:
            self.info = get_product_info(self.pdp_url)
        except Exception as e:
            print(current_time(),
                  '[get_product_info][error]', self.pdp_url, e)
            self.info = []
        self.result = []
        if len(self.info) == 0:
            self.result.append(self.product)
        else:
            for line in self.info:
                self.result.append(self.product+line)


def load_products():
    products = get_products()
    items = []
    for product in products:
        items.append(product)
        if len(items) < 5:
            continue
        yield items
        items = []
    yield items


def crawl():
    result = []
    counter = 0
    for products in load_products():
        tasks = []
        for item in products:
            task = ConverseProduct(item)
            tasks.append(task)
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        for task in tasks:
            result += task.result
            counter += 1
            print(current_time(),
                  '[get_product_info][OK]', task.pdp_url, counter)
        time.sleep(2)
    current_dir = os.getcwd()
    write_to_excel(result, current_dir+'/files/' +
                   current_time().replace(':', '_') + '.xlsx')


crawl()
