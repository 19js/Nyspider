import requests
from bs4 import BeautifulSoup
import os
import time
import threading
import copy

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_department(hospital_id):
    html=requests.get('http://yyghwx.bjguahao.gov.cn/hp/search4department.htm?hId=%s&type=1'%hospital_id, headers=headers,timeout=30).text
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
    html=requests.get(url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'html.parser').find('ul',{'class':'date_nr_ul'}).find_all('li')
    result=[]
    for li in table:
        try:
            a=li.find('a')
            class_name=a.get('class')[0]
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
    html=requests.get(url,headers=headers,timeout=30).text
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

class Book(threading.Thread):
    def __init__(self,department):
        super(Book,self).__init__()
        self.department=department

    def run(self):
        self.result=[]
        try_count=0
        while True:
            try:
                ok_list=ok_date(self.department)
                break
            except:
                try_count+=1
                if try_count==4:
                    ok_list=[]
                    break
        for item in ok_list:
            try_count=0
            while True:
                try:
                    self.result+=register_infor(item)
                    break
                except:
                    try_count+=1
                    if try_count==4:
                        break

def update_infor(departments):
    result=[]
    while len(departments):
        count=0
        threadings=[]
        while count<10:
            try:
                department=departments.pop()
                count+=1
            except:
                break
            work=Book(department)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()
        for work in threadings:
            work.join()
        for work in threadings:
            result+=work.result
        threadings.clear()
        return result
    return result

def sound():
    '''
    clip=mp3play.load('./2.mp3')
    clip.play()
    time.sleep(4)
    clip.stop()
    '''
    os.system('./2.mp3')

def local_time():
    loc_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    return loc_time

def main():
    try:
        os.mkdir('result')
    except:
        pass
    departments=get_department('1')
    try:
        sleep_time=int(input('输入间隔时间(s)：'))
    except:
        sleep_time=60
    template="\r\n医院:%s\r\n科室:%s\r\n医院号源:%s\r\n医生:%s\r\n费用:%s\r\n"
    items=[]
    while True:
        print(local_time(),"开始抓取")
        text='\r\n-------------------\r\n查找时间:%s\r\n-------------------\r\n'%local_time()
        depart_items=copy.deepcopy(departments)
        result=update_infor(depart_items)
        for item in result:
            text+=template%tuple(item)
        if len(items)!=len(result):
            print("有更新")
            f=open("result/result.txt",'a',encoding='utf-8')
            f.write(text)
            f.close()
        items=result
        print(local_time(),"抓取完成\nSleep...")
        time.sleep(sleep_time)

main()
