#coding:utf-8

from bs4 import BeautifulSoup
import requests
import random
import  os

def get_headers():
    headers = {
        'Host':"www.autozi.com",
        "X-Forwarded-For":'%s.%s.%s.%s'%(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
        'Referer':"http://www.autozi.com/carBrandLetter/.html",
        'X-Requested-With':"XMLHttpRequest",
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    return headers

def get_image(url,name):
    headers = {
        "X-Forwarded-For":'%s.%s.%s.%s'%(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    try:
        content=requests.get(url,headers=headers).content
    except:
        return False
    with open('images/'+name,'wb') as img:
        img.write(content)
    return True

def get_infor():
    try:
        os.mkdir('images')
    except:
        print('--')
    f=open('products_url.txt','r')
    failed_f=open('failed.txt','a')
    data_f=open('itemdata.txt','a')
    carmodel_f=open('model.txt','a')
    count=0
    for line in f.readlines():
        count+=1
        line=line.replace('\n','').replace('\t','')
        url=line.split('||')[-1]
        try:
            html=requests.get(url,headers=get_headers()).text
        except:
            failed_f.write(line+'\n')
            continue
        table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'c-main'}).find('div',id='tab_pro_02').find_all('tr')
        text=line
        for tr in table:
            text+='|| '+tr.get_text().replace(' ','').replace('\r\n',' ').replace('\n',' ').replace('\t','')
        img_url=line.split('||')[5]
        name=str(count)+'.'+img_url.split('.')[-1]
        if(get_image(img_url, name)):
            text+='|| '+name
        Id=url.split('/')[-1].split('.')[0]
        model_infor=get_model(Id)
        carmodel_f.write(line+'||'+model_infor+'\n')
        data_f.write(text+'\n')
        print(count)

def get_model(Id):
    try:
        html=requests.get('http://www.autozi.com/goods/carModels.do?goodsId='+Id,headers=get_headers()).text
        table=BeautifulSoup(html,'lxml').find_all('li')
        text=''
        for li in table:
            name=li.find('h4').get_text()
            for a in li.find_all('a'):
                text+=name+'-'+a.get_text()+'---'
        return text
    except:
        return '-'

get_infor()
