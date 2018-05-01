from util import *
from bs4 import BeautifulSoup
import json
import threading
import random

URL = 'https://centricparts.centriccatalog.com/EcatMain.aspx'

T_URL = 'https://centricparts.centriccatalog.com/Inquiry/AppResult.aspx?id=WEB_PADS&v=LD/MD&y=1988&m=16&mm=83&uid=ANR&sid=0'


session_pool = []


def get_products():
    req = build_request(URL)
    products = parser_select('CatalogsDropdownlist', req.text)
    return products


def parser_select(name, html):
    select_list = BeautifulSoup(html, 'lxml').find(
        'select', {'id': name}).find_all('option')
    result = []
    for option in select_list:
        value = option.get('value')
        if 'Select a' in value:
            continue
        key = option.get_text()
        result.append([key, value])
    return result


def get_vehicle_type():
    session = requests.session()
    session.get(URL)
    products = get_products()
    result = []
    for product, value in products:
        url = URL+'?id=%s' % (value)
        req = session.get(url)
        vehicle_list = parser_select('VehicleTypesDropDownList', req.text)
        for vehicle in vehicle_list:
            item = [[product, value], vehicle]
            result.append(item)
    f = open('./files/id_v', 'a')
    for line in result:
        f.write(json.dumps(line)+'\n')
    f.close()


def get_year_values():
    session = requests.session()
    session.get(URL)
    for line in open('./files/id_v', 'r'):
        item = json.loads(line)
        url = URL+'?id={}&v={}'.format(item[0][1], item[1][1])
        try:
            req = session.get(url)
            year_list = parser_select('YearsDropdownlist', req.text)
        except:
            print(item, 'fail')
            f = open('./files/id_v_fail', 'a')
            f.write(line)
            f.close()
            continue
        f = open('./files/id_v_year', 'a')
        for year_item in year_list:
            f.write(json.dumps(item+[year_item])+'\n')
        f.close()
        print(item, 'OK')


def get_make_values():
    session = requests.session()
    session.get(URL)
    for line in open('./files/id_v_year', 'r'):
        item = json.loads(line)
        url = URL+'?id={}&v={}&y={}'.format(item[0][1], item[1][1], item[2][1])
        try:
            req = session.get(url, timeout=20)
            make_list = parser_select('MakesDropdownlist', req.text)
        except:
            session = requests.session()
            session.get(URL, timeout=20)
            print(item, 'fail')
            f = open('./files/id_v_year_fail', 'a')
            f.write(line)
            f.close()
            continue
        f = open('./files/id_v_year_make', 'a')
        for make_item in make_list:
            f.write(json.dumps(item+[make_item])+'\n')
        f.close()
        print(item, 'OK')


def parser_table(html):
    table = BeautifulSoup(html, 'lxml').find(
        'table', {'id': 'AppDataGrid'}).find_all('tr')
    result = []
    for tr in table:
        td_list = tr.find_all('td')
        line = []
        for td in td_list:
            line.append(td.get_text())
        result.append(line)
    return result


def get_inquiry_result(value_item):
    url = 'https://centricparts.centriccatalog.com/Inquiry/AppResult.aspx' + \
        '?id={}&v={}&y={}&m={}&mm={}'.format(
            value_item[0][1], value_item[1][1], value_item[2][1], value_item[3][1], value_item[4][1])
    session = requests.session()
    session.get(URL)
    req = session.get(url)
    result = parser_table(req.text)


def create_session_pool():
    global session_pool
    for i in range(40):
        session = requests.session()
        try:
            session.get(URL, timeout=10)
        except:
            continue
        print('create session', i+1, 'OK')
        session_pool.append(session)


def get_model_value(value_item):
    url = URL + \
        '?id={}&v={}&y={}&m={}'.format(
            value_item[0][1], value_item[1][1], value_item[2][1], value_item[3][1])
    global session_pool
    if len(session_pool) == 0:
        create_session_pool()
    session = random.choice(session_pool)

    for i in range(3):
        try:
            req = session.get(url, timeout=20, headers=get_headers())
            model_list = parser_select('ModelsDropdownlist', req.text)
            result = []
            for model_item in model_list:
                result.append(value_item+[model_item])
            if len(result) == 0:
                raise NetWorkError
            return result
        except Exception as e:
            session_pool.remove(session)
            session = requests.session()
            session.get(URL, timeout=10, headers=get_headers())
            session_pool.append(session)
            continue
    raise NetWorkError


class ModelList(threading.Thread):
    def __init__(self, item):
        super(ModelList, self).__init__()
        self.item = item
        self.daemon = True

    def run(self):
        self.status = False
        try:
            self.result = get_model_value(self.item)
            if len(self.result) != 0:
                self.status = True
        except Exception as e:
            return


def load_id_v_year_make_items():
    items = []
    for line in open('./files/id_v_year_make', 'r'):
        try:
            item = json.loads(line)
        except:
            f = open('./files/id_v_year_make_fail', 'a')
            f.write(line)
            f.close()
            continue
        items.append(item)
        if len(items) < 20:
            continue
        yield items
        items = []
    yield items


def crawl_models():
    result = []
    success_num = 0
    failed_num = 0
    for items in load_id_v_year_make_items():
        tasks = []
        for item in items:
            task = ModelList(item)
            tasks.append(task)
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        for task in tasks:
            if task.status:
                f = open('./files/id_v_year_make_model', 'a')
                for line in task.result:
                    f.write(json.dumps(line)+'\n')
                f.close()
                success_num += 1
            else:
                f = open('./files/id_v_year_make_fail', 'a')
                f.write(json.dumps(task.item)+'\n')
                f.close()
                failed_num += 1
        print(current_time(), success_num, failed_num)


create_session_pool()
crawl_models()
