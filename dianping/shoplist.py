#coding:utf-8

import requests
import json
import xlwt3
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_data(url):
    html=requests.get(url,headers=headers).text
    data=json.loads(html)['shopBeans']
    return data

def shoplist():
    try:
        os.mkdir('data')
    except:
        print('--')
    items={'最佳餐厅':'http://www.dianping.com/mylist/ajax/shoprank?cityId=%s&shopType=10&rankType=score&categoryId=0','人气餐厅':'http://www.dianping.com/mylist/ajax/shoprank?cityId=%s&shopType=10&rankType=popscore&categoryId=0','口味最佳':'http://www.dianping.com/mylist/ajax/shoprank?cityId=%s&shopType=10&rankType=score1&categoryId=0','环境最佳':'http://www.dianping.com/mylist/ajax/shoprank?cityId=%s&shopType=10&rankType=score2&categoryId=0','服务最佳':'http://www.dianping.com/mylist/ajax/shoprank?cityId=%s&shopType=10&rankType=score3&categoryId=0'}
    citys={'北京':'2','上海':'1','广州':'4','深圳':'7','成都':'8','重庆':'9','杭州':'3','南京':'5','沈阳':'18','苏州':'6','天津':'10','武汉':'16','西安':'17','长沙':'344','大连':'19','济南':'22','宁波':'11','青岛':'21','无锡':'13','厦门':'15','郑州':'160'}
    excel=xlwt3.Workbook()
    sheet=excel.add_sheet('sheet')
    count=0
    for city in citys:
        for key in items:
            try:
                data=get_data(items[key]%(citys[city]))
            except:
                print('Error!')
                continue
            num=1
            for item in data:
                sheet.write(count,0,str(count+1))
                sheet.write(count,1,key)
                sheet.write(count,2,city)
                sheet.write(count,3,num)
                sheet.write(count,4,item['filterFullName'])
                sheet.write(count,5,item['mainRegionName'])
                sheet.write(count,6,item['refinedScore1'])
                sheet.write(count,7,item['refinedScore2'])
                sheet.write(count,8,item['refinedScore3'])
                sheet.write(count,9,item['avgPrice'])
                if '(' in item['filterFullName'] or '（' in item['filterFullName']:
                    sheet.write(count,10,'Y')
                else:
                    sheet.write(count,10,'N')
                num+=1
                count+=1
        print(city+'--OK')
        excel.save('data/data.xls')

shoplist()
