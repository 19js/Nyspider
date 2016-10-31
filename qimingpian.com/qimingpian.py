import requests
from bs4 import BeautifulSoup
import json
import xlwt3
import os

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def getCompany():
    page=1
    ticket='7ced4882c35682a0b570d86f5d7707fd'
    data={
        'curpage':page,
        'ticket':ticket,
        'ptype':"qmp_pc",
        'version':"1.0",
        'unionid':"oP3fkwCIIGM082hz48KnF9RxoR-o"
    }
    f=open('companys.txt','a')
    while page<128:
        html=requests.post('http://dev.api.qimingpian.com/h/jigous',data=data,headers=headers).text
        data=json.loads(html)['items']
        ticket=data['next'].split('&')[-1].replace('ticket=','')
        for item in data['data']:
            f.write(item['jigou_name']+'||'+str(item['jigou_ticket'])+'||'+item['detail']+'\n')
        print(page,'--ok')
        page+=1
        data={
            'curpage':page,
            'ticket':ticket,
            'ptype':"qmp_pc",
            'version':"1.0",
            'unionid':"oP3fkwCIIGM082hz48KnF9RxoR-o"
        }
    f.close()

def getDetail(url,name):
    html=requests.get(url,headers=headers).text
    data=json.loads(html)['data']
    excel=xlwt3.Workbook()
    sheet=excel.add_sheet('sheet')
    count=0
    sheet.write(0,0,data['basic']['jigou_name'])
    sheet.write(1,0,data['basic']['jieduan'])
    sheet.write(2,0,data['basic']['hangye'])
    sheet.write(3,0,data['basic']['jianjie'])
    sheet.write(4,0,'投资团队：')
    sheet.write(4,1,'姓名')
    sheet.write(4,2,'职务')
    sheet.write(4,3,'领域')
    count=5
    for item in data['manager']:
        sheet.write(count,1,item['name'])
        sheet.write(count,2,item['zhiwu'])
        sheet.write(count,3,item['lingyu'])
        count+=1
    sheet.write(count,0,'对外投资：')
    sheet.write(count,1,'产品')
    sheet.write(count,2,'投资时间')
    sheet.write(count,3,'行业')
    sheet.write(count,4,'投资轮次')
    sheet.write(count,5,'最新一轮融资金额')
    count+=1
    for item in data['touzi']:
        sheet.write(count,1,item['product'])
        sheet.write(count,2,item['tzdate'])
        hanye=item['hangye1']+'-'+item['hangye2']
        sheet.write(count,3,hanye)
        sheet.write(count,4,item['lunci'])
        try:
            sheet.write(count,5,item['money']+'(%s)'%item['curlunci'])
        except:
            sheet.write(count,5,'-')
        count+=1
    excel.save('failed/%s.xls'%name.replace('/',''))

def detail():
    count=0
    for line in open('failed1.txt','r'):
        count+=1
        print(count)
        lists=line.split('||')
        ticket=lists[1]
        id=lists[-1].split('id=')[-1].replace('&nowx=1\n','')
        url='http://nba.qimingpian.com/d/j2?id=%s&ticket=%s&src=magic'%(id,ticket)
        try:
            getDetail(url,lists[0])
        except:
            failed=open('failed.txt','a')
            failed.write(line)
            failed.close()
            continue
        print(lists[0],'--ok')

def getfailed():
    f=open('exists.txt','w')
    print(len(os.listdir('excel')))
    for filename in os.listdir('excel'):
        for line in open('companys.txt','r'):
            if line.split('||')[0].replace('/','')==filename.replace('.xls','') and line.split('||')[0]!='':
                f.write(line)
    f.close()

getfailed()
