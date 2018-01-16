import requests
import time
import random
import json
import re
import os
import openpyxl

def get_headers():
    """
    构造请求头
    """
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


def build_request(url, headers=None):
    """
    获取url链接页面
    """
    if headers is None:
        headers = get_headers()
    #重试3次
    for i in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            return response
        except:
            continue
    raise NetWorkError


def get_wea_history(city_code, year,month):
    if year<2017:
        # 构造天气数据链接，两个链接可由抓包分析获得
        url='http://tianqi.2345.com/t/wea_history/js/%s_20%s%s.js'%(city_code,year,month)
    else:
        date_str='20%s%02d'%(year,month)
        url = 'http://tianqi.2345.com/t/wea_history/js/{}/{}_{}.js'.format(
            date_str, city_code, date_str)
    req = build_request(url)
    res_text = req.text
    try:
        # print(res_text) #打印页面信息
        # 正则取出taInfo
        tq_info = re.findall('tqInfo:\[(.*?)\]', res_text)[0]
    except:
        return[]
    #正则取出每天的天气信息
    items = re.findall("{([a-zA-Z]+:'.*?'|[a-zA-Z]+:'.*?',)}", tq_info)
    result = []
    for item in items:
        # 正则取出每个key-value对
        key_value_list = re.findall("([a-zA-Z]+):'(.*?)'", item)
        day={}
        for key,value in key_value_list:
            day[key]=value
        result.append(day)
    return result

def load_city_list():
    """
    加载城市列表
    """
    city_list=[]
    for line in open('./city.txt','r',encoding='utf-8'):
        city=json.loads(line)
        city_list.append(city)
    return city_list

def crawl():
    try:
        os.mkdir('files')
    except:
        pass
    city_list=load_city_list()
    for year in range(13,18):
        for month in range(1,13):
            for city in city_list:
                try:
                    result=get_wea_history(city['code'],year,month)
                except Exception as e:
                    print(e)
                    with open('failed.txt','a',encoding='utf-8') as f:
                        city['year']=year
                        city['month']=month
                        f.write(json.dumps(city)+'\n')
                    continue
                if len(result)==0:
                    continue
                f=open('./files/%s_%s.txt'%(city['pre_name'],city['name']),'a',encoding='utf-8')
                for day in result:
                    day['city']=city
                    f.write(json.dumps(day)+'\n')
                f.close()
            print(year,month,'OK')

def write_into_excel(lines,filename):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in lines:
        try:
            sheet.append(line)
        except Exception as e:
            print(e,line)
            continue
    excel.save(filename)

def load_txt(filename):
    keys=['ymd','bWendu','yWendu','tianqi','fengxiang','fengli','aqi','aqiInfo','aqiLevel']
    yield ['城市','区县']+keys
    for line in open(filename,'r',encoding='utf-8'):
        line=json.loads(line)
        item=[line['city']['pre_name'],line['city']['name']]
        for key in keys:
            try:
                item.append(line[key])
            except:
                item.append('')
        yield item
    

if __name__=='__main__':
    #crawl()
    try:
        os.mkdir('excel')
    except:
        pass
    for filename in os.listdir('./files/'):
        if '.txt' not in filename:
            continue
        write_into_excel(load_txt('./files/'+filename),'./excel/'+filename.replace('.txt','.xlsx'))
        print(filename,'OK')

        
