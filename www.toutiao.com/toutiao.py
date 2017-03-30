import requests
from bs4 import BeautifulSoup
import openpyxl
import json
import time

headers = {
    'Host':"www.toutiao.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    'X-Requested-With':'XMLHttpRequest',
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"}

def crawl(media_id):
    max_behot_time=0
    baseurl='http://www.toutiao.com/pgc/ma_mobile/?page_type=1&max_behot_time=%s&aid=&media_id=%s&count=10&version=2&as=479BB4B7254C150'
    result=[]
    page=1
    while True:
        url=baseurl%(max_behot_time,media_id)
        try:
            html=requests.get(url,headers=headers,timeout=30).text
            data=json.loads(html)
        except:
            continue
        if data['has_more']!=1:
            break
        max_behot_time=data['max_behot_time']
        table=BeautifulSoup(data['html'],'lxml').find_all('section')
        for item in table:
            try:
                title=item.find('h3').get_text()
                url=item.find('a').get('href')
                count=item.find('span',{'class':'label-count'}).get_text()
                comment=item.find('span',{'class':'label-comment'}).get_text()
                date=item.find('span',{'class':'time'}).get('title')
                line=[title,url,count,comment,date]
            except:
                continue
            result.append(line)
        print(page,'ok')
        page+=1
        time.sleep(1)
    return result

def write_to_excel(result):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in result:
        try:
            sheet.append(line)
        except:
            continue
    excel.save('result.xlsx')

def toutiao():
    media_id=input("输入media_id:")
    result=crawl(media_id)
    write_to_excel(result)

toutiao()
