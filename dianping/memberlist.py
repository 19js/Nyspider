import requests
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
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
        page+=1
    return result

def main():
    usrs=[eval(line) for line in open('./memberlist.txt','r')]
    flag=True
    for usr in usrs:
        usrid=usr[1].split('/')[-1]
        if usrid!='5459347' and flag==True:
            continue
        flag=False
        try:
            result=get_comments(usrid)
        except:
            failed=open('failed.txt','a')
            failed.write(str(usr)+'\n')
            failed.close()
            continue
        f=open('comments.txt','a')
        for item in result:
            f.write(str(usr+item)+'\n')
        f.close()
        print(usr,'ok')

main()
