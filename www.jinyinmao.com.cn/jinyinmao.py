import requests
import time
import random
import datetime
import json
import csv
import os
from bs4 import BeautifulSoup


def get_headers():
    pc_headers = {
        "X-Forwarded-For": '%s.%s.%s.%s' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    return pc_headers


class NetWorkError(Exception):
    pass


def build_request(url, headers=None, data=None, json_data=None, timeout=15, try_times=3):
    time.sleep(random.randint(1, 5)/10)
    if headers is None:
        headers = get_headers()
    for i in range(try_times):
        try:
            if data:
                response = requests.post(
                    url, data=data, headers=headers, timeout=timeout)
            elif json_data:
                headers['Content-Type'] = 'application/json'
                response = requests.post(
                    url, data=json.dumps(json_data), headers=headers, timeout=timeout)
            else:
                response = requests.get(url, headers=headers, timeout=timeout)
            return response
        except Exception as e:
            continue
    raise NetWorkError


def write_to_csv(lines, filename):
    csvfile = open(filename, 'w', encoding='utf-8')
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for line in lines:
        spamwriter.writerow(line)
    csvfile.close()


def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def get_project_list(page):
    url = 'https://jym-pre-api.jinyinmao.com.cn/Product/Regular/FavoriteTypePage/{}?orderby=undefined&ascdesc=undefined&categories=100000010&categories=100000011&categories=100000012&categories=100000020&categories=100000021&categories=100000022&categories=100000023&categories=100000040&categories=210001010&categories=210003010&categories=210002020'.format(
        page)
    headers = get_headers()
    headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    req = build_request(url, headers=headers)
    items = req.json()['items']
    result = []
    category_dict = {
        '10020': '银企众盈',
        '10010': '商融保盈',
        '10030': '普惠众盈',
        '21000': '银行专区'
    }
    need_keys = ['topProductCategory', 'issueNo', 'yield', 'period', 'financingSumAmount', 'bankName', 'riskManagement', 'riskManagementMode', 'productId', 'assetInfoDesc', 'currentValueDate', 'drawee', 'draweeInfo', 'endorseImageLink', 'endorseImagesLink', 'endSellTime', 'enterpriseInfo', 'enterpriseLicense', 'enterpriseName', 'isLoans', 'isSignature', 'issueTime', 'paidAmount', 'pledgeNo', 'productCategory',
                 'productIdentifier', 'productName', 'productNo', 'issueProductPuHuiZhongYinCarRequest', 'issueProductPuHuiZhongYinDebtorBasicInfoRequest', 'issueProductPuHuiZhongYinHouseRequest', 'repaid', 'repaidTime', 'repaymentDeadline', 'returnMoneyMethod', 'riskManagementInfo', 'settleDate', 'soldOut', 'soldOutTime', 'specifyValueDate', 'startSellTime', 'unitPrice', 'usage', 'valueDate', 'valueDateMode', 'valueDays']
    for item in items:
        line = []
        for key in need_keys:
            if key in item:
                value = item[key]
                if value is None:
                    value = ''
                if key in ['financingSumAmount', 'yield']:
                    value = value/100
                if type(value) is str:
                    value = value.replace('\r', '').replace('\n', '')
                line.append(value)
            else:
                value.append('')
        category = category_dict[str(line[0])]
        result.append([category]+line)
    return result


def get_project_orders(project_id):
    url = 'https://jym-pre-api.jinyinmao.com.cn/api/V1/Order/PagingOrders/{}/{}'
    not_end = True
    page = 0
    result = []
    while not_end:
        try:
            req = build_request(url.format(project_id, page))
            data = req.json()
            not_end = data['hasNextPage']
            items = data['items']
        except:
            break
        for item in items:
            try:
                line = [item['userInfos']['realName'],
                        item['principal']/100, item['orderTime']]
            except:
                continue
            result.append(line)
        page += 1
    return result


def crawl_projects():
    start_page = 1  # 起始页
    end_page = 1  # 结束页
    current_page = start_page-1
    header = ['Category', 'topProductCategory', 'issueNo', 'yield', 'period', 'financingSumAmount', 'bankName', 'riskManagement', 'riskManagementMode', 'productId', 'assetInfoDesc', 'currentValueDate', 'drawee', 'draweeInfo', 'endorseImageLink', 'endorseImagesLink', 'endSellTime', 'enterpriseInfo', 'enterpriseLicense', 'enterpriseName', 'isLoans', 'isSignature', 'issueTime', 'paidAmount', 'pledgeNo', 'productCategory',
              'productIdentifier', 'productName', 'productNo', 'issueProductPuHuiZhongYinCarRequest', 'issueProductPuHuiZhongYinDebtorBasicInfoRequest', 'issueProductPuHuiZhongYinHouseRequest', 'repaid', 'repaidTime', 'repaymentDeadline', 'returnMoneyMethod', 'riskManagementInfo', 'settleDate', 'soldOut', 'soldOutTime', 'specifyValueDate', 'startSellTime', 'unitPrice', 'usage', 'valueDate', 'valueDateMode', 'valueDays']
    result = [header]
    while current_page < end_page:
        projects = get_project_list(current_page)
        for project in projects:
            order_list = get_project_orders(project[-1])
            for order in order_list:
                result.append(project+order)
            if len(order_list) == 0:
                result.append(project)
            print('Get Project Info', project[2], project[-1], 'OK')
        print(current_time(), 'Page', current_page+1, 'OK')
        current_page += 1
    write_to_csv(result, '{}-{}页.csv'.format(start_page, end_page))


crawl_projects()
