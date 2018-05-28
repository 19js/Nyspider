from util import *
from bs4 import BeautifulSoup
import time
import json
import threading


def get_weather_data(url):
    req = build_request(url)
    content = BeautifulSoup(req.text, 'lxml').find(
        'div', {'id': 'content'}).find('table').find_all('tr')
    result = []
    for tr in content:
        if '天气状况' in str(tr):
            continue
        td_list = tr.find_all('td')
        line = []
        for td in td_list:
            line.append(sub_str(td.get_text(), append=['  ']))
        result.append(line)
    return result


class MonthWeather(threading.Thread):
    def __init__(self, base_inf):
        super(MonthWeather, self).__init__()
        self.base_info = base_inf
        self.daemon = True

    def run(self):
        try:
            data = get_weather_data(self.base_info[-1])
            self.result = []
            for line in data:
                self.result.append(self.base_info+line)
            self.status = True
        except:
            self.status = False


def load_urls():
    items = []
    for line in open('./files/month_list', 'r'):
        try:
            item = sub_str(line).split(',')
        except:
            filename = './result/fail_month'
            f = open(filename, 'a')
            f.write(json.dumps(task.base_info, ensure_ascii=False)+'\n')
            f.close()
            continue
        items.append(item)
        if len(items) < 10:
            continue
        yield items
        items = []
    yield items


def crawl_weather_data():
    succ_num = 0
    fail_num = 0
    for items in load_urls():
        tasks = []
        for item in items:
            task = MonthWeather(item)
            tasks.append(task)
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        for task in tasks:
            if task.status:
                filename = './result/{}'.format(task.base_info[0])
                f = open(filename, 'a')
                for line in task.result:
                    f.write(json.dumps(line, ensure_ascii=False)+'\n')
                f.close()
                succ_num += 1
            else:
                filename = './result/fail_month'
                f = open(filename, 'a')
                f.write(json.dumps(task.base_info, ensure_ascii=False)+'\n')
                f.close()
                fail_num += 1
        print(current_time(), 'Success:', succ_num, 'Fail:', fail_num)

crawl_weather_data()