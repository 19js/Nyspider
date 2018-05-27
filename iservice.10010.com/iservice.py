from util import *
import json
from bs4 import BeautifulSoup
import time


def load_city():
    f = open('./files/city.json', 'r')
    city_data = json.load(f)
    return city_data


def get_city_hall(province_code, city_code):
    url = 'http://iservice.10010.com/e3/static/life/listHallByPropertyNew?provinceCode={}&cityCode={}&page={}'
    page = 1
    result = []
    keys = ['epProvincename', 'epCityname', 'epName', 'epAddress']
    while True:
        req = build_request(url.format(province_code, city_code, page))
        res_data = req.json()
        if 'errorMessage' in res_data:
            break
        try:
            hall_list = res_data['BusinessHallList']
        except:
            continue
        for hall in hall_list:
            line = []
            for key in keys:
                line.append(hall[key])
            result.append(line)
        print(current_time(), province_code, city_code, page, 'OK')
        page += 1
    return result


def crawl_hall():
    city_data = load_city()
    provinces = city_data['provinces']
    city_list = city_data['citys']
    for index in range(len(provinces)):
        province_code = provinces[index][0]
        province_name = provinces[index][1]
        for city in city_list[index]:
            city_code = city[0]
            city_name = city[1]
            try:
                result = get_city_hall(province_code, city_code)
            except:
                f=open('./files/fail','a')
                f.write(json.dumps(provinces[index]+city,ensure_ascii=False)+'\n')
                f.close()
                continue
            f = open('./files/result', 'a')
            for hall in result:
                f.write(json.dumps(
                    [province_name, city_name]+hall, ensure_ascii=False)+'\n')
            f.close()
            print(current_time(),province_name,city_name,'OK')

write_to_excel(load_txt('./files/result'),'联通营业厅数据.xlsx')