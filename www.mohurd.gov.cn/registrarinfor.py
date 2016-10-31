import requests
from bs4 import BeautifulSoup
import re

headers = {
    'Host':"210.12.219.18",
    'X-Requested-With':"XMLHttpRequest",
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/44.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer':"http://210.12.219.18/jianguanfabuweb/companies.html",
    'Cookie':"ASP.NET_SessionId=evkmapz1ljljsqh54siborwj",
    'Connection': 'keep-alive'}

def get_infor(item):
    url='http://210.12.219.18/jianguanfabuweb/'+item['url']
    html=requests.get(url,headers=headers,timeout=30).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'content'})
    basic=soup.find('table',{'class':'engineer_basic_infor_table'}).get_text().replace('\r','').replace('\n','').replace(' ','')
    basic_re='姓名：(.*?)民族：(.*?)性别：(.*?)手.*?学历：(.*?)学位'
    basicinfor=re.findall(basic_re,basic)[0]
    item['姓名']=basicinfor[0]
    item['民族']=basicinfor[1]
    item['性别']=basicinfor[2]
    item['学历']=basicinfor[3]
    zhengshu=soup.find_all('div',{'class':'zhengshu'})
    for div in zhengshu:
        header=div.find('div',{'class':'zhengshu_head'}).get_text()
        profess=div.find('table').find_all('td')[-1].get_text().split(',')
        item[header]=profess
    return item


def main():
    f=open('result.txt','a')
    count=0
    for line in open('person.txt','r').readlines():
        count+=1
        person=eval(line.replace('\n',''))
        try:
            item=get_infor(person)
        except:
            failed=open('person_failed.txt','a')
            failed.write(line)
            failed.close()
            print(person['name'],'failed')
            continue
        print(count)
        f.write(str(item)+'\n')
    f.close()

main()
