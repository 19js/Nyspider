from util import *
from bs4 import BeautifulSoup
import json
import threading
import random

URL = 'https://centricparts.centriccatalog.com/EcatMain.aspx'

T_URL = 'https://centricparts.centriccatalog.com/Inquiry/AppResult.aspx?id=WEB_PADS&v=LD/MD&y=1988&m=16&mm=83&uid=ANR&sid=0'


session_pool = []

PC_LOC = '_ali'

session_lock = threading.Lock()

THREAD_SIZE = 5


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


def create_session_pool(pool_size=40):
    global session_pool
    for i in range(pool_size):
        session = requests.session()
        try:
            session.get(URL, timeout=20)
        except:
            continue
        print('create session', i+1, 'OK')
        session_pool.append(session)


def load_session():
    global session_pool
    with session_lock:
        if len(session_pool) == 0:
            create_session_pool(THREAD_SIZE*2)
        session = session_pool.pop(0)
    return session


def get_model_value(value_item):
    url = URL + \
        '?id={}&v={}&y={}&m={}'.format(
            value_item[0][1], value_item[1][1], value_item[2][1], value_item[3][1])
    global session_pool
    for i in range(3):
        try:
            session = load_session()
            req = session.get(url, timeout=20, headers=get_headers())
            model_list = parser_select('ModelsDropdownlist', req.text)
            result = []
            for model_item in model_list:
                result.append(value_item+[model_item])
            if len(result) == 0:
                raise NetWorkError
            with session_lock:
                session_pool.append(session)
            return result
        except Exception as e:
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
        if len(items) < THREAD_SIZE:
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


def parser_table(html):
    table = BeautifulSoup(html, 'lxml').find(
        'table', {'id': 'AppDataGrid'})
    header = table.find('tr', {'class': 'header'}).find_all('td')
    keys = []
    for td in header:
        key = td.get_text().replace('\xa0', '').replace('\n', '')
        keys.append(key)
    tr_list = table.find_all('tr')
    result = []
    for tr in tr_list[1:]:
        td_list = tr.find_all('td')
        if len(td_list) != len(keys):
            continue
        line = {}
        for index in range(len(keys)):
            key = keys[index]
            if key == 'Pic':
                a_list = td_list[index].find_all('a')
                urls = []
                for a in a_list:
                    urls.append(
                        'https://centricparts.centriccatalog.com/Inquiry/' + a.get('href'))
                value = '\t\t'.join(urls)
                line[key] = value
                continue
            value = td_list[index].get_text().replace(
                '\xa0', '').replace('\n', '')
            if key in line:
                line[key] += '\t\t'+value
            else:
                line[key] = value
        result.append(line)
    td_list = tr_list[-1].find_all('td')
    page_value = []
    for td in td_list:
        page_value.append(td.get_text().replace(
            '\xa0', '').replace('\n', ''))

    return {
        'result': result,
        'page_value': page_value,
    }


def get_inquiry_result(value_item):
    url = 'https://centricparts.centriccatalog.com/Inquiry/AppResult.aspx' + \
        '?id={}&v={}&y={}&m={}&mm={}'.format(
            value_item[0][1], value_item[1][1], value_item[2][1], value_item[3][1], value_item[4][1])
    global session_pool
    for i in range(3):
        try:
            session = load_session()
            req = session.get(url, timeout=30, headers=get_headers())
            result = parser_table(req.text)
            result['url'] = url
            with session_lock:
                session_pool.append(session)
            return result
        except Exception as e:
            continue
    raise NetWorkError


class AppResult(threading.Thread):
    def __init__(self, item):
        super(AppResult, self).__init__()
        self.daemon = True
        self.item = item

    def run(self):
        self.status = False
        try:
            values = get_inquiry_result(self.item)
            self.result = {
                'result': values,
                'item': self.item
            }
            self.status = True
        except:
            pass


def load_id_v_year_make_model_items():
    items = []
    for line in open('./files/id_v_year_make_model'+PC_LOC, 'r'):
        try:
            item = json.loads(line)
        except:
            f = open('./files/fail'+PC_LOC, 'a')
            f.write(line)
            f.close()
            continue
        items.append(item)
        if len(items) < 20:
            continue
        yield items
        items = []
    yield items


def crawl_app_result():
    success_num = 0
    failed_num = 0
    for items in load_id_v_year_make_model_items():
        tasks = []
        for item in items:
            task = AppResult(item)
            tasks.append(task)
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        for task in tasks:
            if task.status:
                f = open('./files/result'+PC_LOC, 'a')
                f.write(json.dumps(task.result)+'\n')
                f.close()
                success_num += 1
            else:
                f = open('./files/fail'+PC_LOC, 'a')
                f.write(json.dumps(task.item)+'\n')
                f.close()
                failed_num += 1
        print(current_time(), success_num, failed_num)


crawl_models()
