import requests
import time
import openpyxl
import random
import datetime
import json
import re
import csv
import os


def get_headers():
    pc_headers = {
        "X-Forwarded-For": '%s.%s.%s.%s' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    return pc_headers


def get_ie_headers():
    headers = get_headers()
    headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'
    return headers


class NetWorkError(Exception):
    pass


def build_session_request(session, url, headers=None, data=None, json_data=None, timeout=15, try_times=3):
    if headers is None:
        headers = get_headers()
    for i in range(try_times):
        try:
            if data:
                response = session.post(
                    url, data=data, headers=headers, timeout=timeout)
            elif json_data:
                headers['Content-Type'] = 'application/json'
                response = session.post(
                    url, data=json.dumps(json_data), headers=headers, timeout=timeout)
            else:
                response = session.get(url, headers=headers, timeout=timeout)
            return response
        except Exception as e:
            continue
    raise NetWorkError


def build_request(url, headers=None, data=None, json_data=None, timeout=15, try_times=3):
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


def write_to_excel(lines, filename, write_only=True):
    excel = openpyxl.Workbook(write_only=write_only)
    sheet = excel.create_sheet()
    for line in lines:
        try:
            sheet.append(line)
        except Exception as e:
            print('Write to excel fail', e)
            continue
    excel.save(filename)


def write_to_csv(lines, filename):
    csvfile = open(filename, 'w', encoding='utf-8')
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for line in lines:
        spamwriter.writerow(line)
    csvfile.close()


def get_next_date(current_date='2017-01-01'):
    current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
    oneday = datetime.timedelta(days=1)
    next_date = current_date+oneday
    return str(next_date).split(' ')[0]


def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def load_txt(filename):
    for line in open(filename, 'r'):
        try:
            item = json.loads(line)
        except Exception as e:
            print('load txt fail', e)
            continue
        yield item


def sub_str(string, words=None, append=None):
    if words is None:
        words = ['\r', '\n', '\t', '\xa0']
    if append is not None:
        words += append
    string = re.sub('|'.join(words), '', string)
    return string

