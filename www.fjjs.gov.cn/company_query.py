from util import *
from bs4 import BeautifulSoup
import json
import threading
import time
import re

def get_company_list():
    req = build_request(
        'http://www.fjjs.gov.cn:96/ConstructionInfoPublish/Pages/CompanyQuery.aspx')
    company_list = parser_company_list(req.text)
    f = open('./files/company_list.txt', 'a')
    for company in company_list:
        f.write(json.dumps(company)+'\n')
    f.close()
    data = build_data(req.text)
    page = 1
    while True:
        try:
            req = build_request(
                'http://www.fjjs.gov.cn:96/ConstructionInfoPublish/Pages/CompanyQuery.aspx', data=data)
            company_list = parser_company_list(req.text)
        except Exception as e:
            print(e)
            continue
        if len(company_list) == 0:
            break
        data = build_data(req.text)
        f = open('./files/company_list.txt', 'a')
        for company in company_list:
            f.write(json.dumps(company)+'\n')
        f.close()
        print(page, 'OK')
        page += 1


def build_data(html):
    soup = BeautifulSoup(html, 'lxml')
    data = {}
    data['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder$pGrid$nextpagebtn'
    data['__VIEWSTATE'] = soup.find(
        'input', {'id': '__VIEWSTATE'}).get('value')
    data['__VIEWSTATEGENERATOR'] = soup.find(
        'input', {'id': '__VIEWSTATEGENERATOR'}).get('value')
    data['__EVENTVALIDATION'] = soup.find(
        'input', {'id': '__EVENTVALIDATION'}).get('value')
    return data


def parser_company_list(html):
    html = html.replace('<br />', ',').replace('<br>', ',')
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find(
        'table', {'id': 'ctl00_ContentPlaceHolder_gvDemandCompany'}).find_all('tr')
    company_list = []
    for tr in table:
        td_list = tr.find_all("td")
        try:
            name = td_list[0].get_text().replace(
                '\r', '').replace('\n', '').replace('  ', '')
            url = 'http://www.fjjs.gov.cn:96/ConstructionInfoPublish/Pages/' + \
                td_list[0].find('a').get('href')
            line = [name, url]
            for td in td_list[1:]:
                line.append(td.get_text().replace(
                    '\r', '').replace('\n', '').replace('  ', ''))
        except:
            continue
        company_list.append(line)
    return company_list


def get_company_info(company_id):
    url = 'http://www.fjjs.gov.cn:96/ConstructionInfoPublish/Pages/CompanyInfo.aspx?companyID={}'.format(
        company_id)
    req = build_request(url)
    soup = BeautifulSoup(req.text, 'lxml').find('div', {'id': 'main'})
    legal_man = soup.find('td', {'id': 'LegalMan'}).get_text().replace(
                    '\r', '').replace('\n', '').replace('  ', '')
    address = soup.find('td', {'id': 'RegPrin'}).get_text().replace(
                    '\r', '').replace('\n', '').replace('  ', '')
    business_num = soup.find('td', {'id': 'EconType'}).get_text().replace(
                    '\r', '').replace('\n', '').replace('  ', '')
    return [legal_man, address, business_num]



def get_manager_info(company_id):
    index = 0
    result = []
    while True:
        url = 'http://www.fjjs.gov.cn:96/ConstructionInfoPublish/Pages/ManagerInfo.aspx?companyID={}&index={}'.format(
            company_id, index)
        req = build_request(url)
        if '没有查询到任何结果' in req.text:
            return result
        table = BeautifulSoup(req.text, 'lxml').find(
            'div', {'id': 'divManager'}).find_all('tr')
        for tr in table:
            if '<th' in str(tr):
                continue
            td_list = tr.find_all('td')
            line = []
            for td in td_list:
                line.append(td.get_text().replace(
                    '\r', '').replace('\n', '').replace('  ', ''))
            result.append(','.join(line))
        index += 1
    return result

def get_person_info(company_id):
    index = 0
    result = []
    while True:
        url = 'http://www.fjjs.gov.cn:96/ConstructionInfoPublish/Pages/RegisterPersonInfo.aspx?companyID={}&index={}'.format(
            company_id, index)
        req = build_request(url)
        if '没有查询到任何结果' in req.text:
            return result
        table = BeautifulSoup(req.text, 'lxml').find(
            'div', {'id': 'divPerson'}).find_all('tr')
        for tr in table:
            if '<th' in str(tr):
                continue
            td_list = tr.find_all('td')
            line = []
            for td in td_list:
                line.append(td.get_text().replace(
                    '\r', '').replace('\n', '').replace('  ', ''))
            result.append(','.join(line))
        index += 1
    return result

def get_title_man_info(company_id):
    index = 0
    result = []
    while True:
        url = 'http://www.fjjs.gov.cn:96/ConstructionInfoPublish/Pages/TitleManInfo.aspx?companyID={}&index={}'.format(
            company_id, index)
        req = build_request(url)
        if '没有查询到任何结果' in req.text:
            return result
        table = BeautifulSoup(req.text, 'lxml').find(
            'div', {'id': 'divTitleMain'}).find_all('tr')
        for tr in table:
            if '<th' in str(tr):
                continue
            td_list = tr.find_all('td')
            line = []
            for td in td_list:
                line.append(td.get_text().replace(
                    '\r', '').replace('\n', '').replace('  ', ''))
            result.append(','.join(line))
        index += 1
    return result

def get_liable_person_info(company_id):
    index = 0
    result = []
    while True:
        url = 'http://www.fjjs.gov.cn:96/ConstructionInfoPublish/Pages/LiablePersonInfo.aspx?companyID={}&index={}'.format(
            company_id, index)
        req = build_request(url)
        if '没有查询到任何结果' in req.text:
            return result
        table = BeautifulSoup(req.text, 'lxml').find(
            'div', {'id': 'divLiable'}).find_all('tr')
        for tr in table:
            if '<th' in str(tr):
                continue
            td_list = tr.find_all('td')
            line = []
            for td in td_list:
                line.append(td.get_text().replace(
                    '\r', '').replace('\n', '').replace('  ', ''))
            result.append(','.join(line))
        index += 1
    return result

def get_other_liable_person_info(company_id):
    index = 0
    result = []
    while True:
        url = 'http://www.fjjs.gov.cn:96/ConstructionInfoPublish/Pages/OtherLiablePersonInfo.aspx?companyID={}&index={}'.format(
            company_id, index)
        req = build_request(url)
        if '没有查询到任何结果' in req.text:
            return result
        table = BeautifulSoup(req.text, 'lxml').find(
            'div', {'id': 'divLiable'}).find_all('tr')
        for tr in table:
            if '<th' in str(tr):
                continue
            td_list = tr.find_all('td')
            line = []
            for td in td_list:
                line.append(td.get_text().replace(
                    '\r', '').replace('\n', '').replace('  ', ''))
            result.append(','.join(line))
        index += 1
    return result


class CompanyInfo(threading.Thread):
    def __init__(self,base_info):
        super(CompanyInfo,self).__init__()
        self.daemon=True
        self.base_info=base_info
        self.company_id=re.findall('companyID=(\d+)',self.base_info[1])[0]

    def run(self):
        self.status=False
        try:
            company_info=get_company_info(self.company_id)
        except:
            return
        try:
            person_list=get_person_info(self.company_id)
        except:
            return
        try:
            manager_list=get_manager_info(self.company_id)
        except:
            return
        try:
            title_man_list=get_title_man_info(self.company_id)
        except:
            return
        try:
            liable_list=get_liable_person_info(self.company_id)
        except:
            return
        try:
            other_liable_list=get_other_liable_person_info(self.company_id)
        except:
            return
        self.result=self.base_info+company_info+['\n'.join(person_list),'\n'.join(manager_list),'\n'.join(title_man_list),'\n'.join(liable_list),'\n'.join(other_liable_list)]
        self.status=True
        
def load_company_items():
    items=[]
    for line in open('./files/company_list.txt','r'):
        item=json.loads(line)
        items.append(item)
        if len(items)<1:
            continue
        yield items
        items=[]
    yield items

def crawl():
    success_num=0
    failed_num=0
    for items in load_company_items():
        tasks=[]
        for item in items:
            task=CompanyInfo(item)
            tasks.append(task)
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        for task in tasks:
            if task.status:
                f=open('./files/result.txt','a')
                f.write(json.dumps(task.result)+'\n')
                f.close()
                success_num+=1
            else:
                failed=open('./files/failed.txt','a')
                failed.write(json.dumps(task.base_info)+'\n')
                failed.close()
                failed_num+=1
        print(current_time(),success_num,failed_num)

crawl()