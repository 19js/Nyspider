import json
import re
import time
from bs4 import BeautifulSoup
import requests
import openpyxl
import random


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
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }
    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
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
            print(e)
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
    page = 1
    result = []
    while True:
        try:
            url = 'https://store.nike.com/html-services/gridwallData?country=CN&lang_locale=zh_CN&pn={}'.format(
                page)
            req = build_request(url)
            res = json.loads(req.text)
            if res['foundProductResults'] is False:
                break
        except Exception as e:
            print(current_time(), '[get_products][request error]', url, e)
            continue
        try:
            products = res['sections'][0]['products']
        except Exception as e:
            print(current_time(),
                  '[get_products][load products error]', url, e)
            continue
        print(current_time(), '[get_products]', 'Page', page, 'OK')
        result += products
        page += 1
    return result


def get_color_and_style(res_text):
    res_text = res_text.replace('\r', '').replace('\n', '').replace(
        ' ', '').replace('\t', '').replace('\\u002F', '/').replace('：', ':')
    re_exp_dict = {
        'color': ['"colorDescription":"(.*?)"'],
        'style': ['"styleColor":"(.*?)"', '>款式:(.*?)<']
    }
    result = {}
    for key in re_exp_dict:
        value = ''
        for re_exp in re_exp_dict[key]:
            try:
                value = re.findall(re_exp, res_text)[0]
                break
            except Exception as e:
                continue
        result[key] = value
    return result


def parser_store(res_text):
    json_text = BeautifulSoup(res_text, 'lxml').find(
        'script', id='product-data').get_text()
    data = json.loads(json_text)
    sku_list = data['skuContainer']['productSkus']
    result = []
    for sku_item in sku_list:
        if sku_item['inStock'] == True:
            result.append(sku_item['displaySize'])
    return result


def get_available_skus(product_id_list):
    url = 'https://api.nike.com/deliver/available_skus/v1/?filter=productIds({})'.format(
        ','.join(product_id_list))
    for i in range(3):
        try:
            req = build_request(url)
            data = json.loads(req.text)['objects']
            ava_sku_list = []
            for item in data:
                if item['available'] == True:
                    ava_sku_list.append(item['skuId'])
            return ava_sku_list
        except:
            continue
    raise NetWorkError
        

def parser_cn(res_text):
    res_text = res_text.replace('\r', '').replace('\n', '').replace(
        ' ', '').replace('\t', '').replace('\\u002F', '/').replace('：', ':')
    products_text = re.findall('"products":({.*?})},"intl":', res_text)[0]
    products = json.loads(products_text)
    product_id_list = []
    for key in products:
        product_id_list.append(products[key]['id'])
    try:
        ava_sku_list = get_available_skus(product_id_list)
    except Exception as e:
        print(current_time(), '[get_available_skus][request error]', e)
        return []
    result = []
    for key in products:
        product = products[key]
        item = {}
        try:
            item['color'] = product['colorDescription']
        except:
            item['color'] = ''
        try:
            item['style'] = product['styleColor']
        except:
            item['style'] = ''
        sku_info = []
        for sku_item in product['skus']:
            if sku_item['skuId'] in ava_sku_list:
                sku_info.append(sku_item['localizedSize'])
        item['sku_info'] = sku_info
        result.append(item)
    return result


def get_product_info(url):
    req = build_request(url)
    sku_info = []
    result = []
    if 'store.nike.com' in url:
        item = get_color_and_style(req.text)
        item['sku_info'] = []
        try:
            sku_info = parser_store(req.text)
            item['sku_info'] = sku_info
        except Exception as e:
            print(current_time(), '[parser_store][parser error]', e)
        result.append(item)
    if 'www.nike.com' in url:
        try:
            result = parser_cn(req.text)
        except Exception as e:
            print(current_time(), '[parser_cn][parser error]', e)
    return result


def crawl():
    result = []
    keys = ['title', 'subtitle', 'pdpUrl',
            'overriddenLocalPrice', 'localPrice']
    products = get_products()
    counter = 0
    for item in products:
        pdp_url = item['pdpUrl']
        base_info = []
        for key in keys:
            try:
                value = item[key]
                if value is None:
                    value = '-'
            except:
                value = '-'
            base_info.append(value)
        if 'store.nike.com' in pdp_url:
            result.append(base_info)
            continue
        try:
            products = get_product_info(pdp_url)
        except Exception as e:
            print(current_time(), '[get_product_info][error]', pdp_url, e)
            result.append(base_info)
            continue
        for product in products:
            line = base_info + [product['color'], product['style']]
            for sku_size in product['sku_info']:
                result.append(line + [sku_size])
            if len(product['sku_info']) == 0:
                result.append(base_info)
        counter += 1
        print(current_time(), '[get_product_info][OK]', pdp_url, counter)
    write_to_excel(result, 'files/' +
                   current_time().replace(':', '_') + '.xlsx')


crawl()
