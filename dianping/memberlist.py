import requests
from bs4 import BeautifulSoup
import time

headers = {
    'Host':'www.dianping.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Cookie':'_hc.v=6a05f596-3058-2734-267b-4911da5f4dca.1478187831; __utma=1.605496850.1478187831.1478187831.1478187831.1; __utmz=1.1478187831.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; PHOENIX_ID=0a010439-1582d1bafc7-3dd609; JSESSIONID=AC590505E722BF8103C4D9C3A612EEF4; aburl=1; cy=4; cye=guangzhou',
    'Connection': 'keep-alive'}

def get_memberlist():
    page=1
    while True:
        url='http://www.dianping.com/memberlist/4/10?pg='+str(page)
        html=requests.get(url,headers=headers).text
        table=BeautifulSoup(html,'lxml').find('table',{'class':'rankTable'}).find('tbody').find_all('tr')
        f=open('memberlist.txt','a')
        for item in table:
            try:
                tds=item.find_all('td')
                name=tds[0].find('a').get_text()
                url=tds[0].find('a').get('href')
                comment_num=tds[1].get_text()
                reply_num=tds[3].get_text()
                flower_num=tds[4].get_text()
                f.write(str([name,url,comment_num,reply_num,flower_num])+'\n')
            except:
                continue
        f.close()
        page+=1
        if page==7:
            break

def get_comments(usrid):
    baseurl='http://www.dianping.com/member/{}/reviews?pg={}&reviewCityId=0&reviewShopType=10&c=0&shopTypeIndex=1'
    page=1
    html=requests.get(baseurl.format(usrid,page),headers=headers).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'main'})
    citys=soup.find('div',{'class':'p-term-list'}).find_all('li')[1].find_all('span')
    city_num=len(citys)
    city_text=''
    for span in citys:
        city_text+=span.get_text()+'\t'
    table=soup.find('div',id='J_review').find_all('div',{'class':'J_rptlist'})
    result=[]
    for item in table:
        title=item.find('a').get_text()
        url=item.find('a').get('href')
        try:
            address=item.find('div',{'class':'addres'}).get_text()
        except:
            address=''
        try:
            star=item.find('div',{'class':'comm-rst'}).find('span').get('class')[1].replace('irr-star','')
        except:
            star=''
        content=item.find('div',{'class':'comm-entry'}).get_text()
        date=item.find('div',{'class':"info"}).find('span').get_text().replace("发表于",'')
        line=[city_num,city_text,title,url,address,star,content,date]
        result.append(line)
    page+=1
    while True:
        print(page)
        html=requests.get(baseurl.format(usrid,page),headers=headers).text
        soup=BeautifulSoup(html,'lxml').find('div',{'class':'main'})
        table=soup.find('div',id='J_review').find_all('div',{'class':'J_rptlist'})
        for item in table:
            title=item.find('a').get_text()
            url=item.find('a').get('href')
            try:
                address=item.find('div',{'class':'addres'}).get_text()
            except:
                address=''
            try:
                star=item.find('div',{'class':'comm-rst'}).find('span').get('class')[1].replace('irr-star','')
            except:
                star=''
            content=item.find('div',{'class':'comm-entry'}).get_text()
            date=item.find('div',{'class':"info"}).find('span').get_text().replace("发表于",'')
            line=[city_num,city_text,title,url,address,star,content,date]
            result.append(line)
            if len(result)==100:
                return result
        time.sleep(1)
        page+=1
    return result

def shop_infor(shopurl):
    html=requests.get(url,headers=headers).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'body-content'})
    try:
        types=soup.find('div',{'class':'breadcrumb'}).find_all('a')
        shop_type=types[2].get_text()
    except:
        shop_type=''
    base_infor=soup.find('div',id='basic-info').find('div',{'class':'brief-info'})
    try:
        star=base_infor.find('span',{'class':'mid-rank-stars'}).get('class')[1].replace('mid-str','')
    except:
        star=''
    line=['']*4
    for item in base_infor.find_all('span'):
        if '人均' in str(item):
            text=item.get_text()
            line[0]=text
        if '口味' in str(item):
            text=item.get_text()
            line[1]=text
        if '环境' in str(item):
            text=item.get_text()
            line[2]=text
        if '服务' in str(item):
            text=item.get_text()
            line[3]=text
    return [shop_type,star]+line

def get_fans(usrid):
    

def main():
    usrs=[eval(line) for line in open('./memberlist.txt','r')]
    flag=True
    for usr in usrs:
        usrid=usr[1].split('/')[-1]
        try:
            result=get_comments(usrid)
        except:
            failed=open('failed.txt','a')
            failed.write(str(usr)+'\n')
            failed.close()
            print(usr,'failed')
            continue
        f=open('comments.txt','a')
        for item in result:
            f.write(str(usr+item)+'\n')
        f.close()
        print(usr,'ok')

main()
