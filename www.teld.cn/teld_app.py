import requests
import openpyxl
import time
import os
import json


headers = {
    "Cookie": "TELDAppID=;domain=.teld.cn;path=/",
    #"Device": 'network=wifi&app_version=3.6.0&client=android&os_version=7.0&device_name=FRD-AL00&device_id=35CB60FD4C991B5C3EB3EC2523ADAB73&city_code=11&city_name=%E5%8C%97%E4%BA%AC&location_city_name=%E5%8C%97%E4%BA%AC&lat=40.067378&lng=116.307245',
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.0; FRD-AL00 Build/HUAWEIFRD-AL00)",
    "Host": "basesg.teld.cn",
}


class NetworkError(Exception):
    pass


def load_post_res_text(url, data, headers):
    for i in range(3):
        try:
            res_text = requests.post(
                url, data=data, headers=headers, timeout=20).text
            return res_text
        except Exception as e:
            print(e)
            continue
    raise NetworkError


def get_stations(city_code):
    stations_url = 'https://basesg.teld.cn/api/invoke?SID=BaseApi-App0304_SearchStation'
    page = 1
    need_keys = ['id', 'name', 'lng', 'lat',
                 'stationAddress', 'stationType', 'stationState','price','originalPrice','activityPrice']
    result = []
    while True:
        data = {
            "param": '''{
            "locationFilterType": "1", 
            "itemNumPerPage": "20", 
            "coordinateType": "gaode", 
            "keyword": "", 
            "pageNum": "%s", 
            "sortType": "1", 
            "lat": "40.067378", 
            "lng": "116.307245", 
            "locationFilterValue": "", 
            "cityCode": "%s"}''' % (page, city_code)
        }
        try:
            res_text = load_post_res_text(stations_url, data, headers)
        except:
            break
        data = json.loads(res_text)
        if(len(data['data']['stations']) == 0):
            break
        for item in data['data']['stations']:
            line = []
            for key in need_keys:
                try:
                    line.append((item[key]))
                except:
                    line.append('')
            result.append(line)
        if data['data']['currentPage'] == data['data']['pageCount']:
            break
        page += 1
    return result


def get_station_info(station_id):
    station_info_url = 'https://basesg.teld.cn/api/invoke?SID=BaseApi-App0304_GetTerminalOfStation'
    data = {
        "param": '''{
        "stationId":"%s",
        "keyword":"",
        "power":"15-360",
        "orderBy":""}''' % (station_id)
    }
    res_text = load_post_res_text(station_info_url, data, headers)
    data = json.loads(res_text)
    need_keys = ['terminalId', 'terminalCode', 'terminalName', 'terminalType',
                 'chargeInterface', 'stateName', 'stateCode', 'terminalTypeCode']
    result = []
    for item in data['data']:
        line = []
        for key in need_keys:
            try:
                line.append((item[key]))
            except:
                line.append('')
        result.append(line)
    return result


def get_cities():
    cities_url = 'https://basesg.teld.cn/api/invoke?SID=BaseApi-GetCities'
    data = {
        "timeStamp": int(time.time())
    }
    res_text = load_post_res_text(cities_url, data, headers)
    data = json.loads(res_text)
    result = []
    return data['data']['cities']


def get_charge_list(station_id):
    v_list_url = 'https://basesg.teld.cn/api/invoke/?SID=BaseApi-GetChargeListBySta'
    page = 1
    need_keys = ['carTypeName', 'userNickName', 'chargeTime']
    result = {}
    while True:
        data = {
            "filter": '''{
                "rows":"50",
                "confirmFilter":"",
                "keyword":"",
                "StaID":"%s",
                "page":%s}''' % (station_id, page)
        }
        try:
            res_text = load_post_res_text(v_list_url, data, headers)
        except:
            break
        data = json.loads(res_text)
        rows = data['data']['rows']
        for item in rows:
            line = []
            for key in need_keys:
                try:
                    line.append(item[key])
                except:
                    line.append('')
            key = item['PileName'].replace('交流','').replace('直流','')
            if key in result:
                result[key].append(line)
            else:
                result[key] = [line]
        if data['data']['pageNum'] == data['data']['pageCount']:
            break
        page += 1
    return result


def get_time():
    timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return timenow


def crawl(station, crawl_date):
    try:
        station_info_list = get_station_info(station[1])
    except Exception as e:
        try:
            print(station[0], station[2], 'Failed ', e)
        except:
            pass
        return
    try:
        charge_info = get_charge_list(station[1])
    except:
        charge_info = {}
    timenow = get_time()
    f = open('temp/' + crawl_date + '.txt', 'a', encoding='utf-8')
    for item in station_info_list:
        line = [timenow] + station + item
        terminal_name = item[2]
        if terminal_name in charge_info:
            line_name = [''] * len(line)
            line_time = [''] * len(line)
            for charge_item in charge_info[terminal_name]:
                line.append(charge_item[0])
                line_name.append(charge_item[1])
                line_time.append(charge_item[2])
            f.write(str(line) + '\r\n')
            f.write(str(line_name) + '\r\n')
            f.write(str(line_time) + '\r\n')
        else:
            f.write(str(line) + '\r\n')
    f.close()
    try:
        print(timenow, station[0], station[2], 'OK ')
    except:
        pass


def teld():
    try:
        os.mkdir('result')
    except:
        pass
    try:
        os.mkdir('temp')
    except:
        pass
    try:
        cities = get_cities()
    except Exception as e:
        print('Error ', e)
        return
    crawl_date = time.strftime('%Y_%m_%d')
    for city in cities:
        try:
            city_code = city['cityCode']
            city_name = city['cityName']
            stations = get_stations(city_code)
        except Exception as e:
            continue
        for station in stations:
            station = [city_name] + station
            crawl(station, crawl_date)
        try:
            print(city_name, 'OK')
        except:
            pass
    write_to_excel(crawl_date)
    print(get_time(), crawl_date, '抓取完成')


def write_to_excel(crawl_date):
    excel = openpyxl.Workbook(write_only=True)
    sheet = excel.create_sheet()
    for line in open('temp/' + crawl_date + '.txt', 'r', encoding='utf-8'):
        try:
            sheet.append(eval(line))
        except:
            continue
    excel.save('result/' + crawl_date + '.xlsx')


if __name__ == '__main__':
    # station_info=get_station_info('81d2973c-54d8-406f-826c-8feb86492511')
    # print(station_info)
    # print(get_charge_list('81d2973c-54d8-406f-826c-8feb86492511'))
    print('开始抓取')
    teld()
    input('')
