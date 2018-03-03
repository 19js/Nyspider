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
                url, headers=headers, proxies=get_proxies_abuyun(), timeout=15)
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
    need_urls = ['https://www.adidas.com.cn/plp/list.json?pf=25-40%2C25-60%2C25-60&pr=-&fo=p25%2Cp25&pn={}&pageSize=120&p=%E7%94%B7%E5%AD%90-%E4%B8%AD%E6%80%A7&isSaleTop=false',
                 'https://www.adidas.com.cn/plp/list.json?ni=112&pf=25-82%2C25-60%2C25-60&pr=-&fo=p25%2Cp25&pn={}&pageSize=120&p=%E5%A5%B3%E5%AD%90-%E4%B8%AD%E6%80%A7&isSaleTop=false',
                 'https://www.adidas.com.cn/plp/list.json?ni=139&pf=25-160%2C25-220%2C24-250%2C24-239%2C24-39&pr=-&fo=p25%2Cp25%2Cp24%2Cp24%2Cp24&pn={}&pageSize=120&p=%E7%94%B7%E7%AB%A5-%E5%A5%B3%E7%AB%A5-%E5%A4%A7%E7%AB%A5%EF%BC%888-14%E5%B2%81%EF%BC%89-%E5%B0%8F%E7%AB%A5%EF%BC%884-8%E5%B2%81%EF%BC%89-%E5%A9%B4%E7%AB%A5%EF%BC%880-4%E5%B2%81%EF%BC%89&isSaleTop=false']
    result = []
    for base_url in need_urls:
        page = 1
        failed_times = 0
        while True:
            try:
                url = base_url.format(page) + '&_=' + \
                    str(int(time.time() * 1000))
                req = build_request(url)
                res = json.loads(req.text)
                return_obj = res['returnObject']
                if 'view' not in return_obj:
                    break
            except Exception as e:
                print(current_time(), '[get_products][request error]', url, e)
                failed_times += 1
                if failed_times == 3:
                    break
                continue
            failed_times = 0
            try:
                items = return_obj['view']['items']
            except Exception as e:
                break
            for item in items:
                base_info = {}
                try:
                    base_info['title'] = item['t']
                except:
                    base_info['title'] = '-'
                try:
                    base_info['s_title'] = item['st']
                except:
                    base_info['s_title'] = ''
                try:
                    base_info['original_price'] = item['lp']
                except:
                    base_info['original_price'] = '-'
                try:
                    base_info['real_price'] = item['sp']
                except:
                    base_info['real_price'] = '-'
                base_info['code'] = item['c']
                result.append(base_info)
            print(current_time(), '[get_products]', 'Url', url, 'OK')
            page += 1
    return result


def get_ava_sku(item_id):
    sku_str = "[]"
    for i in range(3):
        try:
            url = 'https://www.adidas.com.cn/productGetItemIvts/{}.json?_={}'.format(
                item_id, str(int(time.time() * 1000)))
            req = build_request(url)
            res_text = req.text
            data = json.loads(res_text)
            sku_str = data['skuStr']
            break
        except:
            continue
    result = json.loads(sku_str)
    return result


def get_product_info(url):
    req = build_request(url)
    soup = BeautifulSoup(req.text, 'lxml')
    item_id = soup.find("input", {"id": 'itemId'}).get("value")
    color = soup.find("input", {'id': 'colorDisPaly'}).get('value')
    try:
        login_info=soup.find('div',{'class':'login-text'}).find('p').get_text()
    except Exception as e:
        login_info=''
    table = soup.find('div', {'class': 'overview product-size'}).find_all("li")
    product_size = []
    for li in table:
        display_size = li.get_text()
        size_id = li.get('ipi')
        product_size.append([size_id, display_size])
    ava_list = get_ava_sku(item_id)
    sku_info = []
    for item in product_size:
        for ava_sku in ava_list:
            if item[0] in ava_sku['properties']:
                sku_info.append([item[1], ava_sku['availableQty']])
                break
    return {
        'color': color,
        'login_info':login_info,
        'sku_info': sku_info
    }


class AdidasProduct(threading.Thread):
    def __init__(self, base_info):
        super(AdidasProduct, self).__init__()
        self.base_info = base_info
        self.pdp_url = self.base_info[-1]

    def run(self):
        try:
            self.product = get_product_info(self.pdp_url)
        except Exception as e:
            print(current_time(),
                  '[get_product_info][error]', self.pdp_url, e)
            self.product = {'color': '','login_info':'', 'sku_info': []}
        self.lines = []
        if len(self.product['sku_info']) == 0:
            self.lines.append(self.base_info + [self.product['color'],self.product['login_info']])
        else:
            for sku_item in self.product['sku_info']:
                line = self.base_info + [self.product['color'],self.product['login_info']] + sku_item
                self.lines.append(line)


def load_products():
    products = get_products()
    keys = ['title', 's_title', 'original_price',
            'real_price', 'code']
    items = []
    for product in products:
        item = []
        for key in keys:
            value = product[key]
            item.append(value)
        item.append('https://www.adidas.com.cn/item/' + product['code'])
        items.append(item)
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
            task = AdidasProduct(item)
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
    current_dir = os.getcwd()
    write_to_excel(result, current_dir+'/files/' +
                   current_time().replace(':', '_')+'_adidas' + '.xlsx')


crawl()
