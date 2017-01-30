import requests
from bs4 import BeautifulSoup
import time
import openpyxl
import re

kinds={ "Women's Fashion":'womens-fashion-accessories',
        "Men's Fashion":'mens-fashion-accessories',
        "Kids' & Toys":'kids-babies',
        "Sports & Recreation":'sports-fitness',
        "Bags & Luggage":'bags-luggage',
        "Beauty, Health & Skin Care":'beauty-health',
        "Home & Living":'home-decor',
        "Electronics & Appliances":'computers-electronics',
        "Books & Stationery":'books-stationer'}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    'Host':'www.westfield.com.au',
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_centre():
    html=requests.get('https://www.westfield.com.au/',headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find_all('a',{'class':'js-centre-name'})
    result=[]
    for a in table:
        item={}
        try:
            item['url']=a.get('href').replace('/','')
            item['title']=a.get('data-track-label').replace(' home','')
        except:
            continue
        result.append(item)
    return result

def get_products(centre,kind):
    page=1
    keys=['custom_productname','custom_productbrand','custom_productprice']
    f=open('temp.txt','w',encoding='utf-8')
    while True:
        try:
            html=requests.get('https://www.westfield.com.au/%s/products/%s?page=%s'%(centre,kind,page),headers=headers,timeout=30).text
        except:
            print(centre,kind,page,'failed')
            continue
        table=BeautifulSoup(html,'lxml').find_all('article',{'class':'new-tile--product'})
        if len(table)==0:
            break
        for item in table:
            product=[]
            try:
                a=item.find('a')
                data=a.get('data-custom-dimensions-on-click')
                for key in keys:
                    try:
                        value=re.findall('"%s": "(.*?)"'%key,data)[0]
                        product.append(value)
                    except:
                        product.append('')
                product.append('https://www.westfield.com.au'+a.get('href'))
                imgurl=item.find('img').get('data-src')
                if imgurl==None:
                    imgurl=item.find('img').get('data-srcset')
                product.append(imgurl)
            except:
                continue
            f.write(str(product)+'\n')
        print(centre,kind,page,'ok')
        page+=1
    f.close()

def get_description(url):
    html=requests.get(url,headers=headers,timeout=30).text
    text=BeautifulSoup(html,'lxml').find('div',{'class':'text-truncate'}).get_text()
    return text

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in open('result.txt','r',encoding='utf-8'):
        try:
            line=eval(line)
            sheet.append(line)
        except:
            continue
    excel.save('result.xlsx')

def westfield():
    shops=get_centre()
    for shop in shops:
        for kind in kinds:
            get_products(shop['url'],kinds[kind])
            count=1
            for line in open('temp.txt','r',encoding='utf-8'):
                item=eval(line)
                try:
                    des=get_description(item[-2])
                except:
                    des=''
                item=[shop['title'],kind]+item
                item.append(des)
                print(shop['title'],kind,count,'ok')
                count+=1
                f=open('result.txt','a',encoding='utf-8')
                f.write(str(item)+'\n')
                f.close()
    write_to_excel()
    
westfield()
