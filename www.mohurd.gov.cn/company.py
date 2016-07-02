import requests
from bs4 import BeautifulSoup
import json
import re
import copy

headers = {
    'Host':"210.12.219.18",
    'X-Requested-With':"XMLHttpRequest",
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/44.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer':"http://210.12.219.18/jianguanfabuweb/companies.html",
    'Connection': 'keep-alive'}

def getCompanyUrl():
    f=open('urls.txt','a')
    page=1
    while page<926:
        try:
            html=requests.get('http://210.12.219.18/jianguanfabuweb/handler/GetCompanyData.ashx?method=GetCorpData&corpname=&certid=&endtime=&cert=5&name=-1&PageIndex=%s&PageSize='%(page),headers=headers).text
        except:
            continue
        data=json.loads(html)['tb']
        table=BeautifulSoup(html,'lxml').find_all('tr')
        for tr in table:
            f.write(tr.find('a').get('title')+'||'+tr.find('a').get('href')+'\n')
        print(page)
        page+=1

def companyInfor(url,name):
    keys=['法人代表','所属省市','联系地址','工程监理资质','招标代理','造价咨询','注册人员']
    company={}
    company['name']=name
    for key in keys:
        company[key]=[]
    html=requests.get('http://210.12.219.18/jianguanfabuweb/'+url,headers=headers).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'content'})
    corpid=re.findall('encodeURI\((\d+)\)',html)[0]
    basic=soup.find('table',{'class':'company_basic_infor_table'}).get_text().replace('\r','').replace('\n','').replace(' ','')
    basic_re='法人代表：(.*?)企业.*所属省市：(.*?)联系地址：(.*?)备注'
    infor=re.findall(basic_re,basic)[0]
    company['法人代表']=infor[0]
    company['所属省市']=infor[1]
    company['联系地址']=infor[2]
    zizhi=soup.find_all('div',{'class':'zizhi'})
    for item in zizhi:
        header=item.find('div',{'class':'zizhi_header'}).get_text()
        if '监理' in header:
            table=item.find('table').find_all('td')[-1].get_text().split(',')
            company['工程监理资质']+=table
        if '招标代理' in header:
            table=item.find('table').find_all('td')[-1].get_text().split(',')
            company['招标代理']+=table
        if '造价' in header:
            table=item.find('table').find_all('td')[-1].get_text().split(',')
            company['造价咨询']+=table
    html=requests.get('http://210.12.219.18/jianguanfabuweb/handler/Company_Details_CertifiedEngineers.ashx?method=getStaff&corpid='+corpid,headers=headers).text
    table=BeautifulSoup(html,'lxml').find_all('a')
    result=[]
    for item in table:
        person=copy.deepcopy(company)
        person['url']=item.get('href').replace('\\"','')
        result.append(person)
    return result

def getPerson():
    f=open('person.txt','a')
    for line in open('urls.txt','r').readlines():
        lists=line.replace('\n','').split('||')
        try:
            result=companyInfor(lists[1],lists[0])
        except:
            failed=open('failed_company.txt','a')
            failed.write(line)
            failed.close()
            print(line,'failed')
            continue
        for item in result:
            f.write(str(item)+'\n')
    f.close()

getPerson()
