#coding:utf-8

import requests
from bs4 import BeautifulSoup

def get_infor(name,x_id):
    headers = {
            'Host':"www.zhongchou.com",
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
    html=requests.get('http://www.zhongchou.com/deal-show/id-'+x_id,headers=headers,timeout=50).text.encode('ISO-8859-1').decode('utf-8','ignore')
    table=BeautifulSoup(html,'lxml').find('div',id='xqTabOBox').find('ul',id='xqTabNav_ul').find_all('li')
    jingzhan=table[1].find('b').get_text()
    comments=table[2].find('b').get_text()
    right_table=BeautifulSoup(html,'lxml').find('div',id='rightfix-ch').find('div',attrs={'class':'zcje_ItemBox'}).find('h3')
    price=right_table.find('b').get_text()
    per_num=right_table.get_text().replace('人已支持','').replace(price,'')
    table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'xqMainLeftBox'}).find('a',attrs={'class':'xqMainLeft_vedioA siteImgBox'})
    if table==None:
        video='No'
    else:
        video='Yes'
    pri=get_jiaoyi(x_id)
    text=name+'|'+x_id+'|'+jingzhan+'|'+comments+'|'+pri+'|'+video
    return text


def get_jiaoyi(x_id):
    headers = {
            'Host':"www.zhongchou.com",
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
    try:
        data=requests.get('http://www.zhongchou.com/deal-support_list?id=%s&page_size=100000&offset=0'%x_id,headers=headers,timeout=50).text
    except:
        return '--|--'
    data=eval(data)
    lists=data['data']['support_list']
    sup_lists=[]
    deal_lists={}
    for item in lists:
        if item['deal_num']=='1':
            sup_lists.append(item)
            deal_lists[item['deal_price']]=1
    for item in sup_lists:
        deal_lists[item['deal_price']]+=1
    lists=[]
    min_pr=10000000
    for key in deal_lists:
        if min_pr>int(key.replace(',','')):
            min_pr=int(key.replace(',',''))
    text=str(min_pr)+'|'+str(deal_lists[str(min_pr)])
    return text

def main():
    file_id=open('ids.txt','r')
    data_f=open('data.txt','a')
    num=1
    for line in file_id.readlines():
        lists=line.replace('\n','').split('|')
        try:
            text=get_infor(lists[0], lists[1])
        except:
            continue
        print(num)
        num+=1
        print(text)
        data_f.write(text+'\n')
    data_f.close()
    file_id.close()

main()
