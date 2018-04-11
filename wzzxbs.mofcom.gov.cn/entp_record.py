from util import *
from bs4 import BeautifulSoup
import json
import time
import re
import threading


def load_exists():
    exists = {}
    for line in open('./files/records.txt', 'r'):
        item = json.loads(line)
        exists[item[-1]] = 1
    return exists


def get_record_list():
    page = 0
    exists = load_exists()
    count = 0
    while True:
        data = {
            'params.entpName': '',
            'page.currentPage': page,
            'page.limit': 35000,
            'page.option': 'next',
            'page.start': (page-1)*35000,
            'page.rowCount': 232155,
            'listGrid.col': '1:showRecordInfo(0),2,3,4',
            'listGrid.type': 'link,ro,ro,ro'
        }
        try:
            url = 'http://wzzxbs.mofcom.gov.cn/WebProSP/infoPub/record/loadRecordData.action'
            req = build_request(url, data=data)
            result = json.loads(req.text)['rows']
        except Exception as e:
            print(page, e, 'fail')
            continue
        f = open('./files/records.txt', 'a')
        for item in result:
            values = item['data']
            try:
                code = re.findall(
                    'showRecordInfo\(\"(.*?)\"\);', values[0])[-1]
            except:
                continue
            if code in exists:
                continue
            exists[code] = 1
            count += 1
            f.write(json.dumps(values+[code])+'\n')
        f.close()
        print(page, count, 'OK')
        page += 1


def get_record_info(record_id):
    url = 'http://wzzxbs.mofcom.gov.cn/WebProSP/infoPub/record/loadEntpRecordDetails.action?params.recordId=%s' % record_id
    req = build_request(url)
    table = BeautifulSoup(req.text, 'lxml').find('table').find_all('tr')
    types = ['合资', '合作', '独资', '股份制']
    business_types = ['设立备案', '变更备案']
    result = {}
    for item in table:
        try:
            key = item.find('th').get_text().replace('\r', '').replace(
                '\n', '').replace('\t', '').replace('\xa0', '')
            value = item.find('td').get_text().replace('\r', '').replace(
                '\n', '').replace('\t', '').replace('\xa0', '')
            result[key] = value
        except:
            pass

        if '企业类型' in str(item):
            inputs = item.find_all('input')
            ty_value = ''
            for i in range(len(inputs)):
                if 'checked' in str(inputs[i]):
                    ty_value = types[i]
                    break
            result['企业类型'] = ty_value

        if '业务类型' in str(item):
            inputs = item.find_all('input')
            ty_value = ''
            for i in range(len(inputs)):
                if 'checked' in str(inputs[i]):
                    ty_value = business_types[i]
                    break
            result['业务类型'] = ty_value

        if '投资者名称' in str(item):
            if 'table' in str(item):
                trs = item.find_all('tr')
                infors = []
                for tr in trs:
                    if '投资者名称' in str(tr):
                        continue
                    tds = tr.find_all("td")
                    line = []
                    for td in tds:
                        try:
                            line.append(td.get_text().replace('\r', '').replace(
                                '\n', '').replace('\t', '').replace('\xa0', ''))
                        except:
                            line.append('')
                    infors.append(line)
                result['投资者'] = infors
    return result


def load_records():
    items = []
    for line in open('./files/records.txt', 'r'):
        try:
            item = json.loads(line)
        except:
            f = open('./files/failed.txt', 'a')
            f.write(line)
            f.close()
            continue
        items.append(item)
        if len(items) < 5:
            continue
        yield items
        items = []
    yield items


class Record(threading.Thread):
    def __init__(self, base_info):
        super(Record, self).__init__()
        self.daemon = True
        self.base_info = base_info
        self.record_id = self.base_info[-1]

    def run(self):
        try:
            self.info = get_record_info(self.record_id)
            self.status = True
        except:
            self.status = False
            return
        self.result = self.info
        self.result['base_info'] = self.base_info


def crawl():
    success_num = 0
    failed_num = 0
    for items in load_records():
        tasks = []
        for item in items:
            task = Record(item)
            tasks.append(task)
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        for task in tasks:
            if task.status:
                f = open('./files/result.txt', 'a')
                f.write(json.dumps(task.result)+'\n')
                f.close()
                success_num += 1
            else:
                f = open('./files/failed.txt', 'a')
                f.write(json.dumps(task.base_info)+'\n')
                f.close()
                failed_num += 1
        print(current_time(), success_num, failed_num)


crawl()
