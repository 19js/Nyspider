import requests
from bs4 import BeautifulSoup
import time
import json
import re
import csv

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

#获取动漫信息
def anime_info(url):
    html=requests.get(url,headers=headers,timeout=30).text
    html=ILLEGAL_CHARACTERS_RE.sub(r'', html)
    soup=BeautifulSoup(html,'html.parser').find('div',{'class':'info-content'})

    #标题
    title=soup.find('h1',{'class':'info-title'}).get_text()
    #类型
    info_style=soup.find('div',{'class':'b-head'}).find_all('span',{'class':'info-style-item'})
    styles=[]
    for item in info_style:
        styles.append(item.get_text())

    #播放数，追番人数，弹幕数
    info_count=soup.find('div',{'class':'info-count'})
    play_count=info_count.find('span',{'class':'info-count-item-play'}).find('em').get_text()
    fans=info_count.find('span',{'class':'info-count-item-fans'}).find('em').get_text()
    review_count=info_count.find('span',{'class':'info-count-item-review'}).find('em').get_text()

    #更新日期
    info_update=soup.find('div',{'class':'info-update'}).find_all('span')
    date=info_update[0].get_text()
    statue=info_update[1].get_text().split(',')

    #声优
    info_cv=soup.find('div',{'class':'info-cv'}).find_all('span',{'class':'info-cv-item'})
    cv=[]
    for item in info_cv:
        line=item.get_text().split('、')
        for i in line:
            if i.replace(' ','')=='':
                continue
            cv.append(i)
    #描述
    des=soup.find('div',{'class':'info-desc'}).get_text().replace('\r','').replace('\n','')

    result=[title,styles,play_count,fans,review_count,date]+statue+[des,cv]
    return result

#抓取所有动漫的链接
def get_anime_urls():
    page=1
    urls=[]
    while True:
        url='http://bangumi.bilibili.com/web_api/season/index_global?page=%s&page_size=20&version=0&is_finish=0&start_year=0&tag_id=&index_type=1&index_sort=0&quarter=0'%page
        try:
            html=requests.get(url,headers=headers,timeout=30).text
        except:
            continue
        items=json.loads(html)['result']['list']
        if len(items)==0:
            break
        for item in items:
            urls.append(item['url'])
        print("urls page %s ok"%page)
        page+=1
    return urls


#写入Excel
def write_to_csv(result):
    with open('result.csv', 'w', newline='',encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for line in result:
            spamwriter.writerow(line)

#解析获取的信息，将声优和类型转为BOOL型
def parser_temp():
    lines=[]
    cv_dict={}
    cv_index=0
    cvs=[]
    styles_dict={}
    style_index=0
    styles=[]
    for line in open('./temp.txt','r',encoding='utf-8'):
        line=line.replace('\\r','').replace('\\n','')
        line=eval(line)
        lines.append(line)
        for cv in line[-1]:
            if cv in cv_dict:
                continue
            cv_dict[cv]=cv_index
            cvs.append(cv)
            cv_index+=1
        for style in line[1]:
            if style in styles_dict:
                continue
            styles_dict[style]=style_index
            styles.append(style)
            style_index+=1
    result=[]
    result.append(['title','styles','play_count','fans','review_count','date','是否完结','话数','des','cv']+styles+cvs)

    for line in lines:
        style_info=['F']*style_index
        cv_info=['F']*cv_index

        for style in line[1]:
            style_info[styles_dict[style]]='T'

        for cv in line[-1]:
            cv_info[cv_dict[cv]]='T'

        line[1]=','.join(line[1])
        line[-1]=','.join(line[-1])
        result.append(line+style_info+cv_info)
    write_to_csv(result)

def bangumi():
    urls=get_anime_urls()
    for url in urls:
        try:
            line=anime_info(url)
        except:
            failed=open('failed.txt','a',encoding='utf-8')
            failed.write(url+'\n')
            failed.close()
            print(url,'failed')
            continue
        f=open('temp.txt','a',encoding='utf-8')
        f.write(str(line)+'\n')
        f.close()
        try:
            print(line[0],'ok')
        except:
            continue

bangumi()
parser_temp()
