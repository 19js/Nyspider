import json
import re
import time
from bs4 import BeautifulSoup
import requests
import openpyxl
import random
import os

try:
    os.mkdir('files')
except:
    pass


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


def build_request(url, headers=None, is_proxies=True):
    if headers is None:
        headers = get_headers()
    for i in range(5):
        try:
            if is_proxies:
                response = requests.get(
                    url, headers=headers, proxies=get_proxies_abuyun(), timeout=15)
            else:
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


def get_hourse_list():
    url = 'https://gz.lianjia.com/ershoufang/pg{}/'
    page = 1
    while page <= 100:
        try:
            req = build_request(url.format(page))
            table = BeautifulSoup(req.text, 'lxml').find(
                'ul', {'class': 'sellListContent'}).find_all('li')
        except:
            continue
        f = open('./files/urls.txt', 'a')
        for item in table:
            title = item.find('div', {'class': 'title'}).get_text()
            hourse_url = item.find('a').get('href')
            address = item.find(
                'div', {'class': 'houseInfo'}).get_text().split('|')[0]
            try:
                text=item.find('div',{'class':'positionInfo'}).get_text()
                build_year=re.findall('(\d+)年',text)[0]
            except:
                build_year=''
            total_price = item.find('div', {'class': 'totalPrice'}).get_text()
            unit_price = item.find('div', {'class': 'unitPrice'}).get_text()
            f.write(json.dumps(
                [title, hourse_url, address, total_price, unit_price,build_year])+'\n')
        f.close()
        print(page, 'OK')
        page += 1


def get_hourse_detail(url):
    req = build_request(url)
    soup = BeautifulSoup(req.text, 'lxml').find('div', {'class': 'introContent'}).find(
        'div', {'class': 'content'}).find_all('li')
    result = {}
    for li in soup:
        key = li.find('span').get_text()
        value = li.get_text().replace(key, '')
        if '所在楼层' in key:
            try:
                floor_num = re.findall('共(\d+)层', value)[0]
            except:
                floor_num = ''
            result['floor_num'] = floor_num
        result[key] = value
    return result


def crawl():
    for line in open('./files/urls.txt', 'r'):
        item = json.loads(line)
        try:
            info = get_hourse_detail(item[1])
        except:
            f = open('./files/failed.txt', 'a')
            f.write(line)
            f.close()
            continue
        f = open('./files/ershoufang.txt', 'a')
        f.write(json.dumps({'base_info': item, 'detail': info})+'\n')
        f.close()
        print(item[0], item[1], 'OK')


def get_location(address, city):
    try:
        url = 'http://api.map.baidu.com/place/v2/search?query=%s&region=%s&city_limit=true&output=json&ak=fh980b9Ga64S8bl8QblSC3kq' % (
        address, city)
        req=build_request(url,is_proxies=False)
        html = req.text
        data = json.loads(html)['results'][0]['location']
        lng = data['lng']
        lat = data['lat']
    except:
        return ['','']
    return [lng,lat]


def load_from_txt():
    keys=['所在楼层','floor_num','建筑面积','套内面积','装修情况','房屋朝向','建筑类型','配备电梯','房屋户型']
    yield ['title','url','小区','价格','单价','建筑年代','经度','纬度']+keys
    for line in open('./files/ershoufang.txt','r'):
        item=json.loads(line)
        values=item['base_info']
        location=get_location(values[2].replace(' ',''),'广州')
        values+=location
        for key in keys:
            try:
                values.append(item['detail'][key])
                if key=='所在楼层':
                    if '高楼' in values[-1]:
                        values[-1]='0.5'
                    if '中楼' in values[-1]:
                        values[-1]='0'
                    if '低楼' in values[-1]:
                        values[-1]='1'
            except:
                values.append('')
        yield values
        print(values[2],location)

get_hourse_list()
crawl()
write_to_excel(load_from_txt(),'广州二手房信息.xlsx')