import requests
import json
import xlwt
import time
import chardet
import os
import re
import random


def get_headers():
    headers = {
        "X-Forwarded-For": '%s.%s.%s.%s' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        'Host': "wx.starcharge.com",
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; FRD-AL00 Build/HUAWEIFRD-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    return headers


def get_city_list():
    city_list_url = 'https://wx.starcharge.com/weChat.cityList.htm?from=list&sLat=39.9112&sLng=116.414&lat=&lng='
    html = requests.get(city_list_url, headers=get_headers(), timeout=20).text
    city_list = re.findall('"id":"(\d+)","name":"(.*?)"', html)
    return city_list


def get_stations(city_code):
    data = {
        "FRAMEparams": '{"city":%s,"screenItems":"","orderClause":0,"lng":114.42824029332,"lat":30.515423064794}' % (city_code)
    }
    res_text = requests.post(
        'https://wx.starcharge.com/api/weChat.findStubGroup', data=data, headers=get_headers()).text
    res_data = json.loads(res_text)
    result = []
    if res_data['code'] != '200':
        return result
    for item in res_data['data']['data']:
        try:
            line = [item['id'], item['name'], item['address'], item['tel'],
                    item['gisBd09Lat'], item['gisBd09Lng'], item['totalFee'], item['totalFeeInfo']]
        except Exception as e:
            continue
        result.append(line)
    return result


def get_stub_info(stub_group_id):
    data = {
        "FRAMEparams": '{"stubGroupId":"%s"}' % (stub_group_id)
    }
    res_text = requests.post('https://wx.starcharge.com/api/weChat.getStubGroup',
                             data=data, headers=get_headers(), timeout=20).text
    res_data = json.loads(res_text)
    if res_data['code'] != '200':
        print('[get_stub_info][%s] failed' % stub_group_id)
        return []
    result = []
    for item in res_data['data']['data']['stubList']:
        try:
            line = [item['id'], item['name'], item['modelNo'],
                    item['type'], item['kw'], item['existsGun'], item['status']]
        except:
            continue
        result.append(line)
    return result


def try_func(func, try_count=5):
    for i in range(try_count):
        try:
            result = func()
            return result
        except:
            continue
    return None


def try_func_with_arguments(func, arg, try_count=5):
    for i in range(try_count):
        try:
            result = func(arg)
            return result
        except:
            continue
    return None


def crawl(crawl_date, city):
    stations = try_func_with_arguments(get_stations, city[0])
    if stations == None:
        print('[crawl][get_stations]failed')
        return
    f = open('temp/' + crawl_date + '.txt', 'a', encoding='utf-8')
    for station in stations:
        timenow = get_time()
        stubs = get_stub_info(station[0])
        line = [timenow]
        for stub in stubs:
            f.write(str(line + city + station + stub) + '\r\n')
    f.close()


def get_time():
    timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return timenow


def write_to_excel(crawl_date):
    header = ['time', 'city_id', 'city_name', 'station_id', 'station_name', 'address', 'tel', 'gisBd09Lat',
              'gisBd09Lng', 'totalFee', 'totalFeeInfo', 'stub_id', 'stub_name', 'modelNo', 'type', 'kw', 'existsGun', 'status']
    excel = xlwt.Workbook()
    table = excel.add_sheet('table')
    for index in range(len(header)):
        table.write(0, index, header[index])
    line_num = 1
    for line in open('temp/' + crawl_date + '.txt', 'r', encoding='utf-8'):
        try:
            values = eval(line)
            for index in range(len(values)):
                table.write(line_num, index, values[index])
            line_num += 1
        except:
            continue
    excel.save('result/' + crawl_date + '.xls')


def starcharge():
    try:
        os.mkdir('result')
    except:
        pass
    try:
        os.mkdir('temp')
    except:
        pass
    crawl_date = time.strftime('%Y_%m_%d')
    city_list = try_func(get_city_list)
    if city_list == None:
        print('[starcharge][get_city_list]failed')
        return
    for city in city_list:
        crawl(crawl_date, list(city))
        print(city, 'OK')
    write_to_excel(crawl_date)
    print(get_time(), crawl_date, '抓取完成')


if __name__ == '__main__':
    starcharge()
    time.sleep(3000)
