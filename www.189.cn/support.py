from util import *
import json
from bs4 import BeautifulSoup
import time


def get_province():
    table = BeautifulSoup(
        open('./files/temp.html', 'r').read(), 'lxml').find_all('option')
    province_list = []
    for item in table:
        province_list.append(item.get('value'))
    print(province_list)


province_list = ['内蒙古', '山东', '贵州', '广西', '海南', '黑龙江', '山西', '西藏', '安徽', '福建', '甘肃', '天津', '河南',
                 '宁夏', '上海', '辽宁', '江苏', '北京', '湖北', '江西', '四川', '新疆', '河北', '广东', '湖南', '重庆', '陕西', '浙江', '云南']


def get_city(province):
    url = 'http://www.189.cn/dqmh/hallInfo.do?method=getCity'
    data = {
        'hallProvince': province
    }
    req = build_request(url, data=data)
    res_text = req.text
    city_list = [city for city in res_text.split(",") if city != 'null']
    return city_list


def get_area(city):
    url = 'http://www.189.cn/dqmh/hallInfo.do?method=getArea'
    data = {
        'hallCity': city
    }
    req = build_request(url, data=data)
    res_text = req.text
    area_list = [area for area in res_text.split(",") if area != 'null']
    return area_list


def get_all_area():
    for province in province_list:
        city_list = get_city(province)
        for city in city_list:
            f = open('./files/area_list', 'a')
            area_list = get_area(city)
            for area in area_list:
                f.write(json.dumps([province, city, area],
                                   ensure_ascii=False)+'\n')
            f.close()
            print(province, city, 'ok')


def query_service_hall(province, city, area):
    data = {
        'page': 0,
        'pageTotal': 0,
        'hallProvince': province,
        'hallCity': city,
        'hallArea': area,
        'Submit': '查询'
    }
    page = 1
    result = []
    while True:
        url = 'http://www.189.cn/dqmh/hallInfo.do?method=querysZqNew&pageNo={}'.format(
            page)
        req = build_request(url, data=data)
        hall_list = BeautifulSoup(req.text, 'lxml').find(
            'ul', {'class': 'dropd_entity'}).find_all('li')
        if len(hall_list) == 0:
            break
        for item in hall_list:
            line = []
            for p in item.find_all('p'):
                line.append(sub_str(p.get_text()))
            result.append(line)
        print(current_time(), province, city, area, page, 'OK')
        page += 1
    return result


def crawl_hall():
    for line in open('./files/area_list', 'r'):
        area_item = json.loads(line)
        try:
            result = query_service_hall(*area_item)
        except:
            print(*area_item,'fail')
            f = open('./files/fail', 'a')
            f.write(line)
            f.close()
            continue
        f = open('./files/result', 'a')
        for hall in result:
            f.write(json.dumps(area_item+hall,
                               ensure_ascii=False)+'\n')
        f.close()
        print(*area_item,'OK')

write_to_excel(load_txt('./files/result'),'电信营业厅数据.xlsx')
