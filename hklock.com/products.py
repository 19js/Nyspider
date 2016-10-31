import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def login():
    data={
    'username':'iwin',
    'password':'iwin123'
    }
    session=requests.session()
    session.post('http://store.hklock.com/usercheck.asp',data=data,headers=headers).text
    return session

def get_urls(html):
    table=BeautifulSoup(html,'lxml').find('ul',{'class':'prolist'}).find_all('li')
    result=[]
    for item in table:
        try:
            img='http://store.hklock.com/'+item.find('img').get('src')
            title=item.find('a').get('title')
            url='http://store.hklock.com/'+item.find('a').get('href')
            num=item.find('div',{'class':'p-num'}).get_text()
            result.append([title,num,url,img])
        except:
            continue
    return result

def get_img(imgurl,filename):
    if os.path.exists('images/'+filename):
        return
    content=requests.get(imgurl,headers=headers,timeout=30).content
    with open('images/'+filename,'wb') as img:
        img.write(content)

def get_category():
    html=requests.get('http://store.hklock.com/productcategory.html',headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('div',id='maindiv').find_all('div',{'class':'classitem'})
    urls=[]
    '''
    for dd in table:
        for a in dd.find_all('a'):
            try:
                title=a.get_text()
                url='http://store.hklock.com/'+a.get('href')
                urls.append([title,url])
            except:
                continue
    return urls
    '''
    for classitem in table[:-1]:
        for dt in classitem.find_all('dt'):
            for a in dt.find_all('a'):
                try:
                    title=a.get_text()
                    url='http://store.hklock.com/'+a.get('href')
                    urls.append([title,url])
                except:
                    continue
    for dd in table[-1].find_all('dd'):
        for a in dd.find_all('a'):
            try:
                title=a.get_text()
                url='http://store.hklock.com/'+a.get('href')
                urls.append([title,url])
            except:
                continue
    return urls

def get_price(url,session):
    html=session.get(url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('div',id='proright').find('table',id='jglist').find_all('tr')[-1]
    price=[]
    for item in table.find_all('td'):
        price.append(item.get_text())
    return price

def write_to_excel(result):
    try:
        os.mkdir('result')
    except:
        pass
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for item in result:
        sheet.append(item)
    timenow=time.strftime("%Y%m%d_%H%M%S")+'.xlsx'
    excel.save('result/'+timenow)

def main():
    try:
        urls=get_category()
    except:
        print('Get Category Failed')
        return
    try:
        os.mkdir('images')
    except:
        pass
    products=[]
    for item in urls:
        page=1
        while True:
            try:
                html=requests.get(item[1].replace('-1.html','-%s.html'%page),headers=headers,timeout=30).text
                result=get_urls(html)
            except:
                break
            if result==[]:
                break
            for product in result:
                products.append([item[0]]+product)
            print(item[0],page,'ok')
            page+=1
    session=login()
    result=[]
    timenow=time.strftime("%Y-%m-%d")
    for product in products:
        try:
            price=get_price(product[3],session)
        except:
            price=[]
        result.append([timenow]+product+price)
        try:
            get_img(product[4],product[2]+'.jpg')
        except:
            continue
        print(product[1],'ok')
    write_to_excel(result)

main()
