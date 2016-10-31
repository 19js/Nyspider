import requests
import json
import time
from bs4 import BeautifulSoup
import random

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}

def get_province():
    html=requests.get('http://ditu.amap.com/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&city=100000&geoobj=19.198221%7C11.793397%7C-172.051779%7C53.547635&keywords=%E5%B9%B2%E6%9E%9C',headers=headers).text
    data=json.loads(html)
    table=BeautifulSoup(data['html'],'lxml').find_all('div',{'class':'sug-province'})
    f=open('citys.txt','a')
    for item in table:
        try:
            province=item.find('b').get_text()
            citys=item.find_all('a',{'class':'citycode'})
            for city in citys:
                f.write(province+'|'+city.get_text()+'|'+city.get('adcode')+'\n')
        except:
            continue
    f.close()

def search(key,citycode):
    page=1
    result=[]
    while True:
        html=requests.get('http://ditu.amap.com/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum=%s&qii=true&cluster_state=5&need_utd=true&div=PC1000&addr_poi_merge=true&is_classify=true&city=%s&keywords=%s'%(page,citycode,key),headers=headers).text
        data=json.loads(html)['data'][0]['list']
        if data==[]:
            break
        for item in data:
            try:
                tel=item['templateData']['tel']
                address=item['address']
                name=item['name']
                result.append(name+'| '+address+' |'+tel)
            except:
                continue
        page+=1
        print(citycode,page)
        time.sleep(random.randint(2,8))
    return result

def main():
    for line in open('citys.txt','r'):
        line=line.replace('\n','')
        code=line.split('|')[-1]
        try:
            result=search('干果',code)
        except:
            failed=open('failed.txt','a')
            failed.write(line+'\n')
            failed.close()
            continue
        f=open('result.txt','a')
        for item in result:
            f.write(line+'|'+item+'\n')
        f.close()
        print(line)
main()
        