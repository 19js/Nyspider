#coding:utf-8

import requests
import json
import xlwt3
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_job(keyword,pagenum):
    js_data=requests.get('http://www.lagou.com/jobs/positionAjax.json?px=new&kd=%s&pn=%s&'%(keyword,pagenum),headers=headers).text
    data=json.loads(js_data)
    data=data['content']['result']
    jobs=[]
    for item in data:
        job={}
        job['postiontype']=item['positionType']
        job['company']=item['companyShortName']
        job['salary']=item.get('salary')
        job['workYear']=item['workYear']
        job['education']=item['education']
        job['industryField']=item['industryField']
        job['companySize']=item['companySize']
        job['createTime']=item['createTime']
        job['city']=item['city']
        job['financeStage']=item['financeStage']
        jobs.append(job)
    return jobs

def excel():
    excel=xlwt3.Workbook()
    sheet=excel.add_sheet('sheet')
    count=0
    labels=['postiontype','company','salary','workYear','education','industryField','companySize','city','financeStage']
    page=1
    while page<300:
        try:
            jobs=get_job('',page)
        except:
            time.sleep(5)
            continue
        for job in jobs:
            num=0
            for i in labels:
                sheet.write(count,num,job[i])
                num+=1
            count+=1
        print(page,count)
        page+=1
        time.sleep(2)
        excel.save('jobs.xls')

def write2txt():
    f=open('job.txt','a')
    page=1
    count=0
    while page<300:
        try:
            jobs=get_job('',page)
        except:
            time.sleep(5)
            continue
        for job in jobs:
            count+=1
            f.write(str(job)+'\n')
        print(page,count)
        page+=1
        time.sleep(2)
    f.close()

write2txt()
