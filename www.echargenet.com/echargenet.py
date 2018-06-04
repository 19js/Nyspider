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


class NetWorkError(Exception):
    pass


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
            print('Write to excel fail',e)
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
            print('load txt fail',e)
            continue
        yield item


def get_all_stations():
    url = 'http://www.echargenet.com/portal/station/simple'
    try:
        req = build_request(url)
        res_text = re.findall('callback\((.*)\)', req.text)[0]
        stations = json.loads(res_text)['data']
    except:
        return []
    return stations


def get_station_info(id):
    url = 'http://www.echargenet.com/portal/station/info?id={}'.format(id)
    try:
        req = build_request(url)
        res_text = re.findall('callback\((.*)\)', req.text)[0]
        station_info = json.loads(res_text)['data']
    except:
        return None
    keys = ['province', 'cityName', 'name', 'address', 'chargerNumDC', 'chargerNumAC',
            'businessTime', 'parkingFee', 'serviceFee', 'chargingFee', 'payTypeDesc', 'lat', 'lng']
    result = []
    for key in keys:
        try:
            result.append(station_info[key])
        except:
            result.append('')
    return result


def get_station_chargers(id):
    url = 'http://www.echargenet.com/portal/station/chargers?id={}'.format(id)
    try:
        req = build_request(url)
        res_text = re.findall('callback\((.*)\)', req.text)[0]
        chargers_list = json.loads(res_text)['data']
    except:
        return []
    reg_status = {1: "故障", 2: "空闲", 3: "使用", 4: "离线", 5: "使用"}
    result = []
    keys = ['area', 'stakeNo', 'chargerType', 'status', 'standardDesc', 'soc',
            'outPower', 'outVolt', 'current', 'voltage']
    for chargers in chargers_list:
        for item in chargers['chargers']:
            line = []
            for key in keys:
                try:
                    value = item[key]
                    if key == 'status':
                        value = reg_status[value]
                    line.append(value)
                except Exception as e:

                    line.append('')
            result.append(line)
    return result


def crawl():
    stations = get_all_stations()
    try:
        os.mkdir('./files/')
    except:
        pass
    try:
        os.mkdir('./result')
    except:
        pass
    current_date = current_time().split(' ')[0]
    filename = './files/'+current_date+'.txt'
    f = open(filename, 'a', encoding='utf-8')
    f.write(json.dumps(['province', 'cityName', 'name', 'address', 'chargerNumDC', 'chargerNumAC',
                        'businessTime', 'parkingFee', 'serviceFee', 'chargingFee', 'payTypeDesc', 'lat', 'lng']+['area', 'stakeNo', 'chargerType', 'status', 'standardDesc', 'soc',
                                                                                                                 'outPower', 'outVolt', 'current', 'voltage'], ensure_ascii=False)+'\n')
    f.close()
    for station in stations:
        station_id = station['id']
        station_info = get_station_info(station_id)
        chargers_list = get_station_chargers(station_id)
        f = open(filename, 'a', encoding='utf-8')
        for charge in chargers_list:
            f.write(json.dumps(station_info+charge, ensure_ascii=False)+'\n')
        f.close()
        try:
            print(current_time(), station_info[2])
        except:
            pass
    write_to_excel(load_txt(filename), './result/'+current_date+'.xlsx')


crawl()
input('完成')
