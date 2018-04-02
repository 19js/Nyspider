from util import *
from bs4 import BeautifulSoup
import json
import re
import threading
import time


def get_company_list():
    page = 1
    while True:
        try:
            req = build_request(
                'http://was.zhuhai.gov.cn:8182/was5/web/search?page={}&channelid=261794&perpage=1000&outlinepage=10'.format(page))
            table = BeautifulSoup(req.text, 'lxml').find(
                'table', {'style': 'BORDER-COLLAPSE: collapse'}).find_all('a')
        except Exception as e:
            print(page, 'fail', e)
            continue
        if len(table) == 0:
            break
        f = open('./files/company_list.txt', 'a')
        for item in table:
            try:
                name = item.get_text()
                url = item.get('href')
            except:
                continue
            f.write(json.dumps([name, url])+'\n')
        f.close()
        print(page, 'OK')
        page += 1


def get_address(scztbh):
    url = 'http://www.zhuhai.gov.cn/SSDJzzgs/ssgssearch?scztbh='+scztbh
    for i in range(3):
        try:
            req = build_request(url)
            data = json.loads(req.text.replace('null(', '').replace(')', ''))
            return data['SSADDRESS'][0]
        except Exception as e:
            print(e)
            continue
    return ''


def get_company_info(url):
    table = None
    for i in range(3):
        try:
            req = build_request(url)
            table = BeautifulSoup(req.text.encode('iso-8859-1').decode('gbk', 'ignore'),
                                  'lxml').find('table', {'class': 'printCommercial'}).find_all('td')
            break
        except:
            continue
    values = []
    for td in table:
        value = td.get_text().replace('\r', '').replace('\n', '').replace(
            '\t', '').replace('\xa0', '').replace('  ', '').replace('\u3000', '')
        values.append(value)
    result = {}
    for index in range(len(values)):
        key = values[index]
        if key in ['名称', '企业状态', '登记状态', '法定代表人', '成立日期', '核准日期', '最近一次核准日期', '商事主体类型', '登记机关']:
            try:
                value = values[index+1]
            except:
                value = ''
            result[key] = value
        if key == '注册资本' or key == '注册资金':
            try:
                text = values[index+1]
            except:
                result[key] = ''
                continue
            try:
                zczb = re.findall('zczb="(.*?)";', text)[0]
            except:
                zczb = ''
            try:
                ztlx = re.findall('ztlx="(.*?)";', text)[0]
            except:
                zltx = ''
            if zczb != '':
                if ztlx == '个体户' or ztlx == '农民专业合作经济组织':
                    zczb += '元'
                else:
                    zczb += '万元'
            result[key] = zczb
    try:
        scztbh = re.findall('scztbh:"(.*?)"', req.text)[0]
        address = get_address(scztbh)
    except Exception as e:
        address = ''
    try:
        tyshxydm = re.findall('tyshxydm="(.*?)";', req.text)[0]
    except:
        tyshxydm = ''
    result['tyshxydm'] = tyshxydm
    result['address'] = address
    return result


class Info(threading.Thread):
    def __init__(self, base_info):
        super(Info, self).__init__()
        self.base_info = base_info

    def run(self):
        self.status = False
        try:
            self.result = get_company_info(self.base_info[-1])
        except:
            return
        self.result['base_info'] = self.base_info
        self.status = True


def load_items():
    items = []
    for line in open('./files/company_list.txt', 'r'):
        try:
            item = json.loads(line)
        except:
            faild = open('./files/failed.txt', 'a')
            faild.write(line)
            faild.close()
            continue
        items.append(item)
        if len(items) < 5:
            continue
        yield items
        items = []
    yield items


def crawl():
    count = 0
    success_count = 0
    for items in load_items():
        tasks = []
        for item in items:
            task = Info(item)
            tasks.append(task)
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        for task in tasks:
            count += 1
            if task.status:
                f = open('./files/result.txt', 'a')
                f.write(json.dumps(task.result)+'\n')
                f.close()
                success_count += 1
            else:
                faild = open('./files/failed.txt', 'a')
                faild.write(json.dumps(task.base_info)+'\n')
                faild.close()
        print(current_time(), count, success_count, 'OK')


crawl()
