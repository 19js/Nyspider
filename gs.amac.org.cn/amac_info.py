from util import *
from bs4 import BeautifulSoup
import time
import json
import threading


def get_amac_list():
    page = 0
    while True:
        try:
            url = 'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.7659440673420521&page={}&size=100'.format(
                page)
            req = build_request(url, json_data={'page': page})
            content_list = req.json()['content']
        except Exception as e:
            print(page, 'fail', e)
            continue
        if len(content_list) == 0:
            break
        f = open('./files/base_info', 'a')
        for item in content_list:
            f.write(json.dumps(item)+'\n')
        f.close()
        print(page, 'OK')
        page += 1


def get_amac_info(url):
    req = build_request(url)
    res_text = req.text.encode('iso-8859-1').decode('utf-8', 'ignore')
    soup = BeautifulSoup(res_text, 'lxml').find(
        'div', {'class': 'm-list-details'})
    titles = soup.find_all('td', {'class': 'td-title'})
    values = soup.find_all('td', {'class': 'td-content'})
    result = {}
    keys = []
    for i in range(len(titles)):
        key = titles[i].get_text().replace('&nbsp', '').replace('\r\n', '').replace(
            '\n\n', '').replace('  ', '').replace(':', '').replace('：', '')
        value = values[i].get_text().replace('&nbsp', '').replace(
            '\r\n', '').replace('\n\n', '').replace('  ', '')
        if value[0] == '\n':
            value = value[1:]
        result[key] = value
        keys.append(key)
    return result


def load_info():
    keys = ['机构诚信信息', '基金管理人全称(中文)', '基金管理人全称(英文)', '登记编号', '组织机构代码', '登记时间', '成立时间', '注册地址', '办公地址', '注册资本(万元)(人民币)', '实缴资本(万元)(人民币)', '企业性质', '注册资本实缴比例', '机构类型', '业务类型', '员工人数', '机构网址',
            '是否为会员', '当前会员类型', '入会时间', '法律意见书状态', '法定代表人/执行事务合伙人(委派代表)姓名', '是否有从业资格', '资格取得方式', '法定代表人/执行事务合伙人(委派代表)工作履历', '高管情况', '暂行办法实施前成立的基金', '暂行办法实施后成立的基金', '机构信息最后更新时间', '特别提示信息']
    for line in open('./files/result', 'r'):
        item = json.loads(line)
        values = []
        for key in keys:
            try:
                values.append(item[key])
            except:
                values.append('')
        yield values


class GetInfo(threading.Thread):
    def __init__(self, base_info):
        super(GetInfo, self).__init__()
        self.daemon = True
        self.base_info = base_info

    def run(self):
        try:
            self.info = get_amac_info(
                'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/'+self.base_info['url'])
            self.status = True
        except:
            self.status = False
            return
        self.result = self.info
        for key in self.base_info:
            self.result[key] = self.base_info[key]


def load_base_info_list():
    items = []
    for line in open('./files/base_info', 'r'):
        try:
            item = json.loads(line)
        except:
            continue
        items.append(item)
        if len(items) < 5:
            continue
        yield items
        items = []
    yield items


def crawl():
    success_num = 0
    fail_num = 0
    for items in load_base_info_list():
        tasks = []
        for item in items:
            task = GetInfo(item)
            tasks.append(task)
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        for task in tasks:
            if task.status:
                f = open('./files/result', 'a')
                f.write(json.dumps(task.result)+'\n')
                f.close()
                success_num += 1
            else:
                f = open('./files/faild', 'a')
                f.write(json.dumps(task.base_info)+'\n')
                f.close()
                fail_num += 1
        print(current_time(), success_num, fail_num)


crawl()
