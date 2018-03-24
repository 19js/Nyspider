from util import *
from bs4 import BeautifulSoup
import re
import json
import time
import logging


def get_standard_list(page):
    url = 'http://www.std.gov.cn/hb/search/hbPage?searchText=&op=&ISSUE_DATE=&sortOrder=asc&pageSize=50&pageNumber={}'.format(
        page)
    req = build_request(url)
    data = req.json()
    return data['rows']

def crawl_industry_standard():
    page = 1
    while True:
        try:
            standard_list = get_standard_list(page)
        except:
            print(page, 'Faied')
            continue
        if len(standard_list) == 0:
            break
        f = open('./files/industry_standard.txt', 'a')
        for standard in standard_list:
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
    keys = ['id', 'C_STD_CODE', 'C_NAME', 'ISSUE_DATE', 'ACT_DATE','G_TRADE_DEPT_FULL', 'TA_UNIT','CHARGE_DEPT','TRADE_CLASSIFIED','RECORD_NO','NOTICE_NO','DRAFT_UNIT','DRAFT_USERS']
    yield keys
    for line in open('./files/industry_standard.txt', 'r'):
        item = json.loads(line)
        standard = []
        for key in keys:
            try:
                standard.append(item[key])
            except:
                standard.append('')
        exists=[]
        index=0
        for company in standard['DRAFT_UNIT'].split('、'):
            index+=1
            company=company.replace('等')
            if company in companys:
                exists.append('%s %s'%(index,company))
        if len(exists):
            standard.append(','.join(exists))
            yield standard


def load_standard_txt():
    keys = ['id', 'C_STD_CODE', 'C_NAME', 'ISSUE_DATE', 'ACT_DATE','G_TRADE_DEPT_FULL', 'TA_UNIT','CHARGE_DEPT','TRADE_CLASSIFIED','RECORD_NO','NOTICE_NO','DRAFT_UNIT','DRAFT_USERS']
    for line in open('./files/industry_standard.txt', 'r'):
        item = json.loads(line)
        standard = []
        for key in keys:
            try:
                standard.append(item[key])
            except:
                standard.append('')
        yield standard


def crawl_failed():
    for standard in open('./files/failed_industry_standard.txt', 'r'):
        standard = json.loads(standard)
        try:
            info = get_standard_info(standard['id'])
        except Exception as e:
            logging.exception(e)
            failed = open('./files/failed_industry_standard_1.txt', 'a')
            failed.write(json.dumps(standard)+'\n')
            failed.close()
            continue
        f = open('./files/industry_standard.txt', 'a')
        standard['info'] = info
        print(standard['id'], 'OK')
        f.write(json.dumps(standard)+'\n')
        f.close()


crawl_industry_standard()