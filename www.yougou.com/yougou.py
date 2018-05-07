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
    need_brands = [
        'nike',
        'adidas',
        'skechers',
        'adidasoriginals',
        'converse',
        'vans',
        'puma',
        'adidasneo'
    ]
    need_keys = ['commodityName', 'commodityNo',
                 'pageUrl', 'marketPrice', 'ygPrice', 'salePrice']
    exists = {}
    result = []
    for brand in need_brands:
        page_no = 1
        while page_no > 0:
            for tag in [1, 2, 3]:
                data = {
                    'brandEnName': brand,
                    'catgNo': 'PTK',
                    'attrStr': 0,
                    'pageNo': page_no,
                    'orderBy': 0,
                    'mctcd': '',
                    'storeId': '',
                    'tag': tag
                }
                try:
                    req = build_request(
                        'http://www.yougou.com/sr/searchFilterAjax.sc', data=data)
                    product_list = req.json()[0]['resultList']
                except Exception as e:
                    print(current_time(), 'get_products fail.brand:%s page:%s tag:%s' % (
                        brand, page_no, tag))
                    continue
                if len(product_list) == 0:
                    page_no = -2
                    break
                for item in product_list:
                    if item['commodityNo'] in exists:
                        continue
                    exists[item['commodityNo']] = 1
                    line = [brand]
                    for key in need_keys:
                        try:
                            value = item[key]
                        except:
                            value = ''
                        if key == 'pageUrl':
                            value = 'http://www.yougou.com/{}.shtml'.format(
                                value)
                        line.append(value)
                    result.append(line)
                print(current_time(), 'get_products success.brand:%s page:%s tag:%s' % (
                    brand, page_no, tag))
                time.sleep(1)
            page_no += 1
    return result


def get_product_info(c_no, pd_url):
    req = build_request(pd_url)
    res_text = req.text
    soup = BeautifulSoup(res_text, 'lxml')
    try:
        style_no = re.findall('styleNo:"(.*?)",', res_text.replace(' ', ''))[0]
    except:
        style_no = ''
    try:
        goodSizeNos = re.findall(
            'goodSizeNos="(.*?)";', res_text.replace('\r', '').replace('\n', '').replace(' ', ''))[0]
        good_size_list = []
        for size in goodSizeNos.split(','):
            if size == '':
                continue
            good_size_list.append(size)
    except:
        good_size_list = []
    try:
        color = soup.find('p', {'class': 'attrib'}).find(
            'a', {'class': 'select'}).get('data-name')
    except:
        color = ''
    size_spec_item_list = soup.find('p', {'class': 'prosize'}).find(
        'span', {'class': 'prodSpec'}).find_all('a')
    size_dict = {}
    for i in range(len(good_size_list)):
        size_name = size_spec_item_list[i].get_text()
        size_key = good_size_list[i]
        size_dict[size_key] = size_name
    try:
        detail_data = get_detail_info(c_no)
    except:
        pass
    try:
        is_support_coupon = str(detail_data['isSupportCoupon'])
    except:
        is_support_coupon = ''
    ava_size_list = []
    try:
        inventory = detail_data['inventory']
    except:
        inventory = []
    for key in inventory:
        if str(key) in size_dict:
            ava_size_list.append([size_dict[key], inventory[key]])
    try:
        active_name = detail_data['active']['activeName']
    except:
        active_name = ''
    try:
        start_time = detail_data['active']['startTime']
    except:
        start_time = ''
    try:
        end_time = detail_data['active']['endTime']
    except:
        end_time = ''
    product_info = [style_no, color, is_support_coupon,
                    active_name, start_time, end_time]
    if len(ava_size_list) == 0:
        return [product_info]
    result = []
    for size_item in ava_size_list:
        result.append(product_info+size_item)
    return result


def get_detail_info(c_no):
    detail_url = 'http://www.yougou.com/commodity/getGoodsDetail.sc?cNo={}'.format(
        c_no)
    req = build_request(detail_url)
    detail_data = req.json()
    return detail_data


class YougouProduct(threading.Thread):
    def __init__(self, base_info):
        super(YougouProduct, self).__init__()
        self.base_info = base_info
        self.pdp_url = self.base_info[3]
        self.c_no = self.base_info[2]

    def run(self):
        self.lines = []
        try:
            self.product_list = get_product_info(self.c_no, self.pdp_url)
        except Exception as e:
            print(current_time(),
                  '[get_product_info][error]', self.pdp_url, e)
            self.product_list = [['']]
        try:
            number = re.findall('[0-9a-zA-Z-]+', self.base_info[1])[-1]
        except:
            number = ''
        for item in self.product_list:
            self.lines.append(self.base_info+[number]+item)


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
            task = YougouProduct(item)
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
                   current_time().replace(':', '_')+'_yougou' + '.xlsx')


crawl()
