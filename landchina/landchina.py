# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import codecs
import json
import requests
import time
import openpyxl
import random
import datetime
import os

PROVINCE = '广东省'  # 设置爬取的省份
DATE_START = '2018-02-21'
DATE_END = '2018-02-22'


province_map = {
    '北京市': '11',
    '天津市': '12',
    '河北省': '13',
    '山西省': '14',
    '内蒙古': '15',
    '辽宁省': '21',
    '吉林省': '22',
    '黑龙江省': '23',
    '上海市': '31',
    '江苏省': '32',
    '浙江省': '33',
    '安徽省': '34',
    '福建省': '35',
    '江西省': '36',
    '山东省': '37',
    '河南省': '41',
    '湖北省': '42',
    '湖南省': '43',
    '广东省': '44',
    '广西壮族': '45',
    '海南省': '46',
    '重庆市': '50',
    '四川省': '51',
    '贵州省': '52',
    '云南省': '53',
    '西藏': '54',
    '陕西省': '61',
    '甘肃省': '62',
    '青海省': '63',
    '宁夏回族': '64',
    '新疆维吾尔': '65',
    '新疆建设兵团': '66'
}


def init_files():
    """
    初始化文件
    """
    try:
        os.mkdir('./files')
    except:
        pass
    for filename in os.listdir('./files/'):
        os.remove('./files/'+filename)


def get_headers():
    pc_headers = {
        "X-Forwarded-For": '%s.%s.%s.%s' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }
    return pc_headers


class NetWorkError(Exception):
    pass


def build_request(url, headers=None, data=None):
    """
    请求链接
    """
    if headers is None:
        headers = get_headers()
    for i in range(3):
        try:
            if data:
                response = requests.post(
                    url, data=data, headers=headers, timeout=20)
            else:
                response = requests.get(url, headers=headers, timeout=20)
            return response
        except:
            continue
    raise NetWorkError


def write_to_excel(lines, filename, write_only=True):
    """
    写入excel
    """
    excel = openpyxl.Workbook(write_only=write_only)
    sheet = excel.create_sheet()
    for line in lines:
        sheet.append(line)
    excel.save(filename)


def get_next_date(current_date='2017-01-01'):
    """
    获取下一天日期
    """
    current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
    oneday = datetime.timedelta(days=1)
    next_date = current_date+oneday
    return str(next_date).split(' ')[0]


