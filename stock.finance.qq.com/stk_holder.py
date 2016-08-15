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

def get_stkholder(name,stkcode):
    html=requests.get('http://stock.finance.qq.com/corp1/stk_holder.php?zqdm=%s'%stkcode,headers=headers).text
    soup=BeautifulSoup(html,'lxml').find('table',{'class':'list list_d'})
    date=soup.find('tr').find_all('span',{'class':'fntTahoma'})[-1].get_text()
    table=soup.find_all('tr')
    result=[]
    for tr in table[2:-1]:
        tds=tr.find_all('td')
        item=[name,stkcode,date]
        for td in tds:
            item.append(td.get_text())
        result.append(item)
    return result

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    filename=time.strftime("%Y%m%d %H%M%S",time.localtime())+'.xlsx'
    sheet=excel.create_sheet()
    for line in result:
        sheet.append(line)
    excel.save(filename)

def main():
    result=[]
    for line in open('stkcode.txt','r',encoding='utf-8'):
        title=line.replace('\r','').replace('\n','').split('---')
        try:
            items=get_stkholder(title[0],title[1])
        except:
            pass
            time.sleep(3)
            continue
        result+=items
        print(title[0],title[1],'ok')
        time.sleep(3)
    write_to_excel(result)

main()
