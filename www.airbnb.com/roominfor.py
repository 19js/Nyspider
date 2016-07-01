import requests
from bs4 import BeautifulSoup
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/44.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}


def roominfor(url):
    html=requests.get(url,headers=headers,timeout=50).text
    result=parser(html)
    return result

def parser(html):
    soup=BeautifulSoup(html,'lxml').find('div',id='room')
    try:
        wishlist=soup.find('div',attrs={'class':'wishlist-wrapper hide-sm'}).find('div').get('title')
    except:
        wishlist='--'
    top=soup.find('div',attrs={'class':'summary-component'})
    title=top.find('h1').get_text()
    location=top.find('div',id='display-address').get('data-location')
    Room_Guest_Bed_labels=['room','Guests','Bed']
    Room_Guest_BedList={}
    toplist=top.find_all('div',attrs={'class':'col-sm-3'})
    for item in toplist:
        for key in Room_Guest_Bed_labels:
            if key in item.get_text():
                Room_Guest_BedList[key]=item.get_text()
    priceLabels=['Extra people','Cleaning Fee','Weekly discount','Monthly discount','Cancellation']
    priceList={}
    center=soup.find_all('div',attrs={'class':'col-md-6'})
    for item in center:
        for div in item.find_all('div'):
            for key in priceLabels:
                if key in div.get_text():
                    priceList[key]=div.get_text()
    starlabels=['Accuracy','Communication','Cleanliness','Location','Check In','Value']
    starList={}
    stardiv=soup.find('div',attrs={'class':'review-wrapper'}).find_all('div',attrs={'class':'col-lg-6'})
    for item in stardiv:
        for div in item.find_all('div',attrs={'class':'pull-right'}):
            for key in starlabels:
                if key in div.get('data-reactid'):
                    starList[key]=div.find('div',attrs={'class':'star-rating'}).get('content')
    try:
        hostprofile=soup.find('div',id='host-profile').get_text()
    except:
        hostprofile='--'
    result=title+'||'+location+'||'+wishlist
    for key in Room_Guest_Bed_labels:
        try:
            result+='||'+Room_Guest_BedList[key]
        except:
            result+='||--'
    for key in priceLabels:
        try:
            result+='||'+priceList[key]
        except:
            result+='||--'
    for key in starlabels:
        try:
            result+='||'+starList[key]
        except:
            result+='||--'
    result+='||'+hostprofile
    return result

def main():
    userfailed=open('roomfailed.txt','a',encoding='utf-8')
    userdata=open('roomdata.txt','a',encoding='utf-8')
    for line in open('urls.txt','r',encoding='utf-8'):
        line=line.replace('\n','')
        url='https://www.airbnb.com'+line.split('||')[-2]
        try:
            result=roominfor(url)
        except:
            userfailed.write(line+'\n')
            time.sleep(200)
            continue
        userdata.write(line+'||'+result.replace('\n','')+'\n')
        print(line,'--ok')
        time.sleep(10)
    userdata.close()
    userfailed.close()

main()
