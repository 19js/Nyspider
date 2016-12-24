import requests
from bs4 import BeautifulSoup
import time

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_make(year):
    url='https://www.showmethepartsdb.com/bin/ShowMeConnectdll.dll?lookup=make&year={}&id=ASC2182&page=1&start=0&limit=25'.format(year)
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find_all('make')
    result=[]
    for item in table:
        try:
            make_name=item.find('data').get_text()
            make_id=item.find('id').get_text()
            result.append([make_id,make_name])
        except:
            continue
    return result

def get_model(year,make_id):
    url='https://www.showmethepartsdb.com/bin/ShowMeConnectdll.dll?lookup=model&year={}&make={}&id=ASC2182&page=1&start=0&limit=25'.format(year,make_id)
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find_all('model')
    result=[]
    for item in table:
        try:
            model_name=item.find('data').get_text()
            model_id=item.find('id').get_text()
            result.append([model_id,model_name])
        except:
            continue
    return result

def get_engine(year,make_id,model_id):
    url='https://www.showmethepartsdb.com/bin/ShowMeConnectdll.dll?lookup=engine&year={}&make={}&model={}&product=0065&id=ASC2182&page=1&start=0&limit=25'.format(year,make_id,model_id)
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find_all('engine')
    result=[]
    for item in table:
        try:
            engine_name=item.find('data').get_text()
            engine_id=item.find('id').get_text()
            result.append([engine_id,engine_name])
        except:
            continue
    return result

def get_parts(year,make_id,model_id,engine_id):
    url='https://www.showmethepartsdb.com/bin/ShowMeConnectdll.dll?lookup=parts&engine={}&year={}&make={}&model={}&product=0065&id=ASC2182&page=1&start=0&limit=25'.format(engine_id,year,make_id,model_id)
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find_all('partsdata')
    result=[]
    for item in table:
        try:
            part_no=item.find('part_no').get_text()
            result.append(part_no)
        except:
            continue
    return result

def main():
    startyear=1939
    while startyear<2017:
        makes=get_make(startyear)
        for make in makes:
            models=get_model(startyear, make[0])
            for model in models:
                engines=get_engine(startyear,make[0],model[0])
                for engine in engines:
                    parts=get_parts(startyear,make[0],model[0],engine[0])
                    for part in parts:
                        f=open('result.txt','a')
                        f.write("%s||%s||%s||%s||%s\n"%(startyear,make[1],model[1],engine[1],part))
                        f.close()
                print(startyear,make[1],model[1])
        startyear+=1

main()
