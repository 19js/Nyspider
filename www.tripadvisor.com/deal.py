#coding:utf-8

import os
from bs4 import BeautifulSoup
import re


def Deal():
    f=open('data.txt','w')
    for filename in os.listdir('page'):
        html=open('page/'+filename,'r').read()
        soup=BeautifulSoup(html,'lxml').find('div',id='REVIEWS').find_all('div',attrs={'class':'reviewSelector'})
        for item in soup:
            infor=item.find('div',attrs={'class':'member_info'})
            try:
                text=infor.find('div',attrs={'class':'username mo'}).get_text()+'||'+infor.find('div',attrs={'class':'memberOverlayLink'}).get('id')
            except:
                print(filename)
                continue
            try:
                location=infor.find('div',attrs={'class':'location'}).get_text()
            except:
                location='--'
            try:
                level=item.find('div',attrs={'class':'levelBadge'}).get('class')[-1]
            except:
                level='--'
            content=item.find('div',attrs={'class':'col2of2'}).find('div',attrs={'class':'wrap'})
            try:
                title=content.find('div',attrs={'class':'quote'}).find('a').get_text()
            except:
                title='--'
            try:
                rate=content.find('div',attrs={'class':'rating reviewItemInline'}).find('img').get('alt')
            except:
                rate='--'
            try:
                via=content.find('a',attrs={'class':'viaMobile sprite-grayPhone'}).get_text()
            except:
                via='--'
            text+='|| '+location+' ||'+level+'||'+title+'||'+rate+'||'+via
            text=text.replace('\r','').replace('\n','')
            f.write(text+'\n')
    f.close()

def Deal_data():
    f=open('result.txt','w')
    for line in open('re_data.txt','r'):
        line=line.replace('\n','')
        lists=line.split('||')
        lists[3]=lists[3].replace('lvl_','')
        lists[5]=lists[5].split('of')[0].replace(' ','')
        text='||'.join(lists)
        print(text)
        f.write(text+'\n')

    f.close()

def deal_to_txt():
    try:
        os.mkdir('hasDate')
        os.mkdir('nothasDate')
    except:
        pass
    has_file={'5':1,'4':1,'3':1,'2':1,'1':1}
    stars={'5':'Excellent','4':'Verygood','3':'Average','2':'Poor','1':'Terrible'}
    not_file={'5':1,'4':1,'3':1,'2':1,'1':1}
    for key in stars:
        try:
            os.mkdir('hasDate/'+stars[key])
            os.mkdir('nothasDate/'+stars[key])
        except:
            continue
    title=['Name:','Nationality:','Level:','Age & Gender:','Title:','Rating:','Mobile:','Visiting time:','Detailed review:']
    for line in open('result_NEW.txt','r',encoding='utf-16'):
        line=line.replace('\n','')
        lists=line.split('\t')
        if(lists[7]!='--'):
            star=lists[5]
            f=open('hasDate/%s/%s%s.txt'%(stars[star],stars[star],has_file[star]),'w')
            for i in range(len(lists)):
                f.write(title[i]+lists[i]+'\r\n')
            f.close()
            has_file[star]+=1
        else:
            star=lists[5]
            f=open('nothasDate/%s/%s%s.txt'%(stars[star],stars[star],not_file[star]),'w')
            for i in range(len(lists)):
                f.write(title[i]+lists[i]+'\r\n')
            f.close()
            not_file[star]+=1

deal_to_txt()
