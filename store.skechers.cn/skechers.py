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


def build_request_by_proxy(url, data=None, headers=None):
    if headers is None:
        headers = get_headers()
    for i in range(5):
        try:
            if data is None:
                response = requests.get(
                    url, headers=headers, proxies=get_proxies_abuyun(), timeout=15)
            else:
                response = requests.post(
                    url, data=data, headers=headers, proxies=get_proxies_abuyun(), timeout=15)
            if response.status_code != 200:
                continue
            return response
        except Exception as e:
            if '429' in str(e):
                time.sleep(random.randint(0, 1000)/1000.0)
            continue
    raise NetWorkError


def build_request(url, data=None, headers=None):
    if headers is None:
        headers = get_headers()
    for i in range(5):
        try:
            if data is None:
                response = requests.get(
                    url, headers=headers, timeout=15)
            else:
                response = requests.post(
                    url, data=data, headers=headers, timeout=15)
            if response.status_code != 200:
                continue
            return response
        except Exception as e:
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
    need_urls = [
        'https://store.skechers.cn/men/men-shoes/?sz=50&start={}&format=page-element',
        'https://store.skechers.cn/men/men-apparel/?sz=50&start={}&format=page-element',
        'https://store.skechers.cn/women/women-shoes/?sz=50&start={}&format=page-element',
        'https://store.skechers.cn/women/women-apparel/?sz=50&start={}&format=page-element'
    ]
    exists = {}
    result = []
    for base_url in need_urls:
        start = 0
        failed_times = 0
        while True:
            try:
                req = build_request(base_url.format(start))
                table = BeautifulSoup(req.text.replace('\n', ''), 'lxml').find(
                    'ul', {'id': 'search-result-items'}).find_all('li', {'class': 'grid-tile'})
            except Exception as e:
                print(current_time(),
                      '[get_products][request error]', base_url.format(start), e)
                failed_times += 1
                if failed_times == 3:
                    break
                continue
            failed_times = 0
            if len(table) == 0:
                break
            for item in table:
                try:
                    name = item.find(
                        'div', {'class': 'product-name'}).find('a').get_text()
                    url = 'https://store.skechers.cn' + \
                        item.find(
                            'div', {'class': 'product-name'}).find('a').get('href')
                    if url in exists:
                        continue
                    exists[url] = 1
                except:
                    continue
                try:
                    category_name = item.find(
                        'div', {'class': 'category-name'}).get_text()
                except:
                    category_name = ''
                result.append([name, category_name, url])
            print(current_time(), '[get_products]',
                  'Url', base_url.format(start), 'OK')
            start += 50
    return result


def parser_detail(html):
    soup = BeautifulSoup(html.replace('\n','').replace('\t',''), 'lxml').find(
        'div', {'class': 'product-detail'})
    try:
        price_standard = soup.find(
            'span', {'class': 'price-standard'}).get_text().replace(' ','')
    except:
        price_standard = ''
    try:
        price_sales = soup.find('span', {'class': 'price-sales'}).get_text().replace(' ','')
    except:
        price_sales = ''
    try:
        product_number = soup.find(
            'div', {'class': 'product-number'}).get_text().replace('货号：', '').replace(' ','')
    except:
        product_number = '  '
    try:
        ul_list = soup.find('ul', {'class': 'size-swatch'}).find_all('li')
    except:
        ul_list = []
    size_list = []
    for item in ul_list:
        class_str = str(item.get('class'))
        if 'unselectable' in class_str:
            continue
        size_list.append(item.get_text().replace(' ',''))
    return [product_number,product_number[:-1], price_standard, price_sales], size_list
    

def get_goods_details(product_url):
    req = build_request(product_url)
    return parser_detail(req.text)


def get_product_info(pd_url):
    req = build_request(pd_url)
    try:
        soup = BeautifulSoup(req.text, 'lxml').find(
            'div', {'class': 'swatches color'}).find_all('div', {'class': 'item'})
    except Exception as e:
        result=[]
        product_detail, size_list=parser_detail(req.text)
        if len(size_list)==0:
            result.append(['',pd_url]+product_detail)
        else:
            for size in size_list:
                result.append(['',pd_url]+product_detail+[size])
        return result
    item_list = []
    for item in soup:
        try:
            color = item.find('a').get('title').replace('选择颜色:', '')
            url = item.find('a').get('href')
            if 'selected' in str(item.get('class')):
                url=pd_url
        except:
            continue
        item_list.append([color, url])
    result = []
    for item in item_list:
        try:
            product_detail, size_list = get_goods_details(item[-1])
        except:
            continue
        if len(size_list)==0:
            result.append(item+product_detail)
            continue
        for size in size_list:
            result.append(item+product_detail+[size])
    return result


class SkechersProduct(threading.Thread):
    def __init__(self, base_info):
        super(SkechersProduct, self).__init__()
        self.base_info = base_info
        self.pdp_url = self.base_info[-1]

    def run(self):
        self.lines = []
        try:
            self.product_list = get_product_info(self.pdp_url)
        except Exception as e:
            print(current_time(),
                  '[get_product_info][error]', self.pdp_url, e)
            return
        for item in self.product_list:
            self.lines.append(self.base_info+item)


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
            task = SkechersProduct(item)
            tasks.append(task)
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        for task in tasks:
            result += task.lines
            counter += 1
            print(current_time(),
                  '[get_product_info][OK]', task.pdp_url, counter)
    write_to_excel(result, './files/' +
                   current_time().replace(':', '_')+'_skechers' + '.xlsx')


crawl()
