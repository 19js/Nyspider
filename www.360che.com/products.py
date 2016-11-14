import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import pymysql
import json

headers={
    'Host': 'product.m.360che.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

def load_mysql_setting():
    f=open('./mysql_setting.json','r',encoding='utf8')
    config=json.load(f)
    return config

def insert_into_mysql(result):
    config=load_mysql_setting()
    conn=pymysql.connect(**config)
    #conn=pymysql.connect(host=userdata['host'],user=userdata['user'],passwd=userdata['passwd'],db=userdata['db'],port=userdata['port'],charset='utf-8')
    cur=conn.cursor()
    try:
        cur.execute("create table if not exists products(name char(80),series char(80),brand char(80),销售情况 char(80),基本信息 TEXT,发动机 TEXT,货箱参数 TEXT,驾驶室参数 TEXT,变速箱 TEXT,轮胎 TEXT,制动器 TEXT,油箱 TEXT,底盘 TEXT,其它信息 TEXT)")
    except:
        pass
    keys=['brand','series','name','销售情况','基本信息', '发动机', '货箱参数', '驾驶室参数', '变速箱', '轮胎', '制动器', '油箱', '底盘','其它信息']
    for item in result:
        line=[]
        for key in keys:
            try:
                line.append(str(item[key]))
            except:
                line.append('')
        cur.execute('insert into products(brand,series,name,销售情况,基本信息, 发动机, 货箱参数, 驾驶室参数, 变速箱, 轮胎, 制动器, 油箱, 底盘,其它信息) values'+str(tuple(line)))
    conn.commit()
    cur.close()

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
            name=item.find('a').get_text().replace('\n','').replace('人气','')
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
            name=item.find('a').get_text().replace('\n','').replace('人气','')
            url=item.find('a').get('href').replace('_index','_param')
        except:
            continue
        products.append(['停售',name,url])
    return products

def product_infor(url):
    html=requests.get('http://product.m.360che.com/'+url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('table',id='datatable_main').find_all('tr')
    infor={}
    title=''
    for item in table:
        class_name=item.get('class')
        if class_name==['title']:
            title=item.get_text().replace('\n','')
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
    return infor

def main():
    brandlist=get_brandlist()
    keys=['brand','series','name','销售情况','基本信息', '发动机', '货箱参数', '驾驶室参数', '变速箱', '轮胎', '制动器', '油箱', '底盘','其它信息']
    for brand in brandlist:
        series=get_series(brand[1],brand[2])
        for item in series:
            products=get_products(item[1])
            result=[]
            for product in products:
                car={}
                for key in keys:
                    car[key]={}
                car['brand']=brand[0]
                car['series']=item[0]
                car['name']=product[1]
                car['销售情况']=product[0]
                try:
                    infor=product_infor(product[-1])
                except:
                    continue
                for key in infor:
                    try:
                        value=car[key]
                        car[key]=infor[key]
                    except:
                        car['其它信息'][key]=infor[key]
                result.append(car)
            print(item[0])
            insert_into_mysql(result)

main()
