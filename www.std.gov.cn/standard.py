from util import *
from bs4 import BeautifulSoup
import re
import json


def get_standard_list(page):
    url = 'http://www.std.gov.cn/gb/search/gbQueryPage?searchText=&ics=&state=&ISSUE_DATE=&sortOrder=asc&pageSize=50&pageNumber={}'.format(
        page)
    req = build_request(url)
    data = req.json()
    return data['rows']


def get_standard_info(id):
    url = 'http://www.std.gov.cn/gb/search/gbDetailed?id={}'.format(id)
    req = build_request(url)
    html = req.text.replace('\r', '').replace('\n', '').replace('\t', '')
    base_info_text = re.findall('基础信息</h2></div>(<div.*?</dl></div>)', html)[0]
    base_info = BeautifulSoup(base_info_text, 'lxml')
    names = base_info.find_all('dt', {'class': 'basicInfo-item name'})
    values = base_info.find_all('dd', {'class': 'basicInfo-item value'})
    result = {}
    for i in range(len(names)):
        name = names[i].get_text()
        value = values[i].get_text()
        result[name] = value
    result['起草单位'] = []
    try:
        company_info_text = re.findall(
            '起草单位</h2></div>(<div.*?</dl></div>)', html)[0]
        company_info = BeautifulSoup(company_info_text, 'lxml').find_all("dd")
    except:
        company_info = []
    for company in company_info:
        result['起草单位'].append(company.get_text())
    result['起草人'] = []
    try:
        person_info_text = re.findall(
            '起草人</h2></div>(<div.*?</dl></div>)', html)[0]
        person_info = BeautifulSoup(person_info_text, 'lxml').find_all("dd")
    except:
        person_info = []
    for person in person_info:
        result['起草人'].append(person.get_text())
    return result


def crawl_national_standard():
    page = 1
    while True:
        standard_list = get_standard_list(page)
        f = open('./files/national_standard.txt', 'a')
        for standard in standard_list:
            try:
                info = get_standard_info(standard['id'])
            except:
                failed=open('./files/failed_national_standard.txt','a')
                failed.write(json.dumps(standard)+'\n')
                failed.close()
                continue
            standard['info'] = info
            print(standard['id'],'OK')
            f.write(json.dumps(standard)+'\n')
        f.close()
        print(page,'OK')
        page += 1


def load_standard_txt():
    keys=['id','C_STD_CODE','C_C_NAME','ISSUE_DATE','ACT_DATE','STATE']
    info_keys=['全部代替标准','归口单位','执行单位','主管部门']
    yield keys+info_keys+['起草单位','起草人']
    for line in open('./files/national_standard.txt','r'):
        item=json.loads(line)
        standard=[]
        for key in keys:
            try:
                standard.append(item[key])
            except:
                standard.append('')
        info=item['info']
        for key in info_keys:
            try:
                standard.append(info[key])
            except:
                standard.append('')
        standard.append(','.join(info['起草单位']))
        standard.append(','.join(info['起草人']))
        yield standard
        

write_to_excel(load_standard_txt(),'国家标准.xlsx')
