import requests
from bs4 import BeautifulSoup
import openpyxl
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def invest(page):
    html=requests.get('http://newseed.pedaily.cn/invest/p'+str(page),headers=headers).text
    table=BeautifulSoup(html,'lxml').find('table',{'class':'record-table'}).find_all('tr')
    result=[]
    for tr in table:
        tds=tr.find_all('td')
        if len(tds)==0:
            continue
        line=[]
        for td in tds:
            try:
                line.append(td.get_text())
            except:
                line.append('')
        result.append(line)
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

def main():
    pagefrom=input("起始页:")
    pageto=input("结束页:")
    pagefrom=int(pagefrom)
    pageto=int(pageto)
    result=[]
    while pagefrom<=pageto:
        try:
            result+=invest(pagefrom)
        except:
            print(pagefrom,'failed')
            continue
        print(pagefrom,'ok')
        pagefrom+=1
        time.sleep(1)
    write_to_excel(result)

main()
