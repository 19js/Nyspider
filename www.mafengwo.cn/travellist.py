from util import *
from bs4 import BeautifulSoup
import time
import json
import re


def get_travellist(mddid):
    page = 1
    num = 0
    while True:
        data = {
            'mddid': mddid,
            'pageid': 'mdd_index',
            'sort': 2,
            'cost': 0,
            'days': 0,
            'month': 0,
            'tagid': 0,
            'page': page
        }
        try:
            req = build_request(
                'http://www.mafengwo.cn/gonglve/ajax.php?act=get_travellist', data=data)
            res_data = req.json()['list']
        except Exception as e:
            print(current_time(), mddid, page, 'fail', e)
            continue
        tn_list = BeautifulSoup(res_data, 'lxml').find_all(
            'div', {'class': 'tn-item'})
        f = open('./files/{}_tn_list'.format(mddid), 'a')
        for item in tn_list:
            tn_wrapper = item.find('div', {'class': 'tn-wrapper'})
            des = tn_wrapper.find('dd').get_text()
            if len(des) < 100:
                continue
            url_list = tn_wrapper.find('dt').find_all('a')
            url = url_list[-1].get('href')
            title = url_list[-1].get_text()
            user_name = tn_wrapper.find(
                'span', {'class': 'tn-user'}).get_text()
            f.write(json.dumps([title, user_name, url])+'\n')
            num += 1
        f.close()
        print(current_time(), mddid, page, num, 'OK')
        page += 1
        time.sleep(0.5)


def get_user_info(iid):
    url = 'http://pagelet.mafengwo.cn/note/pagelet/headOperateApi?params={{"iid":"{}"}}'.format(
        iid)
    req = build_request(url)
    soup = BeautifulSoup(req.json()['data']['html'], 'lxml')
    per_name = soup.find('a', {'class': 'per_name'}).get_text().replace(
        '\n', '').replace('  ', '')
    try:
        from_city = re.findall('\((.*?)\)', per_name)[0]
    except:
        from_city = ''
    try:
        p_time = soup.find('span', {'class': 'time'}).get_text()
    except:
        p_time = ''
    return [per_name, from_city, p_time]


def get_travel_info(url):
    user_info = get_user_info(url.split('/')[-1].split('.')[0])
    req = build_request(url)
    soup = BeautifulSoup(req.text, 'lxml').find('div', {'class': 'main'})
    view_con = soup.find('div', {'class': 'view_con'})
    content = view_con.get_text()
    tarvel_dir_list = view_con.find('div', {'class': 'tarvel_dir_list'})
    try:
        v_time = tarvel_dir_list.find(
            'li', {'class': 'time'}).get_text().split('/')[-1]
    except:
        v_time = ''
    try:
        day = tarvel_dir_list.find(
            'li', {'class': 'day'}).get_text().split('/')[-1]
    except:
        day = ''
    try:
        people = tarvel_dir_list.find(
            'li', {'class': 'people'}).get_text().split('/')[-1]
    except:
        people = ''
    try:
        cost = tarvel_dir_list.find(
            'li', {'class': 'cost'}).get_text().split('/')[-1]
    except:
        cost = ''
    return user_info+[v_time, day, people, cost, content]


def crawl_travel():
    mddid = '10065'
    # get_travellist(mddid)
    succ_num = 0
    fail_num = 0
    for line in open('./files/{}_tn_list'.format(mddid), 'r'):
        try:
            travel = json.loads(line)
        except:
            continue
        try:
            travel_info = get_travel_info('http://www.mafengwo.cn'+travel[-1])
        except:
            f = open('./files/fail_{}_tn_list'.format(mddid), 'a')
            f.write(line)
            f.close()
            fail_num += 1
            time.sleep(1)
            continue
        succ_num += 1
        f = open('./files/result_{}_tn_list'.format(mddid), 'a')
        f.write(json.dumps(
            travel+['http://www.mafengwo.cn'+travel[-1]]+travel_info)+'\n')
        f.close()
        print(current_time(), succ_num, fail_num)
        time.sleep(1)


crawl_travel()
