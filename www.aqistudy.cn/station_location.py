from bs4 import BeautifulSoup
import requests
import time
import json
import logging
import openpyxl


headers = {
        'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Host':'m.zq12369.com',
        'Referer':'https://m.zq12369.com/cityaqi.php',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}

def get_stations(city):
    url='https://m.zq12369.com/api/manageapi.php'
    data={
        'op':'getData',
        'city':city
    }
    html=requests.post(url,data=data,headers=headers,timeout=30).text
    response_data=json.loads(html)
    result=[]
    for item in response_data['point']:
        line=[item['cityname'],item['region'],item['pointlevel'],item['pointname'],item['longitude'],item['latitude']]
        result.append(line)
    return result

def stations_location():
    for line in open('./city.txt','r'):
        city=line.replace('\n','')
        try:
            result=get_stations(city)
        except Exception as e:
            print(city,'Failed')
            logging.exception(e)
            f=open('failed.txt','a')
            f.write(line)
            f.close()
            continue
        f=open('result.txt','a')
        for item in result:
            f.write(str(item)+'\n')
        f.close()
        print(city,'OK')

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in open('./result.txt','r'):
        item=eval(line)
        sheet.append(item)
    excel.save('result.xlsx')

write_to_excel()
