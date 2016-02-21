#coding:utf-8

import requests
from bs4 import BeautifulSoup


headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}


def login(username,passwd):
    session=requests.session()
    data={
    'username':username,
    'password':passwd
    }
    session.post('http://www.chuanlaoda.cn/good/login.html',headers=headers,data=data)
    return session

def get_urls(session,page):
    header = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With':"XMLHttpRequest",
            'Content-Type':"application/x-www-form-urlencoded; charset=UTF-8",
            'Host':"www.chuanlaoda.cn",
            'Referer':"http://www.chuanlaoda.cn/good/shiplist.html",
            'Connection': 'keep-alive'}
    data={
    'page':page,
    'srcname':"",
    'src':"",
    'destname':"",
    'dest':"",
    'min':"",
    'max':"",
    'atime':""
    }
    html=session.post('http://www.chuanlaoda.cn/good/shiplist.html',data=data,headers=header).text#.encode('ISO-8859-1').decode('utf-8','ignore')
    table=BeautifulSoup(html,'lxml').find('div',attrs={'class':"listbox"}).find_all('dl')
    lists=[]
    for item in table[1:]:
        ship={}
        d3=item.find('dd',attrs={'class':'d3'})
        number=d3.get('n')
        ship['num']=number
        ship['title']=d3.find('span',attrs={'class':'info'}).get('title')
        ship['weight']=item.find('dd',attrs={'class':'d4'}).get_text()
        lists.append(ship)
    return lists

def infor(session,ship):
    num=ship['num']
    html=session.get('http://www.chuanlaoda.cn/good/ship/%s.html'%num,headers=headers).text
    soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'shipinfo'})
    line=soup.find('div',attrs={'class':'linebox'}).find_all('div',attrs={'class':'line'})[1].find_all('div')
    ship['date']=line[0].get_text()
    ship['from']=line[1].get_text().replace('\n','').replace('\t','')
    ship['to']=line[-1].get_text()
    img_url=soup.find('dd',attrs={'class':'uinfo'}).find('div',id='umobile').find('img').get('src')
    img=session.get(img_url,headers=headers).content
    ship['img']=img
    return ship

def img_ocr(img):
    phone=''
    return phone

def main():
    session=login('13291481459','111111')
    ships=get_urls(session, 1)
    for ship in ships:
        ship=infor(session, ship)
        phonenum=img_ocr(ship['img'])
        ship['phone']=phonenum
        break
    for ship in ships:


main()
