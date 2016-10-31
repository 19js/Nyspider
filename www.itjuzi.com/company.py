#codnig:utf-8

import requests
from bs4 import BeautifulSoup
import time
import re
import json
import openpyxl

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_investlist(url):
    html=requests.get(url,headers=headers,timeout=50).text
    results=[]
    table=BeautifulSoup(html,'html.parser').find_all('ul',attrs={'class':'list-main-eventset'})[1].find_all('li')
    for li in table:
        item={}
        i=li.find_all('i')
        item['url']=i[1].find('a').get('href')
        spans=i[2].find_all('span')
        item['name']=spans[0].get_text().replace('\n','').replace('\t','')
        results.append(item)
    return results

def get_companyurl(url):
    html=requests.get(url,headers=headers).text
    companyurl=BeautifulSoup(html,'lxml').find('div',{'class':'main'}).find('div',{'class':'block-inc-fina'}).find('a').get('href')
    return companyurl

def company_infor(company):
    html=requests.get(company['companyurl'],headers=headers).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'thewrap'})
    boxes=soup.find_all('div',{'class':'boxed'})
    picinfo=soup.find('div',{'class':'on-edit-hide'}).find('div',{'class':'picinfo'})
    try:
        title=picinfo.find('span',{'class':'title'}).get_text().replace('\n','').replace('\t','')
        company['name']=title
    except:
        pass
    try:
        indus=picinfo.find('span',{'class':'scope'}).find_all('a')
        company['industry']=''
        for a in indus:
            company['industry']+=a.get_text().replace('\n','')+';'
    except:
        company['industry']=''
    try:
        place=picinfo.find('span',{'class':'loca'}).get_text()
        company['location']=place.replace('\n','')
    except:
        company['location']=''
    try:
        site=picinfo.find('a',{'class':'weblink'}).get_text()
        company['website']=site
    except:
        company['website']=''
    try:
        tags=soup.find('div',{'class':'infoheadrow-v2'}).find('div',{'class':'rowfoot'}).find_all('a')
        company['tags']=''
        for tag in tags:
            company['tags']+=tag.get_text()+';'
    except:
        company['tags']=''
    baseinfor=soup.find('div',{'class':'block-inc-info'}).find_all('div',{'class':'block'})
    try:
        company['baseinfor']=baseinfor[1].get_text().replace('\n','').replace('\t','')
    except:
        company['baseinfor']=''
    try:
        text=baseinfor[2].get_text().replace('\r','').replace('\n','').replace('\t','').replace(' ','')
        result=re.findall('公司全称：(.*?)成立时间：(.*)公司规模：(.*)',text)[0]
        company['fullname']=result[0]
        company['startdate']=result[1].replace('\xa0\xa0','')
        company['size']=result[2].replace('运营中','')
    except:
        result=['']*3
        company['fullname']=result[0]
        company['startdate']=result[1]
        company['size']=result[2]
    try:
        roundlist=soup.find('table',{'class':'list-round-v2'}).find_all('tr')
        rounds=[]
        for tr in roundlist:
            rou={}
            tds=tr.find_all('td')
            rou['date']=tds[0].find('span').get_text().replace('\n','')
            rou['round']=tds[1].get_text().replace('\n','')
            rou['capital']=tds[2].get_text().replace('\n','')
            try:
                companys=tds[3].find_all('a')
                Investmenters=''
                if(companys==[]):
                    Investmenters=tds[3].get_text().replace('\n','').replace('\t','')
                else:
                    for a in companys:
                        Investmenters+=a.get_text().replace('\n','').replace('\t','')+';'
                rou['Investmenters']=Investmenters
            except:
                rou['Investmenters']=''
            rounds.append(rou)
        company['round']=rounds
    except:
        company['round']=[]
    try:
        person=soup.find('ul',{'class':'list-prodcase'}).find_all('li')
        text=''
        for item in person:
            try:
                text+=item.find('p').get_text().replace('\r','').replace('\n','').replace('\t','')+'\n'
            except:
                continue
        company['team']=text
    except:
        company['team']=''
    try:
        des=soup.find_all('div',{'class':'sec'})
        company['sholu']=''
        for item in des:
            if '收录于专辑' in str(item):
                for li in item.find('ul',{'class':'list-lite-pictext'}).find_all('li'):
                    company['sholu']+=li.get_text().replace('\t','').replace('\n','')+'\n'
    except:
        company['sholu']=''
    return company

def write_to_excel(item):
    try:
        import os
        os.mkdir('excel')
    except:
        pass
    keys=['name','industry','location','website','tags','baseinfor','fullname','startdate','size','sholu','team']
    roundkeys=['date','round','capital','Investmenters']
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    company=[]
    for key in keys:
        company.append(item[key])
    if item['round']==[]:
        sheet.append(company)
    for rou in item['round']:
        roundinfor=[]
        for key in roundkeys:
            roundinfor.append(rou[key])
        sheet.append(company+roundinfor)
    excel.save('excel/%s'%(time.strftime("%Y%m%d_%H%M%S",time.localtime()))+'.xlsx')

def main():
    code=input('输入公司代码:')
    item={'companyurl':'http://www.itjuzi.com/company/%s'%code,'name':''}
    company=company_infor(item)
    print(company)
    write_to_excel(company)

main()
