import requests
from bs4 import BeautifulSoup
import openpyxl

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def parser_city():
    html=open('./city.html','r').read()
    table=BeautifulSoup(html,'lxml').find_all('a')
    f=open('city.txt','w')
    for item in table:
        city=item.get_text()
        url=item.get('href')
        f.write(city+'--'+url+'\n')
    f.close()

def parser(city,url):
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'api_month_list'}).find('table').find_all('tr')
    result=[]
    for item in table:
        line=[city]
        for td in item.find_all('td'):
            try:
                line.append(td.get_text().replace('\r\n','').replace(' ',''))
            except:
                line.append('')
        result.append(line)
    return result

def get_air_report(city,city_url):
    year=2013
    month=11
    result=[]
    while(year<2018):
        while(month%13!=0):
            url='http://www.tianqihoubao.com'+city_url.replace('.html','-%s%02d.html'%(year,month))
            try:
                result+=parser(city,url)
            except:
                print(city,year,month,'failed')
                continue
            print(city,year,month,'ok')
            if year==2017 and month==3:
                break
            month+=1
        month=1
        year+=1
    return result

def main():
    for line in open('city.txt','r'):
        line=line.replace('\n','').split('--')
        result=get_air_report(line[0],line[1])
        f=open('result.txt','a')
        for line in result:
            f.write(str(line)+'\n')
        f.close()

main()
