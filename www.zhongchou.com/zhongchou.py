#coding:utf-8

import requests
from bs4 import BeautifulSoup
import logging
import time
import json

headers = {
        'Host':"www.zhongchou.com",
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def get_projects():
    page=1
    pre=[]
    while True:
        try:
            html=requests.get('http://www.zhongchou.com/browse/p'+str(page),headers=headers).text.encode('ISO-8859-1').decode('utf-8','ignore')
            table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'sousuoListBox clearfix'}).find_all('div',attrs={'class':'ssCardItem'})
        except Exception as e:
            print('Error Page ',page,logging.exception(e))
            continue
        if table==pre:
            break
        pre=table
        f=open('projects.txt','a')
        for item in table:
            a=item.find('h3').find('a')
            title=a.get('title')
            project_id=a.get('href').replace('http://www.zhongchou.com/deal-show/id-','')
            f.write(str([title,project_id])+'\n')
        f.close()
        print(page,'OK')
        page+=1
        time.sleep(0.5)

def get_project_date(project_id):
    html=requests.get('http://www.zhongchou.com/deal-march_list?id={}&offset=0&page_size=100'.format(project_id),headers=headers,timeout=30).text
    data=json.loads(html)['data']['march_list']
    date=data[-1]['create_time']
    return date

def get_project_info(project_id):
    html=requests.get('http://www.zhongchou.com/deal-show/id-'+project_id,headers=headers,timeout=50).text.encode('ISO-8859-1').decode('utf-8','ignore')
    soup=BeautifulSoup(html,'lxml')
    table=soup.find('div',id='xqTabOBox').find('ul',id='xqTabNav_ul').find_all('li')
    process_num=table[1].find('b').get_text().replace('\n','')
    comments_num=table[2].find('b').get_text().replace('\n','')
    video=soup.find('div',attrs={'class':'xqMainLeftBox'}).find('a',attrs={'class':'xqMainLeft_vedioA siteImgBox'})
    if video==None:
        has_video='No'
    else:
        has_video='Yes'
    min_price_and_count=get_min_price_and_count(project_id)

    table=soup.find('div',attrs={'class':'mainIn02Box'})
    spans=table.find('div',attrs={'class':'jlxqTitleText siteIlB_box'}).find_all('span')
    project_type=spans[0].get_text().replace('\n','').replace('\n','')
    project_area=spans[1].get_text().replace('\n','')

    right_box=table.find('div',attrs={'class':'xqDetailBox'})
    divs=right_box.find('div',attrs={'class':"xqDetailDataBox"}).find_all('div')
    suport_num=divs[0].get_text().replace('\n','')
    amount=divs[1].get_text().replace('\n','')

    su_table=right_box.find('div',attrs={'class':'xqRatioOuterBox'})
    rate=su_table.find('p').get_text().replace('\n','')
    target_amount=su_table.find('b').get_text().replace('\n','')
    su_table=right_box.find('div',attrs={'class':'xqDetailLeft siteImgBox'}).find('a',{'class':'deal_detail_like'})
    share_num=su_table.get_text().replace('\n','')

    zxjzBox=soup.find_all('div',{'class':'zxjz_NavItem'})
    print(zxjzBox)
    return [process_num,comments_num,has_video]+min_price_and_count+[project_type,project_area,suport_num,amount,target_amount,rate,share_num]

def get_min_price_and_count(project_id):
    try:
        data=requests.get('http://www.zhongchou.com/deal-support_list?id=%s&page_size=100000&offset=0'%project_id,headers=headers,timeout=50).text
        data=eval(data)
        lists=data['data']['support_list']
    except:
        return ['-','-']
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
    return [min_pr,deal_lists[str(min_pr)]]

def zhongchou():
    #get_projects()
    for line in open('./projects.txt','r'):
        line=eval(line)
        try:
            date=get_project_date(line[-1])
        except:
            date='-'
        try:
            info=get_project_info(line[-1])
        except Exception as e:
            print(line,'Error' e)
            failed=open('failed.txt','a')
            failed.write(str(line)+'\n')
            failed.close()
            continue
        f=open('result.txt','a')
        f.write(str(line+[date]+info)+'\n')
        f.close()
zhongchou()
