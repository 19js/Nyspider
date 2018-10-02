# coding:utf-8

import requests
from bs4 import BeautifulSoup
import json
import codecs
import logging
import re
import random
import time
import csv
import os


# 用户名
j_username = ""
# 密码
j_password = ''

Cookies = {}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}


def parser_loan(item):
    info_keys = ['officeScale', 'carLoan', 'realName', 'creditLevel', 'office', 'province', 'officeType', 'idNo', 'sumCreditPoint', 'houseLoan', 'marriage', 'userId', 'city', 'position',
                 'university', 'workYears', 'birthDay', 'graduation', 'homeTown', 'carYear', 'hasHouse', 'gender', 'hasCar', 'officeDomain', 'availableCredits', 'promotion', 'nickName', 'salary', 'carBrand']
    loan_keys = ['loanId', 'title', 'amount', 'status', 'interest', 'repayType', 'verifyState', 'borrowerLevel',
                 'borrowType', 'months', 'leftMonths', 'description', 'startTime', 'passTime', 'nickName', 'address', 'jobType']
    detail_keys = ['totalCount', 'successCount', 'alreadyPayCount',
                   'borrowAmount', 'notPayTotalAmount', 'overdueAmount', 'overdueCount']
    credit_keys = ['identification', 'borrowStudy',
                   'incomeDuty', 'credit', 'identificationScanning', 'work']
    info = []
    for key in loan_keys:
        try:
            value = item['info']['loan'][key]
            if 'Time' in key:
                try:
                    value = time.strftime(
                        '%Y-%m-%d %H:%M:%S', time.localtime(int(value)/1000))
                except Exception as e:
                    print(e)
            info.append(str(value))
        except:
            info.append('')
    for key in info_keys:
        try:
            info.append(str(item['info']['borrower'][key]))
        except:
            info.append('')
    for key in detail_keys:
        try:
            info.append(str(item['info']['userLoanRecord'][key]))
        except:
            info.append('')
    for key in credit_keys:
        try:
            info.append(str(item['info']['creditInfo'][key]))
        except:
            info.append('')
    return info


def append_to_csv_file(lines, filename):
    csvfile = codecs.open(filename, 'a', encoding='utf-8')
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
    for line in lines:
        spamwriter.writerow(line)
    csvfile.close()


def login():
    data = {
        'j_username': j_username,
        'j_password': j_password,
        'rememberme': 'on',
        'targetUrl': 'https://www.renrendai.com/loan.html',
        'returnUrl': ''}
    session = requests.session()
    html = session.post(
        'https://www.renrendai.com/passport/index/doLogin', data=data, headers=headers)
    global Cookies
    Cookies = session.cookies.get_dict()
    print('login', Cookies)


def get_loan_info(loan_id):
    url = 'https://www.renrendai.com/loan-{}.html'.format(loan_id)
    html = requests.get(url, cookies=Cookies, headers=headers).text
    detail = re.findall("var detail = '(.*?)';", html)[0]
    data = json.loads('"%s"' % detail)
    detail = json.loads(data)
    info = re.findall("var info = '(.*?)';", html)[0]
    data = json.loads('"%s"' % info)
    info = json.loads(data)
    return {
        'detail': detail,
        'info': info
    }


def crawl():
    loan_id = 2514193
    loan_id_to = 2714193
    login()
    temp_lines = []

    while loan_id < loan_id_to:
        try:
            loan_info = get_loan_info(loan_id)
            line = parser_loan(loan_info)
            line.append(json.dumps(loan_info))
        except Exception as e:
            print('Error', e)
            try:
                login()
            except:
                pass
            continue

        temp_lines.append(line)
        # 20条保存一次
        if len(temp_lines) == 20:
            append_to_csv_file(temp_lines, './files/人人贷散标数据.csv')
            temp_lines = []

        print(loan_id, 'OK')
        loan_id += 1
    append_to_csv_file(temp_lines, './files/人人贷散标数据.csv')


if __name__ == '__main__':
    try:
        os.mkdir('files')
    except:
        pass
    crawl()
