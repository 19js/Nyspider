#coding:utf-8

import requests
import json

def get_top(page):
    html=requests.get('http://api.kanzhihu.com/topuser/follower/%s/50'%page).text
    data=json.loads(html)['topuser']
    return data

def main():
    f=open('persons.txt','a',encoding='utf-8')
    page=1
    while True:
        data=get_top(page)
        for item in data:
            text=item['name']+'||'+item['id']+'||'+str(item['follower'])+'||'+item['hash']
            f.write(text+'\n')
        print(page)
        page+=1
        if(page==20):
            break
    f.close()

def followee():
    f=open('data.txt','a',encoding='utf-8')
    for line in open('persons.txt','r').readlines():
        line=line.replace('\n','')
        print(line)
        data=requests.get('http://api.kanzhihu.com/userdetail2/'+line.split('||')[-1]).text
        data=json.loads(data)
        line=line+'|| '+str(data['signature'])+'|| '+str(data['description'])+'|| '
        detail=data['detail']
        line=line+str(detail['ask'])+'|| '+str(detail['answer'])+'|| '+str(detail['post'])+'|| '+str(detail['agree'])+'|| '+str(detail['thanks'])+'|| '+str(detail['fav'])+'||'+str(detail['logs'])
        f.write(line.replace('\r','').replace('\n','')+'\n')

followee()
