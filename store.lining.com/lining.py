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


def build_request(url,data=None, headers=None, proxies=None):
    if headers is None:
        headers = get_headers()
    for i in range(5):
        try:
            if data is None:
                response = requests.get(
                    url, headers=headers, proxies=get_proxies_abuyun(), timeout=15)
            else:
                response = requests.post(
                    url,data=data, headers=headers, proxies=get_proxies_abuyun(), timeout=15)
            if response.status_code != 200:
                continue
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
    need_urls = [
        'https://store.lining.com/shop/goodsCate-sale,desc,{},15s15_122,15_122_m,15_122_l-0-0-15_122,15_122_m,15_122_l-0s0-0-0-min,max-0.html',
        'https://store.lining.com/shop/goodsCate-sale,desc,{},15s15_123,15_122_m,15_123_l-0-0-15_123,15_122_m,15_123_l-0s0-0-0-min,max-0.html',
        'https://store.lining.com/shop/goodsCate-sale,desc,{},16s16_126,16_126_m-0-0-16_126,16_126_m-0s0-0-0-min,max-0.html',
        'https://store.lining.com/shop/goodsCate-sale,desc,{},16s16_127,16_126_m-0-0-16_127,16_126_m-0s0-0-0-min,max-0.html',
        'https://store.lining.com/shop/goodsCate-sale,desc,{},17-0-0-17-0s0-0-0-min,max-0.html',
        'https://store.lining.com/shop/goodsCate-sale,desc,{},18-0-0-18-0s0-0-0-min,max-0.html'
    ]
    exists = {}
    result = []
    for base_url in need_urls:
        page = 1
        failed_times = 0
        while True:
            try:
                url = base_url.format(page)
                req = build_request(url)
                res_text = req.text.encode(
                    'iso-8859-1').decode('utf-8', 'ignore')
                table = BeautifulSoup(res_text, 'lxml').find(
                    'div', {'class': 'cate_search_content'})
                if '未搜到满足条件的商品' in str(table) or table is None:
                    break
            except Exception as e:
                print(current_time(), '[get_products][request error]', url, e)
                failed_times += 1
                if failed_times == 3:
                    break
                continue
            failed_times = 0
            items = table.find_all('div', {'class': 'slaveItem'})
            if len(items) == 0:
                break
            for item in items:
                try:
                    name = item.get('goodsname')
                    url = item.get('url')
                    if url in exists:
                        continue
                    exists[url] = 1
                    result.append([name, url])
                except:
                    continue
            print(current_time(), '[get_products]', 'Url', base_url.format(page), 'OK')
            page += 1
    return result

def get_goods_details(postID,sizeStr,product_mainID):
    data={
        'postID':postID,
        'sizeStr':sizeStr,
        'product_mainID':product_mainID
    }
    on_sale=[]
    goodsRank='100%'
    spreadPrice='￥0'
    for i in range(3):
        try:
            req=build_request('https://store.lining.com/ajax/goods_details.html',data=data)
            data=json.loads(req.text)
            if 'message' in data and data['message']=='ok':
                try:
                    goodsRank='{}%'.format(data['data']['goodsRank'])
                except:
                    pass
                try:
                    spreadPrice='￥{}'.format(data['data']['spreadPrice'])
                except:
                    pass
                on_sale=data['data']['onSale']
                break
        except:
            continue
    result=[]
    for key in on_sale:
        result.append(key)
    return result,goodsRank,spreadPrice
        


def get_product_info(url):
    req = build_request(url)
    res_text = req.text.encode(
                    'iso-8859-1').decode('utf-8', 'ignore')
    soup = BeautifulSoup(res_text, 'lxml').find(
        'div', {'class': 'product_detail_full_section'})
    pd_desc = soup.find('div', {'id': "pd_desc"})
    try:
        product_name = pd_desc.find('h1', {'id': 'product_name'}).get_text().replace('\n','')
    except:
        product_name = ''
    try:
        goods_promotion = pd_desc.find(
            'div', {'class': 'goods_promotion'}).get_text()
    except:
        goods_promotion = ''
    try:
        partNumber = pd_desc.find('span', {'id': 'partNumber'}).get_text()
    except:
        partNumber = ''
    try:
        listPrice = pd_desc.find('span', {'id': 'listPrice'}).get_text()
    except:
        listPrice = ''
    try:
        offerPrice = pd_desc.find('span', {'id': 'offerPrice'}).get_text()
    except:
        offerPrice = ''
    try:
        discount = pd_desc.find('span', {'id': 'discount'}).get_text()
    except:
        discount = ''
    choicearea = soup.find('div', {'id': 'choicearea'})
    try:
        color = choicearea.find(
            'li', {'class': 'thumbimgchecked'}).find('a').get('title')
    except:
        color = ''
    base_info=[product_name,url, goods_promotion, partNumber, listPrice, offerPrice, discount, color]
    base_info=[item.replace('\t','').replace('\n','').replace('\xa0','').replace(' ','') for item in base_info]
    try:
        html=res_text.replace('\r','').replace('\n','').replace(' ','').replace('\t','')
        postID=re.findall('''postID:['](.*?)['],''',html)[-1]
        sizeStr=re.findall('''sizeStr:['"](.*?)['"],''',html)[0]
        product_mainID=re.findall('''product_mainID:['"](.*?)['"],''',html)[0]
        size_list,goodsRank,spreadPrice=get_goods_details(postID,sizeStr,product_mainID)
    except:
        size_list=[]
        goodsRank=None
        spreadPrice=None
    if goodsRank is not None and spreadPrice is not None:
        base_info[-2]='折扣:{} ({})'.format(goodsRank,spreadPrice)
    return {
        'base_info': base_info,
        'size_list':size_list
    }


class LiningProduct(threading.Thread):
    def __init__(self, base_info):
        super(LiningProduct, self).__init__()
        self.base_info = base_info
        self.pdp_url = self.base_info[-1]

    def run(self):
        self.lines=[]
        try:
            self.product = get_product_info(self.pdp_url)
        except Exception as e:
            print(current_time(),
                  '[get_product_info][error]', self.pdp_url, e)
            return
        base_info=self.product['base_info']
        size_list=self.product['size_list']
        if len(size_list)==0:
            self.lines=[base_info]
        else:
            for size in size_list:
                self.lines.append(base_info+[size])
            
        


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
            task = LiningProduct(item)
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
                   current_time().replace(':', '_')+'_lining' + '.xlsx')


crawl()

