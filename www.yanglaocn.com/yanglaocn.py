#coding:utf-8

import requests
from bs4 import BeautifulSoup
import json

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_urls():
    f=open('urls.txt','w',encoding='utf-8')
    page=1
    while True:
        html=requests.get('http://www.yanglaocn.com/yanglaoyuan/yly.php?&RgSelect=0531&BNSelect=1&BTSelect=1&PRSelect=1&NaSelect=1&skey=&page=%s'%page,headers=headers).text.encode('ISO-8859-1').decode('utf-8','ignore')
        page+=1
        table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'querywhere2'}).find_all('div',attrs={'class':'jiadiantucontext'})
        for item in table:
            a=item.find('a',attrs={'class':'ameth7'})
            text=a.get_text()+'||'+a.get('href')+'\n'
            f.write(text)
        print(page)
        if page==163:
            break
    f.close()

def get_infor(line):
    url=line.split('||')[-1]
    html=requests.get(url,headers=headers).text.encode('ISO-8859-1').decode('utf-8','ignore')
    soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'ylyxxLeft'})
    table=soup.find('div',id='BasicInformation').find('div',attrs={'class':'leftcontext'}).find_all('div',attrs={'class':'leftcontexttitleT'})
    lists=['成立时间：','床位数量：','机构性质：','机构类型：']
    for item in table:
        title=item.find('span').get_text()
        if  title in lists:
            line+='||'+item.get_text().replace(title,'').replace('\r','').replace('\n','').replace(' ','')
    table=soup.find('div',id='ContactUs').find('div',attrs={'class':'leftcontext'}).find_all('div',attrs={'class':'leftcontexttitle'})
    for item in table:
        title=item.find('span').get_text()
        if  title=='所在地区：':
            line+='||'+item.get_text().replace(title,'').replace('\r','').replace('\n','').replace(' ','')
            break
    return line

def get_place(line):
    keywords=line.split('||')[0]
    data=requests.get('http://api.map.baidu.com/place/v2/search?ak=%s&output=json&query=%s&page_size=50&page_num=%s&scope=1&region=山东'%('GcBSlhCEeemKzzHYT8KWeLeh',keywords,0)).text
    data=json.loads(data)['results']
    try:
        location=data[0]['location']
        line+='||'+str(location['lng'])+'||'+str(location['lat'])+'\n'
        return line
    except:
        return line+'\n'

def get_location(line):
    name=line.split('||')[0]
    html=requests.get('http://api.map.baidu.com/geocoder/v2/?ak=fh980b9Ga64S8bl8QblSC3kq&output=json&address=%s&city=山东'%(name)).text
    data=json.loads(html)
    if data['status']==0:
        location=data['result']['location']
        line+='||'+str(location['lng'])+'||'+str(location['lat'])+'\n'
    else:
        line+='\n'
    return line

def main():
    #get_urls()
    '''
    f=open('data.txt','w',encoding='utf-8')
    for line in open('urls.txt','r',encoding='utf-8').readlines():
        line=line.replace('\n','')
        line=get_infor(line)
        get_infor(line)
        return
        #f.write(line+'\n')
    f.close()
    f=open('results.txt','w')
    num=0
    for line in open('data.txt','r').readlines():
        line=line.replace('\n','')
        line=get_place(line)
        num+=1
        print(num)
        f.write(line)
    f.close()
    '''
    f=open('results.txt','w')
    num=0
    for line in open('data.txt','r').readlines():
        line=line.replace('\n','')
        line=get_location(line)
        num+=1
        print(num)
        f.write(line)
    f.close()

main()
