from util import *
from bs4 import BeautifulSoup
import json
import time


def get_all_brand():
    url = 'https://apicar.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=jingxiaoshang&pagetype=masterbrand&objid=0&citycode=beijing%2F&cityid=201'
    req = build_request(url)
    result = re.findall('name:"(.*?)",url:"(.*?)"', req.text)
    f = open('./files/brand_list', 'a')
    for item in result:
        f.write(json.dumps(
            [item[0], 'https://dealer.bitauto.com'+item[1]], ensure_ascii=False)+'\n')
    f.close()


def get_all_province():
    for line in open('./files/brand_list', 'r'):
        brand_item = json.loads(line)
        req = build_request(brand_item[-1])
        try:
            city_select = BeautifulSoup(req.text, 'lxml').find(
                'ul', {'id': 'provCitySelect'}).find_all('a')
        except:
            print(brand_item, 'Fail')
            continue
        f = open('./files/city_list', 'a')
        for city in city_select:
            city_name = city.get_text()
            city_url = 'https://dealer.bitauto.com'+city.get('href')
            f.write(json.dumps(
                brand_item+[city_name, city_url], ensure_ascii=False)+'\n')
        f.close()
        print(brand_item)


def counter():
    result = {}
    for item in load_txt('./files/city_list.1'):
        num = re.findall('\((\d+)\)', str(item))[0]
        if item[0] in result:
            result[item[0]] += int(num)
        else:
            result[item[0]] = int(num)
    write_to_excel(result.items(), '实际数量.xlsx')


def get_city_dealer(url):
    page = 1
    first_list = []
    result = []
    exists = {}
    while True:
        try:
            req = build_request(url+'&page={}'.format(page))
            table = BeautifulSoup(req.text, 'lxml').find_all(
                'div', {'class': 'dealer-list'})
        except:
            continue
        dealer_list = []
        new_item = False
        for item in table:
            title = item.find('h6').find('a').get_text()
            try:
                brand = item.find('p', {'class': 'brand'}).get_text()
                brand = sub_str(brand)
            except:
                brand = ''
            try:
                span_list = item.find('p', {'class': 'add'}).find_all('span')
                address = ''
                for span in span_list:
                    title_value = span.get('title')
                    if title_value is not None:
                        address += title_value
            except:
                address = ''
            try:
                tel_id = item.find('p', {'class': 'tel'}).find(
                    'span', {'class': 'tel400atr'}).get('dealerid')
            except:
                tel_id = ''
            try:
                city_area = item.find_all('p', {'class': 'add'})[1].get_text()
                city_area = sub_str(city_area)
            except:
                city_area = ''
            line = [sub_str(title), brand, address, city_area, tel_id]
            key = ''.join(line)
            if key not in exists:
                new_item = True
            exists[key] = 1
            dealer_list.append(line)
        if dealer_list == first_list:
            break
        if not new_item:
            break
        if page == 1:
            first_list = dealer_list
        result += dealer_list
        page += 1
    return result


def crawl_dealer_info():
    for line in open('./files/city_list', 'r'):
        city_item = json.loads(line)
        try:
            result = get_city_dealer(city_item[-1])
        except:
            f = open('./files/city_list_fail', 'a')
            f.write(line)
            f.close()
            continue
        f = open('./files/city_list_result', 'a')
        for item in result:
            f.write(json.dumps(city_item+item, ensure_ascii=False)+'\n')
        f.close()
        print(current_time(), city_item[0], city_item[2], 'OK')


def get_tel_info(tel_ids):
    url = 'https://autocall.bitauto.com/eil/das2.ashx?userid={}&mediaid=10&source=bitauto'
    req = build_request(url.format(','.join(tel_ids)))
    result = re.findall('(\{.*?\})', req.text)
    f = open('./files/tel', 'a')
    for line in result:
        f.write(line+'\n')
    f.close()


def load_tel_ids():
    id_list = []
    for item in load_txt('./files/city_list_result'):
        id_list.append(item[-1])
        if len(id_list) < 50:
            continue
        yield id_list
        id_list = []
    yield id_list

def load_result():
    tels={}
    for item in load_txt('./files/tel'):
        tels[item['dealerId']]=item['tel']
    for item in load_txt('./files/city_list_result'):
        try:
            item.append(tels[item[-1]])
        except:
            print(item[-1])
            item.append('')
        yield item


def counter_num():
    result = {}
    for item in load_txt('./files/city_list_result'):
        if item[0] in result:
            result[item[0]] += 1
        else:
            result[item[0]] = 1
    write_to_excel(result.items(), '抓取数量.xlsx')

counter_num()
    

