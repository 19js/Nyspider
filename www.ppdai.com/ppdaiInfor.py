#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def get_person(Id):
    try:
        html=requests.get('http://www.ppdai.com/list/%s'%Id,headers=headers,timeout=50).text
        soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'newLendDetailInfoLeft'})
        text=soup.find('a',attrs={'class':'username'}).get_text()+'|'+soup.find('span',attrs={'class':'bidinfo'}).get_text()+'|'+soup.find('a').get('href')
        return text
    except:
        return False

def PersonInfor(text):
    rel='实名认证：|身份认证\(10分\)|视频认证\(10分\)|学历认证\(5分\)|手机认证\(10分\)|网上银行充值认证\(3分\)|邀请朋友评价\（5分\）\[已停用\]|【逾期未还清用户无法正常发布列表】|\[非实时更新\]|\(1分/次,每个月最多加一分\)|\(-2分/次\)|\(非实时\)| '
    try:
        html=requests.get(text.split('|')[-1],headers=headers,timeout=50).text.encode('ISO-8859-1').decode('utf-8','ignore')
    except:
        return False
    try:
        soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'user_homepage_nav clearfix'})
        left=soup.find('div',attrs={'class':'my-f-left left_user_nav  fl'}).find('ul').find_all('li')
        userinfor=text
        lists=[]
        for item in left[1].find_all('p'):
            userinfor+='|'+item.get_text().replace(' ','').replace('\r','').replace('\n','')
        for item in left[2].find_all('p'):
            userinfor+='|'+item.get_text().replace(' ','').replace('\r','').replace('\n','')
        infor=soup.find('table',attrs={'class':'lendegreetab mb5'}).find_all('tr')
        for tr in infor:
            userinfor+='|'+tr.get_text().replace('\r','').replace('\n','')
        userinfor+='|'+soup.find('div',attrs={'class':'borrowlevelalt_nav'}).find('p').get_text().replace('\r','').replace('\n','')
        userinfor=re.sub(rel,'',userinfor)
        right=soup.find('div',id='memberinfocontent').find('div',id='div1').find_all('li')
        for item in right:
            text=biao_deal(item)
            lists.append(userinfor+text)
        return lists
    except:
        return False

def biao_deal(item):
    soup=item.find('div',attrs={'class':'borrow_list'}).find('table').find_all('td')
    text=''
    for td in soup:
        text+='|'+td.get_text().replace(' ','').replace('\r\n','').replace('\n','')
    return text

def person():
    startId=8643097
    endId=8500000
    f=open('person.txt','w',encoding='utf-8')
    while endId<startId:
        text=get_person(endId)
        endId+=1
        if text!=False:
            f.write(text+'\n')
            print(endId)
        else:
            continue
    f.close()

def Infor():
    f=open('data.txt','w',encoding='utf-8')
    for text in open('person.txt','r').readlines():
        text=text.replace('\n','')
        lists=PersonInfor(text)
        if lists!=False:
            for line in lists:
                f.write(line+'\n')
        print(text+'---OK')
    f.close()

def main():
    person()
    Infor()

main()
