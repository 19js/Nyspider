import requests
from bs4 import BeautifulSoup
import os
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_department(hospital_id):
    html=requests.get('http://yyghwx.bjguahao.gov.cn/hp/search4department.htm?hId=%s&type=1'%hospital_id, headers=headers).text
    table=BeautifulSoup(html,'html.parser').find('div',{'class':'xuanzekshi_box_list'}).find_all('li')
    departments=[]
    for item in table:
        try:
            url=item.find('a').get('href').replace('javascript:getDeptDutySource','').replace(';','')
            department=eval(url)
            departments.append(department)
        except:
            continue
    return departments

def ok_date(department):
    url='http://yyghwx.bjguahao.gov.cn/common/dutysource/appoints/%s,%s.htm?departmentName=%s&type=%s'%department
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'html.parser').find('ul',{'class':'date_nr_ul'}).find_all('li')
    result=[]
    for li in table:
        try:
            a=li.find('a')
            class_name=a.get('class')[0]
            print(class_name)
            if class_name=='data_bgcol3':
                continue
            url=a.get('href')
            item=url.replace('javascript:getDeptDutySourceByDate','').replace(';','')
            result.append(eval(item))
        except:
            continue
    return result

def register_infor(item):
    url=url='http://yyghwx.bjguahao.gov.cn/common/dutysource/appoint/%s,%s.htm?departmentName=%s&dutyDate=%s'%item
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'html.parser').find('div',{'class':'hyxzym_box'}).find_all('div',{'class':'hyxzym_b_sj'})
    result=[]
    for div in table:
        try:
            hospital='北京协和医院'
            department_name=item[2]
            date=item[-1]
            if '约满' in str(div):
                continue
            if '电话预约' in str(div):
                date=date+'（114电话预约可挂号）'
            if '微信预约' in str(div):
                date+='（微信预约）'
            spans=div.find_all('span')
            doctor=spans[0].get_text().replace('\xa0','')
            price=spans[1].get_text().replace('\xa0','')
            result.append([hospital,department_name,date,doctor,price])
        except:
            continue
    return result

def update_infor(departments):
    for department in departments:
        ok_list=ok_date(department)
        for item in ok_list:
            result=register_infor(item)
            print(result)

def main():
    departments=get_department('1')
    update_infor(departments)

main()
