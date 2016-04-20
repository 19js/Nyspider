import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/44.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def rooms(url):
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'listings-container'}).find_all('div',attrs={'class':'listing'})
    result=[]
    for item in table:
        price=item.find('div',attrs={'class':'price-amount-container'}).get_text()
        media=item.find('div',attrs={'class':'media'})
        title=media.find('h3').get_text()
        userurl=media.find('a').get('href')
        roomurl=media.find('h3').find('a').get('href')
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
            review=re.findall('')

        text=title+'||'+price+'||'+review+'||'+roomurl+'||'+userurl
rooms('https://www.airbnb.com/s/San+Francisco?page=3&s_tag=xSPAdV5c')
