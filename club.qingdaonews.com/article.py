import requests
from bs4 import BeautifulSoup
import openpyxl

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    'Cookie':'PHPSESSID=d2a521b9298f8691e4c37487b6657ac3; Hm_lvt_099a2f2a4f2c2f042dbd360b42309fc4=1482199772; Hm_lpvt_099a2f2a4f2c2f042dbd360b42309fc4=1482199852; CNZZDATA1000084976=1383072779-1482195841-null%7C1482195841; username=JarMrmn4olyPFzOAltjC0Q%3D%3D; password=jv2Y7Ga10EoO2Tn3W%2FY1plZvYz1QGqB2; NSC_dmvc=ffffffff09020e0445525d5f4f58455e445a4a423660',
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_article(endpage):
    page=1
    result=[]
    while True:
        url='http://club.qingdaonews.com/usercenter/mytopic.php?page=%s'%page
        try:
            html=requests.get(url,headers=headers,timeout=30).text
        except:
            continue
        table=BeautifulSoup(html,'lxml').find('div',{'class':'add_list'}).find_all('li')
        for li in table:
            try:
                url='http://club.qingdaonews.com'+li.find('a').get('href')
                title=li.find('a').get_text()
                result.append([title,url])
            except:
                continue
        if page==endpage:
            break
        print(page,'ok')
        page+=1
    return result

def main():
    result=get_article(168)
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in result:
        sheet.append(line)
    excel.save('urls.xlsx')

main()