def current_time():
    """
    获取当前时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S")


def get_item_list(date_limit, province):
    """
    爬取交易列表
    """
    select_district = province_map[province]+'▓~'+province
    page = 1
    result = []
    while True:
        data = {
            'hidComName': "default",
            'TAB_QueryConditionItem': ['9f2c3acd-0256-4da2-a659-6949c4671a2a', '42ad98ae-c46a-40aa-aacc-c0884036eeaf'],
            'TAB_QuerySubmitConditionData': "9f2c3acd-0256-4da2-a659-6949c4671a2a:{}|42ad98ae-c46a-40aa-aacc-c0884036eeaf:{}".format(date_limit, select_district).encode('GBK'),
            'TAB_QuerySubmitOrderData': "",
            'TAB_RowButtonActionControl': "",
            'TAB_QuerySubmitPagerData': page,
            'TAB_QuerySubmitSortData': ""
        }
        req = build_request(
            url='http://www.landchina.com/default.aspx?tabid=263', data=data)
        table = BeautifulSoup(req.text, 'lxml').find(
            'table', id='TAB_contentTable').find_all('tr')
        if '没有检索到相关数据' in str(table):
            break
        for item in table:
            try:
                line = ['http://www.landchina.com/'+item.find('a').get('href')]
            except:
                continue
            for td in item.find_all('td'):
                try:
                    line.append(td.get_text().replace(
                        '\r', '').replace('\n', ''))
                except:
                    line.append('')
            result.append(line)
        print(date_limit, 'Page', page, 'OK')
        if len(table) < 31:
            break
        page += 1
    return result


def parser_info_html(res_text):
    """
    解析供地结果信息页面
    """
    table = BeautifulSoup(res_text, 'lxml').find(
        'table', id='mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1')
    tr_ids = ['mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r17', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20',
              'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r12', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r23', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14']
    line = ''
    for trid in tr_ids:
        if trid == 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r12':
            try:
                trs = table.find('tr', id=trid).find(
                    'table', id='mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3').find_all('tr')
                text = '|分期支付约定:'
                for tr in trs:
                    if 'r2_tmp' in str(tr) or 'p1_f3_r1' in str(tr):
                        continue
                    for td in tr.find_all('td'):
                        text += td.get_text()+' '
            except:
                continue
        elif trid == 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21':
            try:
                tr = table.find('tr', id=trid)
            except:
                continue
            try:
                down = tr.find(
                    'td', id='mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c2').get_text()
            except:
                down = ''
            try:
                up = tr.find(
                    'td', id='mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c4').get_text()
            except:
                up = ''
            try:
                date = tr.find(
                    'td', id='mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21_c4').get_text()
            except:
                date = ''
            text = '|约定容积率下限:'+down+'|约定容积率上限:'+up+'|约定交地时间:'+date
        else:
            try:
                tds = table.find('tr', id=trid).find_all('td')
            except:
                continue
            text = ''
            for td in tds:
                text += '| '+td.get_text()
        line += text
    line = line.replace('\r', '').replace('\n', '').replace('\t', '').replace(
        '||', '|').replace('||', '|').replace('：', ':').replace(':|', ':')
    item = {}
    for key_value in line.split('|'):
        key = key_value.split(':')[0]
        key = key.replace(' ', '').replace('\xa0', '')
        if key == '':
            continue
        try:
            item[key] = key_value.split(':')[1]
        except:
            item[key] = ''
    if item['面积(公顷)'] == item['土地来源']:
        item['土地来源'] = '现有建设用地'
    elif float(item['土地来源']) == 0:
        item['土地来源'] = '新增建设用地'
    else:
        item['土地来源'] = '新增建设用地(来自存量库)'
    return item


def get_item_info(url):
    """
    获取结果信息，重试3次
    """
    for i in range(3):
        try:
            req = build_request(url)
            item = parser_info_html(req.text)
            item['url'] = url
            return item
        except:
            continue
    raise NetWorkError


def get_province_items():
    """
    爬取设置省份指定日期区间的所有列表数据
    """
    province = PROVINCE
    date_from = DATE_START
    date_to = DATE_END
    current_date = date_from
    while current_date != date_to:
        date = '-'.join([str(int(value)) for value in current_date.split('-')])
        try:
            result = get_item_list(date+'~'+date, province)
        except Exception as e:
            # 获取失败将日期写入date_failed文件
            failed = codecs.open('./files/date_failed.txt',
                                 'a', encoding='utf-8')
            failed.write(current_date+'\n')
            failed.close()
            current_date = get_next_date(current_date)
            continue
        f = codecs.open('./files/items.txt', 'a', encoding='utf-8')
        for item in result:
            f.write(json.dumps(item, ensure_ascii=False)+'\n')
        f.close()
        print(current_time(), 'Date:', current_date, 'OK')
        current_date = get_next_date(current_date)


def crawl_info():
    """
    爬取items.txt文件中每条交易的详细信息
    """
    for line in codecs.open('./files/items.txt', 'r', encoding='utf-8'):
        item = json.loads(line)
        try:
            info_item = get_item_info(item[0])
        except Exception as e:
            # 获取失败写入info_failed文件
            failed = codecs.open('./files/info_failed.txt',
                                 'a', encoding='utf-8')
            failed.write(line)
            failed.close()
            print(item[0], 'fail')
            continue
        with codecs.open('./files/result.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(info_item, ensure_ascii=False)+'\n')
        print(current_time(), item[0], 'OK')


def load_result():
    keys = ['行政区', '电子监管号', '项目名称', '项目位置', '面积(公顷)', '土地来源', '土地用途', '供地方式', '土地使用年限', '行业分类', '土地级别', '成交价格(万元)',
            '分期支付约定', '土地使用权人', '约定容积率下限', '约定容积率上限', '约定交地时间', '约定开工时间', '约定竣工时间', '实际开工时间', '实际竣工时间', '批准单位', '合同签订日期', 'url']
    yield keys
    for line in codecs.open('./files/result.txt', 'r', encoding='utf-8'):
        item = json.loads(line)
        line = []
        for key in keys:
            try:
                value = item[key]
                if '约定容积率' in key:
                    try:
                        num = float(value)
                    except:
                        value = ''
            except:
                value = ''
            line.append(value)
        yield line


init_files()
# 先爬取列表
get_province_items()
# 再爬取每条的详细信息
crawl_info()
# 将result.txt的数据写入excel
write_to_excel(load_result(), '{}_{}_{}.xlsx'.format(
    PROVINCE, DATE_START, DATE_END))
