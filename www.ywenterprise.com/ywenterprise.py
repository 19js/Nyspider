import requests
import openpyxl
from bs4 import BeautifulSoup
import time
import os
import json
import re
import random

requests.packages.urllib3.disable_warnings()

products_urls = [
    ['Office Items', 'Plastic Clip',
        'http://www.ywenterprise.com/products.php/parent_id-59/cat_id-88/Plastic+Clip.html'],
    ['Office Items', 'Ruler',
        'http://www.ywenterprise.com/products.php/parent_id-59/cat_id-90/Ruler.html'],
    ['Office Items', 'Stapler',
        'http://www.ywenterprise.com/products.php/parent_id-59/cat_id-91/Stapler.html'],
    ['Office Items', 'Paper clip dispenser',
        'http://www.ywenterprise.com/products.php/parent_id-59/cat_id-92/Paper+clip+dispenser.html'],
    ['Office Items', 'Name card holder,Pen and Memo holder & Mobile phon',
        'http://www.ywenterprise.com/products.php/parent_id-59/cat_id-38/Name+card+holder%2CPen+and+Memo+holder+%26+Mobile+phon.html'],
    ['Office Items', 'Recycle NoteBook,PP Notebook & Sticker Notebook',
        'http://www.ywenterprise.com/products.php/parent_id-59/cat_id-58/Recycle+NoteBook%2CPP+Notebook+%26+Sticker+Notebook.html'],
    ['Office Items', 'Budge Key Holder& Key Ring',
        'http://www.ywenterprise.com/products.php/parent_id-59/cat_id-80/Budge+Key+Holder%26+Key+Ring.html'],
    ['Office Items', 'Magnifier',
        'http://www.ywenterprise.com/products.php/parent_id-59/cat_id-40/Magnifier.html'],
    ['Office Items', 'Lanyard & Whistle',
        'http://www.ywenterprise.com/products.php/parent_id-59/cat_id-51/Lanyard+%26+Whistle.html'],
    ['Office Items', 'Ballpen,Laser pen & Highlight Pen',
        'http://www.ywenterprise.com/products.php/parent_id-59/cat_id-60/Ballpen%2CLaser+pen+%26+Highlight+Pen.html'],
    ['Travelling Sets & Houseware', 'Earbud',
        'http://www.ywenterprise.com/products.php/parent_id-68/cat_id-93/Earbud.html'],
    ['Travelling Sets & Houseware', 'Travelling Sets',
        'http://www.ywenterprise.com/products.php/parent_id-68/cat_id-82/Travelling+Sets.html'],
    ['Travelling Sets & Houseware', 'Back Cushion',
        'http://www.ywenterprise.com/products.php/parent_id-68/cat_id-86/Back+Cushion.html'],
    ['Travelling Sets & Houseware', 'Coin Bank,Coin Holder & Photo Holder',
        'http://www.ywenterprise.com/products.php/parent_id-68/cat_id-45/Coin+Bank%2CCoin+Holder+%26+Photo+Holder.html'],
    ['Travelling Sets & Houseware', 'Coffee Mug&Aluminum Bottle(Sports Bottle&Vacuum Fl',
     'http://www.ywenterprise.com/products.php/parent_id-68/cat_id-39/Coffee+Mug%26Aluminum+Bottle%28Sports+Bottle%26Vacuum+Fl.html'],
    ['Travelling Sets & Houseware', 'Neoprene Can Holder And Bottle Koozie',
        'http://www.ywenterprise.com/products.php/parent_id-68/cat_id-57/Neoprene+Can+Holder+And+Bottle+Koozie.html'],
    ['Travelling Sets & Houseware', 'Hair Brush, Mirror & Sewing Set',
        'http://www.ywenterprise.com/products.php/parent_id-68/cat_id-47/Hair+Brush%2C+Mirror+%26+Sewing+Set.html'],
    ['Travelling Sets & Houseware', 'Mobile Phone Charger',
        'http://www.ywenterprise.com/products.php/parent_id-68/cat_id-56/Mobile+Phone+Charger.html'],
    ['Travelling Sets & Houseware', 'Pill Box & Pill Cutter',
        'http://www.ywenterprise.com/products.php/parent_id-68/cat_id-61/Pill+Box+%26+Pill+Cutter.html'],
    ['Travelling Sets & Houseware', 'lives the daily necessities',
        'http://www.ywenterprise.com/products.php/parent_id-68/cat_id-76/lives+the+daily+necessities.html'],
    ['Travelling Sets & Houseware', 'Manicure Sets,Massage Sets and Hairdressing Sets',
        'http://www.ywenterprise.com/products.php/parent_id-68/cat_id-77/Manicure+Sets%2CMassage+Sets+and+Hairdressing+Sets.html'],
    ['Travelling Sets & Houseware', 'Recreation commidities',
        'http://www.ywenterprise.com/products.php/parent_id-68/cat_id-78/Recreation+commidities.html'],
    ['Bags', 'Bicycle bag',
        'http://www.ywenterprise.com/products.php/parent_id-72/cat_id-85/Bicycle+bag.html'],
    ['Bags', 'Shopping bag',
        'http://www.ywenterprise.com/products.php/parent_id-72/cat_id-71/Shopping+bag.html'],
    ['Bags', 'handbag', 'http://www.ywenterprise.com/products.php/parent_id-72/cat_id-73/handbag.html'],
    ['Bags', 'Backpack', 'http://www.ywenterprise.com/products.php/parent_id-72/cat_id-75/Backpack.html'],
    ['Tool sets', 'Table Bag Holder',
        'http://www.ywenterprise.com/products.php/parent_id-81/cat_id-87/Table+Bag+Holder.html'],
    ['Tool sets', 'Calculator',
        'http://www.ywenterprise.com/products.php/parent_id-81/cat_id-37/Calculator.html'],
    ['Tool sets', 'Bottle Opener & Wine Sets',
        'http://www.ywenterprise.com/products.php/parent_id-81/cat_id-41/Bottle+Opener+%26+Wine+Sets.html'],
    ['Tool sets', 'Carabiner And Compass',
        'http://www.ywenterprise.com/products.php/parent_id-81/cat_id-43/Carabiner+And+Compass.html'],
    ['Tool sets', 'CD Bags,CD Holder CD Cleaner & Mouse Pad',
        'http://www.ywenterprise.com/products.php/parent_id-81/cat_id-44/CD+Bags%2CCD+Holder+CD+Cleaner+%26+Mouse+Pad.html'],
    ['Tool sets', 'Ice Scraper & Tire Guage',
        'http://www.ywenterprise.com/products.php/parent_id-81/cat_id-48/Ice+Scraper+%26+Tire+Guage.html'],
    ['Tool sets', 'Knife & Scissors',
        'http://www.ywenterprise.com/products.php/parent_id-81/cat_id-50/Knife+%26+Scissors.html'],
    ['Tool sets', 'Laser Edge Water Level',
        'http://www.ywenterprise.com/products.php/parent_id-81/cat_id-52/Laser+Edge+Water+Level.html'],
    ['Tool sets', 'LED Torch,LED Light & LED Key Chain',
        'http://www.ywenterprise.com/products.php/parent_id-81/cat_id-53/LED+Torch%2CLED+Light+%26+LED+Key+Chain.html'],
    ['Tool sets', 'Letter Opener',
        'http://www.ywenterprise.com/products.php/parent_id-81/cat_id-54/Letter+Opener.html'],
    ['Tool sets', 'Mini Tools & Flash Light',
        'http://www.ywenterprise.com/products.php/parent_id-81/cat_id-55/Mini+Tools+%26+Flash+Light.html'],
    ['Tool sets', 'Tape Measure',
        'http://www.ywenterprise.com/products.php/parent_id-81/cat_id-65/Tape+Measure.html'],
    ['Tool sets', 'Kitchen Timer',
        'http://www.ywenterprise.com/products.php/parent_id-81/cat_id-67/Kitchen+Timer.html'],
    ['PU AND PVC STRESS ITEMS', '',
        'http://www.ywenterprise.com/products.php/parent_id-0/cat_id-63/PU+and+PVC+Stress+Items.html']
]


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
        f = open('temp/exists.json', 'r',encoding='utf-8')
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
    result = []
    for type_item in products_urls:
        page = 1
        base_url = type_item[-1].replace(type_item[-1].split('/')[-1],'')        
        while True:
            url=base_url+'page-%s'%(page)
            html = load_html(url)
            if html == None:
                continue
            table = BeautifulSoup(html, 'lxml').find_all('div', {'align': 'center'})
            if len(table)<=1:
                break
            for item in table[1:]:
                product_item = item.find('p',{'align':'center'})
                product_url=item.find('a').get('href')
                if product_url==None or  product_url in exists:
                    continue
                try:
                    product_name = product_url.split('/')[-1].replace('.html','')
                    product_img = product_item.find('img').get('src').replace('unx','und')
                except:
                    continue
                result.append(type_item+[product_name, product_url, product_img])
            try:
                print(type_item[:2],'[get_products][Page]', page, 'OK')
            except:
                pass
            page += 1
    return result

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
        image_name = product[-1].split('/')[-1]
        try:
            image_dir = product[-3].split('-')[0]
            try_mkdir(['images/' + image_dir])
        except:
            image_dir = 'default'
        img_path = 'images/%s/%s' % (image_dir, image_name)
        if download_img(product[-1], img_path):
            exists[product[-2]] = 1
            try:
                print(product[-3], 'OK')
            except:
                pass
            result.append(product + [image_name, img_path])
        else:
            continue
    try:
        f = open('temp/exists.json', 'w',encoding='utf-8')
        json.dump(exists, f)
    except:
        pass
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
    print("抓取完成")
    time.sleep(10000)
