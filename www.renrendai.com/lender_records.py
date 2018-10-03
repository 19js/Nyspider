# coding:utf-8
import json
import codecs
import csv
import requests
import random
import time


def get_headers():
    pc_headers = {
        "X-Forwarded-For": '%s.%s.%s.%s' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }
    return pc_headers


class NetWorkError(Exception):
    pass


def build_request(url, headers=None, data=None):
    if headers is None:
        headers = get_headers()
    for i in range(3):
        try:
            if data:
                response = requests.post(
                    url, data=data, headers=headers, timeout=30)
            else:
                response = requests.get(url, headers=headers, timeout=30)
            return response
        except:
            continue
    raise NetWorkError


def get_lender_records(loan_id):
    url = 'https://www.renrendai.com/pc/transfer/detail/loanInvestment?loanId={}'.format(
        loan_id)
    req = build_request(url)
    data = req.json()
    keys = ['loanId', 'id', 'lenderType', 'userId', 'userNickName',
            'financeCategory', 'orderNo', 'bussNo', 'amount', 'lendTime']
    if 'status' in data and data['status'] == 0:
        result = []
        base_info = []
        for lender in data['data']['list']:
            lender_line = []
            for key in keys:
                try:
                    value = lender[key]
                    if 'Time' in key:
                        try:
                            value = time.strftime(
                                '%Y-%m-%d %H:%M:%S', time.localtime(int(value)/1000))
                        except Exception as e:
                            print(e)
                    lender_line.append(value)
                except:
                    lender_line.append('')
            result.append(base_info+lender_line)
        return result
    return None


def append_to_csv_file(lines, filename):
    add_header = False
    if not os.path.exists(filename):
        add_header = True
    csvfile = codecs.open(filename, 'a', encoding='utf-8')
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
    if add_header:
        header = ['loanId', 'id', 'lenderType', 'userId', 'userNickName',
                  'financeCategory', 'orderNo', 'bussNo', 'amount', 'lendTime']
        spamwriter.writerow(header)
    for line in lines:
        spamwriter.writerow(line)
    csvfile.close()


def crawl():
    loan_id = 2121001
    loan_id_to = 2486529
    while loan_id < loan_id_to:
        try:
            result = get_lender_records(loan_id)
        except Exception as e:
            print('Fail', loan_id)
            continue
        if result is None:
            print('Fail', loan_id)
            continue
        append_to_csv_file(result, './files/人人贷散标数据-投标记录.csv')
        print(loan_id, 'OK')
        loan_id += 1


if __name__ == '__main__':
    try:
        import os
        os.mkdir('files')
    except:
        pass
    crawl()
