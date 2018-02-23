# encoding:utf-8

from util import *
from bs4 import BeautifulSoup
import codecs
import json


def get_item_list(date_limit, province):
    nodes = {
        '广东省': '44'
    }
    select_district = nodes[province]+'▓~'+province
    page = 1
    result = []
    while True:
        data = {
            'hidComName': "default",
            'TAB_QueryConditionItem': ['9f2c3acd-0256-4da2-a659-6949c4671a2a', 'ec9f9d83-914e-4c57-8c8d-2c57185e912a'],
            'TAB_QuerySubmitConditionData': "9f2c3acd-0256-4da2-a659-6949c4671a2a:{}|42ad98ae-c46a-40aa-aacc-c0884036eeaf:{}".format(date_limit, select_district.decode('utf-8').encode('GBK')),
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
                line=['http://www.landchina.com/'+item.find('a').get('href')]
            except:
                continue
            for td in item.find_all('td'):
                try:
                    line.append(td.get_text().replace('\r','').replace('\n',''))
                except:
                    line.append('')
            result.append(line)
            # try:
            #     item_url = 'http://www.landchina.com/' + \
            #         item.find('a').get('href')
            # except:
            #     continue
            # result.append(item_url)
        print(page, 'OK')
        if len(table) < 31:
            break
        page += 1
    return result

def crawl():
    current_date='2016-01-01'
    while current_date!='2018-02-23':
        date='-'.join([str(int(value)) for value in current_date.split('-')])
        try:
            result=get_item_list(date+'~'+date,'广东省')
        except:
            failed=codecs.open('failed.txt','a',encoding='utf-8')
            failed.write(current_date+'\n')
            failed.close()
            current_date=get_next_date(current_date)
            continue
        f=codecs.open('items.txt','a',encoding='utf-8')
        for item in result:
            f.write(json.dumps(item)+'\n')
        f.close()
        current_date=get_next_date(current_date)
        print(current_time(),current_date,'OK')

crawl()