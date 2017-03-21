import requests
from bs4 import BeautifulSoup
import openpyxl
import json


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_all_market():
    url='http://www.mcdonalds.com.cn/ajaxs/get_all_marker'
    html=requests.get(url,headers=headers).text
    data=json.loads(html)
    return data

def get_store_infor(store_id):
    html=requests.get('http://www.mcdonalds.com.cn/ajaxs/get_marker_detail/'+str(store_id),headers=headers).text
    data=json.loads(html)
    result=[]
    keys=['name','city','province','address','phone_number']
    for key in keys:
        try:
            result.append(str(data[key]))
        except:
            result.append('')
    return result

def write_to_excel(result):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in result:
        sheet.append(line)
    excel.save('麦当劳.xlsx')

def main():
    markets=get_all_market()
    result=[]
    for item in markets:
        try:
            line=get_store_infor(item['id'])
        except:
            failed=open('failed.txt','a')
            failed.write(str(item)+'\n')
            failed.close()
            continue
        print(item)
        result.append(line)
    write_to_excel(result)

main()
