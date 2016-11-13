import requests
from bs4 import BeautifulSoup
import openpyxl
import time

headers={
    'Host': 'product.m.360che.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

def get_brandlist():
    html=requests.get('http://product.m.360che.com/brandlist.html',headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'brands-model'}).find_all('li')
    brandlist=[]
    for item in table:
        try:
            name=item.find('figcaption').get_text().split('  ')[0]
            brandid=item.get('data-brandid')
            brandtype=item.get('data-brandtype')
            brandlist.append([name,brandid,brandtype])
        except:
            continue
    return brandlist

def get_series(brandid,brandtype):
    html=requests.get('http://product.m.360che.com/index.php?r=m/ajax/filter/index&option=series&id={}&brandtype={}'.format(brandid,brandtype),headers=headers).text.encode('iso-8859-1').decode('utf-8','ignore')
    table=BeautifulSoup(html,'lxml').find_all('a')
    series=[]
    for item in table:
        try:
            name=item.find('h4').get_text()
            url=item.get('href')
        except:
            continue
        series.append([name,url])
    return series

def get_products(url):
    html=requests.get('http://product.m.360che.com/'+url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('div',id='tab_content').find_all('div',{'class':'dealer-module-wrap'})
    products=[]
    items=table[0].find_all('li')
    for item in items:
        try:
            name=item.find('a').get_text()
            url=item.find('a').get('href').replace('_index','_param')
        except:
            continue
        products.append(['在售',name,url])
    try:
        items=table[1].find_all('li')
    except:
        items=[]
    for item in items:
        try:
            name=item.find('a').get_text()
            url=item.find('a').get('href').replace('_index','_param')
        except:
            continue
        products.append(['停售',name,url])
    return products

def product_infor(url):
    html=requests.get('http://product.m.360che.com/'+url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('table',id='datatable_main').find_all('tr')
    infor={}
    keys=[]
    title=''
    for item in table:
        class_name=item.get('class')
        if class_name==['title']:
            title=item.get_text().replace('\n','')
            keys.append(title)
        if class_name!=None:
            continue
        try:
            key=item.find('th').get_text()
        except:
            continue
        if '厂商指导' in key or '本地最低' in key:
            continue
        try:
            value=item.find('td').get_text().replace('\r','').replace('\n','').replace('\t','').replace(' ','')
        except:
            value=''
        try:
            infor[title][key]=value
        except:
            infor[title]={}
            infor[title][key]=value
    f=open('keys.txt','a')
    f.write(str(keys)+'\n')
    f.close()
    return infor

def main():
    brandlist=get_brandlist()
    for brand in brandlist:
        series=get_series(brand[1],brand[2])
        for item in series:
            products=get_products(item[1])
            for product in products:
                try:
                    infor=product_infor(product[-1])
                except:
                    print(product)
                print(brand[0],item[0],product[1])
                break
main()
