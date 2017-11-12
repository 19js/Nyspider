import requests
import openpyxl
from bs4 import BeautifulSoup
import time
import os
import json
import re
import random

requests.packages.urllib3.disable_warnings()


def get_headers():
    headers = {
        "X-Forwarded-For": '%s.%s.%s.%s' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0"}
    return headers


def load_content(url):
    for i in range(5):
        try:
            content = requests.get(url, verify=False, timeout=20).content
            return content
        except:
            pass
    return None


def download_img(img_url, file_path):
    content = load_content(img_url)
    if content == None:
        return False
    with open(file_path, 'wb') as f:
        f.write(content)
    return True


def load_exists():
    try:
        f = open('temp/exists.json', 'r')
        data = json.load(f)
        return data
    except:
        return {}


def load_html(url):
    for i in range(5):
        try:
            html = requests.get(url, headers=get_headers(),
                                verify=False, timeout=20).text
            return html
        except:
            pass
    return None


def get_products():
    exists = load_exists()
    page = 1
    pre_table = []
    result = []
    while True:
        url = 'https://www.hambleside-merchandise.co.uk/shop/products.html?___store=default_hamble&p=%s' % (
            page)
        html = load_html(url)
        if html == None:
            continue
        table = BeautifulSoup(html, 'lxml').find(
            'div', {'class': 'category-products'}).find_all('li', {'class': 'item last'})
        if table == pre_table:
            break
        pre_table = table
        for item in table:
            product_url = item.find('a').get('href')
            if product_url in exists:
                continue
            try:
                product_name = item.find(
                    'h2', {'class': 'product-name'}).get_text()
                product_price = item.find(
                    'span', {'class': 'price'}).get_text()
            except:
                continue
            result.append([product_name, product_price, product_url])
        print('[get_products][Page]', page, 'OK')
        page += 1
    return result


def get_product_info(url):
    html = load_html(url)
    soup = BeautifulSoup(html, 'lxml').find('div', {'class': 'product-view'})
    des = soup.find(
        'div', {'class': 'box-collateral box-description'}).get_text()
    img_url = soup.find('img', id='image-main').get('src')
    return [des, img_url]


def try_mkdir(dirs):
    for dir in dirs:
        try:
            os.mkdir(dir)
        except:
            pass


def crawl():
    try_mkdir(['images', 'temp', 'result', 'images/default'])
    products = get_products()
    exists = load_exists()
    result = []
    for product in products:
        try:
            base_info = get_product_info(product[-1])
        except:
            continue
        item = product + base_info
        image_name = item[-1].split('/')[-1]
        try:
            image_dir = re.findall('-([a-zA-Z]+)', image_name)[0]
            try_mkdir(['images/' + image_dir])
        except:
            image_dir = 'default'
        img_path = 'images/%s/%s' % (image_dir, image_name)
        if download_img(base_info[-1], img_path):
            exists[product[-1]] = 1
            try:
                print(product[0], 'OK')
            except:
                pass
            result.append(item + [image_name, img_path])
        else:
            continue
    f = open('temp/exists.json', 'w')
    json.dump(exists, f)
    write_to_excel(result)


def write_to_excel(result):
    excel = openpyxl.Workbook(write_only=True)
    sheet = excel.create_sheet()
    for line in result:
        try:
            sheet.append(line)
        except:
            pass
    date_str = time.strftime('%Y_%m_%d', time.localtime())
    excel.save('result/%s.xlsx' % (date_str))


if __name__ == '__main__':
    crawl()
