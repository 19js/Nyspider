import requests
from bs4 import BeautifulSoup
import openpyxl
import time

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_table(url):
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'html.parser').find('table',id='report1').find_all('tr')
    result=[]
    for tr in table[2:-3]:
        item=''
        for td in tr.find_all('td'):
            item+=td.get_text()+'|'
        result.append(item)
    return result

def main():
    text_f=open('2014_2016.txt','w',encoding='utf-8')
    startdate='2014-01-01'#起始日期
    enddate='2016-07-19'#结束日期
    startpage=1#起始页码
    endpage=10#结束页码
    while startpage<=endpage:
        url='http://datacenter.mep.gov.cn/report/air_daily/air_dairy.jsp?city=&startdate={}&enddate={}&page={}'.format(startdate,enddate,startpage)
        try:
            items=get_table(url)
        except:
            time.sleep(2)
            print(startpage,'-failed')
            continue
        for item in items:
            text_f.write(item+'\n')
        print(startpage,'-ok')
        startpage+=1
    text_f.close()
    write_to_excel()

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in open('2014_2016.txt','r',encoding='utf-8'):
        line=line.replace('\n','')
        sheet.append(line.split('|'))
    excel.save('2014_2016.xlsx')

main()
