from util import *
import json
from bs4 import BeautifulSoup


def get_bk_major_list():
    req = build_request('https://www.youzy.cn/major/index/bk')
    table = BeautifulSoup(req.text, 'lxml').find(
        'div', {'class': 'bk-major-list'}).find_all('div', {'class': 'content'})
    result = []
    for item in table:
        level_1 = item.find(
            'div', {'class': 'major-title'}).find('div').get_text()
        major_num_list = item.find_all('div', {'class': 'major-num'})
        ul_list = item.find_all('ul')
        for i in range(len(major_num_list)):
            level_2 = major_num_list[i].get_text()
            for li in ul_list[i].find_all('li'):
                level_3 = li.get_text()
                url = 'https://www.youzy.cn'+li.find('a').get("href")
                result.append([level_1, level_2, level_3, url])
    f = open('./files/bk_major', 'w')
    for major in result:
        f.write(json.dumps(major, ensure_ascii=False)+'\n')
    f.close()


def get_zk_major_list():
    req = build_request('https://www.youzy.cn/major/index/zk')
    table = BeautifulSoup(req.text, 'lxml').find(
        'div', {'class': 'bk-major-list'}).find_all('div', {'class': 'content'})
    result = []
    for item in table:
        level_1 = item.find(
            'div', {'class': 'major-title'}).find('div').get_text()
        major_num_list = item.find_all('div', {'class': 'major-num'})
        ul_list = item.find_all('ul')
        for i in range(len(major_num_list)):
            level_2 = major_num_list[i].get_text()
            for li in ul_list[i].find_all('li'):
                level_3 = li.get_text()
                url = 'https://www.youzy.cn'+li.find('a').get("href")
                result.append([level_1, level_2, level_3, url])
    f = open('./files/zk_major', 'w')
    for major in result:
        f.write(json.dumps(major, ensure_ascii=False)+'\n')
    f.close()


def get_major_info(major_id):
    req = build_request('https://www.youzy.cn/Majors/V3/Detail.aspx?majorId={}&mc='.format(major_id))
    detail = BeautifulSoup(req.text, 'lxml').find(
        'div', {'class': "major-detail"})
    result = {}
    major_con = detail.find('div', {'class': 'major-con'}).get_text()
    result['major_con'] = sub_str(major_con,append=['  '])
    base_info_list = detail.find(
        'div', {'class': 'base-info'}).find_all('div', {'class': 'mt20'})
    for item in base_info_list:
        key = item.find('p', {'class': 'title'}).get_text()
        p_list=item.find_all('p')
        value=''
        for p_item in p_list[1:]:
            value += p_item.get_text().replace('  ','')
        result[sub_str(key,append=['•'])] = value
    
    req=build_request('https://www.youzy.cn/Majors/V3/JobProspect.aspx?majorId={}&mc='.format(major_id))
    try:
        soup=BeautifulSoup(req.text,'lxml').find('div',{'class':'job-prospect'}).find('div',{'class':'mt30'})
        result['就业方向']=soup.find_all('p')[-1].get_text().replace('\r\n','').replace('  ','')
    except:
        pass
    return result

def crawl_major_info():
    for line in open('./files/bk_major','r'):
        major=json.loads(line)
        info=get_major_info(major[-1])
        info['base']=major
        f=open('./files/bk_result','a')
        f.write(json.dumps(info,ensure_ascii=False)+'\n')
        f.close()
        print(major,'OK')
    for line in open('./files/zk_major','r'):
        major=json.loads(line)
        info=get_major_info(major[-1])
        info['base']=major
        f=open('./files/zk_result','a')
        f.write(json.dumps(info,ensure_ascii=False)+'\n')
        f.close()
        print(major,'OK')

def load_major_info(filename):
    keys=['major_con', ' 专业简介', ' 培养目标', ' 培养要求', ' 名人学者', ' 主干课程', ' 学科要求', ' 知识能力', '就业方向']
    yield ['','','','']+keys
    for line in open(filename,'r'):
        major=json.loads(line)
        values=major['base']
        for key in keys:
            try:
                values.append(major[key])
            except:
                values.append('')
        yield values

#crawl_major_info()
write_to_excel(load_major_info('./files/bk_result'),'本科专业.xlsx')
write_to_excel(load_major_info('./files/zk_result'),'专科专业.xlsx')

                
        
    
    
