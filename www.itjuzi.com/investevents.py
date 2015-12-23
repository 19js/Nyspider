#codnig:utf-8

import requests
from bs4 import BeautifulSoup
import xlwt3

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_base_infor():
    f=open('data.txt','a')
    for page in range(1048):
        html=requests.get('https://www.itjuzi.com/investevents?page=%s'%(page+1),headers=headers).text
        table=BeautifulSoup(html,'html.parser').find_all('ul',attrs={'class':'list-main-eventset'})[1].find_all('li')
        for li in table:
            item={}
            i=li.find_all('i')
            item['date']=i[0].get_text()
            item['url']=i[1].find('a').get('href')
            spans=i[2].find_all('span')
            item['name']=spans[0].get_text()
            item['industry']=spans[1].get_text()
            item['local']=spans[2].get_text()
            item['round']=i[3].get_text()
            item['capital']=i[4].get_text()
            companys=i[5].find_all('a')
            lists=[]
            if(companys==[]):
                lists.append(i[5].get_text())
            else:
                for a in companys:
                    lists.append(a.get_text())
            item['Investmenters']=lists
            f.write(str(item)+'\n')
        print(page)

def main():
    f=open('data.txt','r')
    data_f=open('investevents.txt','a')
    failed_f=open('failed.txt','a')
    for line in f.readlines():
        try:
            item=eval(line.replace('\n',''))
            html=requests.get(item['url'],headers=headers).text
            url=BeautifulSoup(html,'lxml').find('div',attrs={'class':'block-inc-fina'}).find('a',attrs={'class':'incicon'}).get('href')
            html=requests.get(url,headers=headers).text
            soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'thewrap'})
            table=soup.find('div',attrs={'class':'sec'})
            company_url=table.find('div',attrs={'class':'rowhead'}).find('div',attrs={'class':'row c-gray-aset'}).find('div',attrs={'class':'dbi linkset c-gray'}).find('a').get('href')
            tags=[]
            for a in table.find('div',attrs={'class':'rowfoot'}).find('div',attrs={'class':'tagset dbi'}).find_all('a'):
                tags.append(a.get_text())
            des=soup.find('div',attrs={'class':'block block-inc-info'}).find('div',attrs={'class':'des'}).get_text()
            item['company_url']=company_url
            item['tags']=tags
            item['des']=des
            data_f.write(str(item)+'\n')
            print(item['url'])
        except:
            failed_f.write(line)

main()
