import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/44.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def rooms(url):
    html=requests.get(url,headers=headers).text
    try:
        table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'listings-container'}).find_all('div',attrs={'class':'listing'})
    except:
        return False
    result=[]
    for item in table:
        try:
            price=item.find('div',attrs={'class':'price-amount-container'}).get_text()
        except:
            price='--'
        try:
            media=item.find('div',attrs={'class':'media'})
            title=media.find('h3').get_text()
            userurl=media.find('a').get('href')
            roomurl=media.find('h3').find('a').get('href')
        except:
            continue
        a=media.find('a',attrs={'class':'text-normal link-reset'})
        try:
            rating=a.find('div',attrs={'class':'star-rating'}).find('div').find_all('i')
            star=len(rating)
            clases=[]
            for i in rating:
                clases+=i.get('class')
            if 'icon-star-half' in clases:
                star=star-0.5
        except:
            star='--'
        try:
            review=a.get_text().replace('\r','').replace('\n','').replace(' ','')
            review=re.findall('(\d+)reviews',review)[0]
        except:
            review='--'
        text=title+'||'+price+'||'+review+'||'+str(star)+'||'+roomurl+'||'+userurl
        result.append(text.replace('\r','').replace('\n','').replace(' ',''))
    return result

def getrooms():
    citys="Chicago,Vancouver,Montreal,Portland,Philadelphia,Denver,Austin,D.C.,New Orleans,Phoenix,San Diego,Nashville,Paris,Berlin,Rome,Amsterdam,Barcelona,Copenhagen,Prague,Budapest,Stockholm,Florence,Edinburgh,Istanbul,Sydney,Melbourne,Cape Town,Beijing,Shanghai,Tokyo"
    failed=open('failed.txt','a',encoding='utf-8')
    for city in citys.split(','):
        print(city)
        url_f=open('urls.txt','a',encoding='utf-8')
        url='https://www.airbnb.com/s/'+city.replace(' ','+').replace('.','%252E')
        page=1
        pre=[]
        while True:
            result=rooms(url+'?ss_id=v5im73ob&page=%s'%page)
            if result==pre:
                break
            pre=result
            if result==False:
                failed.write(city+'--'+str(page))
                break
            for item in result:
                url_f.write(city+'||'+item+'\n')
            print(city,'--',page)
            page+=1
            if(page==18):
                break
        url_f.close()
    url_f.close()
    failed.close()

getrooms()
