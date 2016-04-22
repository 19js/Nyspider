import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/44.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def infor(url):
    html=requests.get(url,headers=headers).text
    parser(html)

def parser(html):
    Verifiedlabels=['Email address','Facebook','LinkedIn','Offline ID']
    table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'page-container page-container-responsive row-space-top-4 row-space-8'})
    right=table.find('div',attrs={'class':'col-lg-3 col-md-4 hide-sm'})
    Verified=right.find('ul',attrs={'class':'list-unstyled'}).find_all('li')
    VerifiedList={}
    for li in Verified:
        text=li.get_text().replace('\r','').replace('\n','').replace('\t','')
        for key in Verifiedlabels:
            if key in text:
                VerifiedList[key]=text.replace(key,'').replace('  ','')
    AboutMeLabels=['School','Work','Languages']
    AboutMeList={}
    AboutMe=right.find_all('div',attrs={'class':'panel-body'})[-1]
    dt=AboutMe.find_all('dt')
    dd=AboutMe.find_all('dd')
    for index in range(len(dt)):
        if dt[index].get_text() in AboutMeLabels:
            AboutMeList[dt[index].get_text()]=dd[index].get_text().replace('  ','')
    left=table.find('div',attrs={'class':'col-lg-9 col-md-8 col-sm-12'})
    baseinfor={}
    top=left.find('div',attrs={'class':'row row-space-4'})
    name=top.find('h1').get_text().replace('  ','')
    location=top.find('a').get_text().replace('  ','')
    jointime=top.find('span',attrs={'class':'text-normal'}).get_text().replace('  ','')
    data_mystique_key=left.find('div',attrs={'data-mystique-key':'user_profile_badgesbundlejs'}).find_all('div',attrs={'class':'badge-container space-top-4'})
    ReviewsLabels=['Verified','Reference','Superhost']
    ReviewsList={}
    for item in data_mystique_key:
        for key in ReviewsLabels:
            if key in item.get('data-reactid'):
                ReviewsList[key]=item.get_text().replace('  ','')
    reviews=left.find('div',id='reviews').find('div',attrs={'class':['reviews_section','as_guest','row-space-top-3']}).find('div',attrs={'class':'reviews'}).find_all('div',attrs={'class':'row'})
    reviews_as_guest=len(reviews)/2
    baseinfor={}
    baseinfor['name']=
    print(VerifiedList,AboutMeList,ReviewsList)

infor('https://www.airbnb.com/users/show/2268502')
