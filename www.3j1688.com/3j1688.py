import requests
from bs4 import BeautifulSoup
import time
import pymysql
import random
import json
import re

def load_mysql_setting():
    f=open('./mysql_setting.json','r',encoding='utf8')
    data=json.load(f)
    return data

def insert_into_mysql(result):
    userdata=load_mysql_setting()
    conn=pymysql.connect(host=userdata['host'],user=userdata['user'],passwd=userdata['passwd'],db=userdata['db'],port=userdata['port'],charset=userdata['charset'])
    cur=conn.cursor()
    where_keys=['bmatch','bmain','bumain','btime']
    update_keys=['buse', 'btype', 'bsrc','bstart','batt','bdateline']
    for item in result:
        where_cmd=''
        for key in where_keys:
            try:
                where_cmd+=key+'='+'"%s"'%item[key]+' and '
            except:
                continue
        update_cmd=''
        for key in update_keys:
            try:
                update_cmd+=key+'='+'"%s"'%item[key]+','
            except:
                continue
        row=cur.execute('update chat_direct set %s where %s'%(update_cmd[:-1],where_cmd[:-4]))
        if row ==0:
            line=[]
            for key in ['bmatch','bmain','bumain','btime','buse', 'btype', 'bsrc','bstart','batt','bdateline']:
                try:
                    line.append(item[key])
                except:
                    line.append('')
            cur.execute('insert into chat_direct(bmatch,bmain,bumain,btime,buse,btype,bsrc,bstart,batt,bdateline) values'+str(tuple(line)))
    conn.commit()
    cur.close()
    conn.close()
    
def get_headers():
    headers = {
        "X-Forwarded-For":'%s.%s.%s.%s'%(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
        'Host':"www.3j1688.com",
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    return headers

def login():
    f=open('login.json','r')
    data=json.load(f)
    session=requests.session()
    html=session.post('http://www.3j1688.com/member/index.html',data=data,headers=get_headers()).text
    return session

def get_phones(session):
    '''
    html=session.get('http://www.3j1688.com/goods/lj/3/bjd.html',headers=get_headers()).text.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
    table=re.findall('varsg={(.*?)}',html)[0].split(',')
    keys=[]
    for item in table:
        try:
            keys.append(item.split(':')[0])
        except:
            continue
    '''
    keys=['小米', '天语', '京凯达', '优思', '多美达', '福中福', '乐视', '华为', '荣耀', '苹果', '百立丰', '三星', '魅族', '大神', '酷派', '诺基亚', '联想', '中兴', '米多', 'Q2', '纽曼', '世纪天元', '爱我', '飞利浦', 'HTC', 'TCL', '倍斯特', '努比亚', '美图', '索尼', '微软', 'JIMI大可乐', '果果', '洪洋伟业', '摩托罗拉', '神舟', '大Q', '优它', '锤子', '青橙', '奇酷', '金星', '台电', '先科', '夏新', 'U8', '掌航', '"21克"', '小辣椒', '一加']
    phones=[]
    for key in keys:
        try:
            html=session.post('http://www.3j1688.com/goods/lj/bjdjsonByBrand.html',data={'brandName':key},headers=get_headers()).text
            data=json.loads(html)['data']
            for item in data:
                item['brand']=key
                if key=='荣耀':
                    item['brand']='华为'
                print(item)
                phones.append(item)
        except:
            continue
    return phones

def get_phone(item,session):
    html=session.get('http://www.3j1688.com/goods/detail/%s.html?s=bjd'%item['goodsNum'],headers=get_headers()).text
    soup=BeautifulSoup(html,'lxml').find('div',id='xq_mian')
    table=soup.find('div',{'class':'xq_main_02_let_03'}).find_all('div',{'class':'xq_main_02_let_02'})
    products=[]
    for div in table:
        try:
            tds=div.find('tr').find_all('td')
            phone_infor=[]
            for td in tds[2:6]:
                try:
                    phone_infor.append(td.get_text())
                except:
                    phone_infor.append('')
            price=div.find('h4').get_text().replace('\r','').replace('\n','').replace('\t','').replace(' ','').replace('/','')
            products.append({'infor':phone_infor,'price':price})
        except:
            continue
    des=str(soup.find('div',{'class':'goods_main_contents'}))
    item['des']=des
    item['products']=products
    return item

session=login()
get_phones(session)
'''
html=open('./template.html','r').read()
item=get_phone({'goodsNum': '875', 'isCollected': False, 'isNew': False, 'price': 2228, 'goodsName': '乐视 乐视Max 2 （6G+64GB）', 'isHot': False},session)
with open('html.html','w') as f:
    f.write(html.format(title=item['goodsName'],des=item['des']))
'''