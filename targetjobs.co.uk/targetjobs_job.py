import requests
from bs4 import BeautifulSoup
import os
import time
import openpyxl
import copy

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
}

facts_class = {
    'closing_date': 'pane-node-field-ad-vac-closing-date',
    'type_of_opportunity': 'pane-node-taxonomy-vocabulary-46',
    'location': 'pane-node-field-ad-vac-locations',
    'region':'pane-node-taxonomy-vocabulary-73',
    'salary_notes':'pane-node-field-ad-vac-salary-notes',
    'vacancies':'pane-node-field-number-of-vacancies',
    'degree_requirements':'pane-node-taxonomy-vocabulary-51',
    'work_permit':'pane-node-field-ad-vac-work-permit'
}

class NetworkError(Exception):
    pass

def load_html(url,headers):
    for i in range(5):
        try:
            html = requests.get(url,headers, timeout=20).text
            return html
        except:
            continue
    raise NetworkError

def get_jobs():
    page=0
    result=[]
    while True:
        url='https://targetjobs.co.uk/internships-vacancies?page='+str(page)
        res_text=load_html(url,headers)
        table=BeautifulSoup(res_text,'lxml').find_all('div',{'class':'panel-flexible-inside panels-flexible-search_result-inside'})[3:]
        if len(table)==0:
            break
        for item in table:
            try:
                tag_list=item.find_all('a')
                job={}
                job['company_url']='https://targetjobs.co.uk'+tag_list[0].get('href')
                job['title']=tag_list[1].get_text()
                job['url']='https://targetjobs.co.uk'+tag_list[1].get('href')
            except:
                continue
            result.append(job)
        print('get_jobs page',page,'OK')
        page+=1
    return result

def get_job_info(url):
    html=load_html(url,headers)
    soup = BeautifulSoup(html, 'lxml').find('div', {'id': 'block-system-main'})
    result={}
    try:
        result['des'] = soup.find(
            'div', {'class': 'field-type-text-with-summary'}).get_text().replace('\xa0', '')
    except:
        result['des'] = ''
    for fact_key in facts_class:
        try:
            item = soup.find('div', {'class': facts_class[fact_key]})
            value = item.find('div', {'class': 'field-item'}).get_text()
            result[fact_key] = value
        except:
            result[fact_key] = ''
    sector_list=soup.find('div',{'class':'pane-employer-details'}).find_all('span',{'class':'sector name'})
    sectors=','.join([item.get_text() for item in sector_list])
    result['sectors']=sectors
    return result

def write_to_excel(result):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    keys=['title','url','company_url','des','sectors','closing_date','type_of_opportunity','location','region','salary_notes','vacancies','degree_requirements','work_permit']
    sheet.append(keys)
    for company in result:
        line=[]
        for key in keys:
            try:
                line.append(company[key])
            except:
                line.append('')
        try:
            sheet.append(line)
        except:
            pass
    excel.save('jobs.xlsx')

def crawl():
    jobs=get_jobs()
    result=[]
    for job in jobs:
        try:
            job_info=get_job_info(job['url'])
        except:
            with open('job_failed.txt','a',encoding='utf-8') as f:
                f.write(str(job)+'\r\n')
            continue
        for key in job_info:
            job[key]=job_info[key]
        result.append(job)
        try:
            print(job['title'],job['url'],'OK')
        except:
            pass
    write_to_excel(result)

if __name__=='__main__':
    crawl()