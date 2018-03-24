from util import *
from bs4 import BeautifulSoup
import re
import json
import time
import logging


def get_standard_list(page):
    url = 'http://www.std.gov.cn/gb/search/gbProcessInfoPage?searchText=&ics=&sortOrder=asc&pageSize=50&pageNumber={}'.format(
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
    return result


def crawl_process_standard():
    page = 1
    while True:
        try:
            standard_list = get_standard_list(page)
        except:
            print(page, 'Faied')
            continue
        if len(standard_list) == 0:
            break
        f = open('./files/process_standard.txt', 'a')
        for standard in standard_list:
            try:
                info = get_standard_info(standard['id'])
            except:
                failed = open('./files/failed_process_standard.txt', 'a')
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
    need_companys = load_companys()
    keys = ['id','C_PLAN_CODE', 'C_C_NAME', 'STD_FORM', 'SEND_DATE', 'CURRENT_LINK']
    info_keys = ['全部代替标准', '归口单位', '执行单位', '主管部门']
    yield keys+info_keys+['起草单位','中关村企业']
    for line in open('./files/process_standard.txt', 'r'):
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
        exists = []
        index = 0
        for company in info['起草单位']:
            index+=1
            if company in need_companys:
                exists.append('%s %s' % (index, company))
        standard.append(','.join(info['起草单位']))
        if len(exists):
            standard.append(','.join(exists))
        yield standard


def load_standard_txt():
    companys = load_companys()
    keys = ['id','C_PLAN_CODE', 'C_C_NAME', 'STD_FORM', 'SEND_DATE', 'CURRENT_LINK']
    info_keys = ['全部代替标准', '归口单位', '执行单位', '主管部门']
    yield keys+info_keys+['起草单位']
    for line in open('./files/process_standard.txt', 'r'):
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
        yield standard


write_to_excel(load_company_standard_txt(),'国家计划.xlsx')