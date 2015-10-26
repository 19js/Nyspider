#coding:utf-8

from bs4 import BeautifulSoup
import requests
import xlwt3

def get_type_urls():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
    html=requests.get('http://product.kimiss.com/catalog/',headers=headers).text.encode('ISO-8859-1').decode('utf-8','ignore')
    tables=BeautifulSoup(html).find('div',attrs={'class':'f_c_list'}).find_all('div',attrs={'class':'f_c_div'})
    mantable=tables[2].find_all('dl')
    f=open('man.txt','w')
    for item in mantable:
        urls=[]
        for i in item.find('dd').find_all('span'):
            try:
                url=i.find('a').get('href')+'product-mostcomment-0-0-0-1.html'
                urls.append(url)
            except:
                continue
        infor={}
        infor[item.find('dt').get_text()]=urls
        f.write(str(infor)+'\n')
    mantable=tables[3].find_all('dl')
    f=open('baby.txt','w')
    for item in mantable:
        urls=[]
        for i in item.find('dd').find_all('span'):
            try:
                url=i.find('a').get('href')+'product-mostcomment-0-0-0-1.html'
                urls.append(url)
            except:
                continue
        infor={}
        infor[item.find('dt').get_text()]=urls
        f.write(str(infor)+'\n')

get_type_urls()
