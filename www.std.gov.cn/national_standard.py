from util import *
from bs4 import BeautifulSoup
import re
import json
import time
import logging


def get_standard_list(page):
    url = 'http://www.std.gov.cn/gb/search/gbQueryPage?searchText=&ics=&state=&ISSUE_DATE=&sortOrder=asc&pageSize=50&pageNumber={}'.format(
        page)
    req = build_request(url)
    data = req.json()
    return data['rows']


def get_standard_info(id):
    url = 'http://www.std.gov.cn/gb/search/gbDetailed?id={}'.format(id)
    req = build_request(url)
    html = req.text.replace('\r', '').replace('\n', '').replace('\t', '')
    base_info_text = re.findall('基础信息</h2></div>(<div.*?</dl></div>)', html)[0]
    base_info = BeautifulSoup(base_info_text, 'lxml')
    names = base_info.find_all('dt', {'class': 'basicInfo-item name'})
    values = base_info.find_all('dd', {'class': 'basicInfo-item value'})
    result = {}
    for i in range(len(names)):
        name = names[i].get_text()
        value = values[i].get_text()
        result[name] = value
    result['起草单位'] = []
    try:
        company_info_text = re.findall(
            '起草单位</h2></div>(<div.*?</dl></div>)', html)[0]
        result['起草单位_text'] = company_info_text
        company_info_list = BeautifulSoup(
            company_info_text, 'lxml').find_all("dl")
        company_info_dl = []
        for item in company_info_list:
            dd_list = item.find_all('dd')
            if len(dd_list):
                company_info_dl.append(dd_list)
    except:
        company_info_dl = []

    while len(company_info_dl):
        company_info = company_info_dl.pop(0)
        if len(company_info) == 0:
            continue
        company = company_info.pop(0)
        result['起草单位'].append(company.get_text())
        if len(company_info):
            company_info_dl.append(company_info)

    result['起草人'] = []
    try:
        person_info_text = re.findall(
            '起草人</h2></div>(<div.*?</dl></div>)', html)[0]
        result['起草人_text'] = person_info_text
        person_info_list = BeautifulSoup(
            person_info_text, 'lxml').find_all("dl")
        person_info_dl = []
        for item in person_info_list:
            dd_list = item.find_all('dd')
            if len(dd_list):
                person_info_dl.append(dd_list)
    except:
        person_info_dl = []

    while len(person_info_dl):
        person_info = person_info_dl.pop(0)
        if len(person_info) == 0:
            continue
        person = person_info.pop(0)
        result['起草人'].append(person.get_text())
        if len(person_info):
            person = person_info.pop(0)
            result['起草人'].append(person.get_text())
        if len(person_info):
            person_info_dl.append(person_info)
    return result


def crawl_national_standard():
    page = 1
    while True:
        try:
            standard_list = get_standard_list(page)
        except:
            print(page, 'Faied')
            continue
        if len(standard_list) == 0:
            break
        f = open('./files/national_standard.txt', 'a')
        for standard in standard_list:
            try:
                info = get_standard_info(standard['id'])
            except:
                failed = open('./files/failed_national_standard.txt', 'a')
                failed.write(json.dumps(standard)+'\n')
                failed.close()
                continue
            standard['info'] = info
            print(standard['id'], 'OK')
            f.write(json.dumps(standard)+'\n')
        f.close()
        print(page, 'OK')
        page += 1


def load_companys():
    companys = {}
    for line in open('./files/companys.txt', 'r'):
        company = line.replace('\r', '').replace('\n', '')
        companys[company] = 1
    return companys


def load_company_standard_txt():
    companys = load_companys()
    keys = ['id', 'C_STD_CODE', 'C_C_NAME', 'ISSUE_DATE', 'ACT_DATE', 'STATE']
    info_keys = ['全部代替标准', '归口单位', '执行单位', '主管部门']
    yield keys+info_keys+['起草单位', '起草人','中关村企业']
    for line in open('./files/national_standard.txt', 'r'):
        item = json.loads(line)
        standard = []
        for key in keys:
            try:
                standard.append(item[key])
            except:
                standard.append('')
        info = item['info']
        for key in info_keys:
            try:
                standard.append(info[key])
            except:
                standard.append('')
        exists=[]
        for company in info['起草单位']:
            if company in companys:
                exists.append(company)
        if len(exists):
            standard.append(','.join(info['起草单位']))
            standard.append(','.join(info['起草人']))
            standard.append(','.join(exists))
            yield standard


def load_standard_txt():
    companys = load_companys()
    keys = ['id', 'C_STD_CODE', 'C_C_NAME', 'ISSUE_DATE', 'ACT_DATE', 'STATE']
    info_keys = ['全部代替标准', '归口单位', '执行单位', '主管部门']
    yield keys+info_keys+['起草单位', '起草人']
    for line in open('./files/national_standard.txt', 'r'):
        item = json.loads(line)
        standard = []
        for key in keys:
            try:
                standard.append(item[key])
            except:
                standard.append('')
        info = item['info']
        for key in info_keys:
            try:
                standard.append(info[key])
            except:
                standard.append('')
        standard.append(','.join(info['起草单位']))
        standard.append(','.join(info['起草人']))
        yield standard


def crawl_failed():
    for standard in open('./files/failed_national_standard.txt', 'r'):
        standard = json.loads(standard)
        try:
            info = get_standard_info(standard['id'])
        except Exception as e:
            logging.exception(e)
            failed = open('./files/failed_national_standard_1.txt', 'a')
            failed.write(json.dumps(standard)+'\n')
            failed.close()
            continue
        f = open('./files/national_standard.txt', 'a')
        standard['info'] = info
        print(standard['id'], 'OK')
        f.write(json.dumps(standard)+'\n')
        f.close()


crawl_national_standard()
write_to_excel(load_standard_txt(), '国家标准.xlsx')
write_to_excel(load_company_standard_txt(),'国家标准_中关村企业.xlsx')