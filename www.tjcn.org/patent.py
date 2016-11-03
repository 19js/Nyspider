import requests
from bs4 import BeautifulSoup
import time
import openpyxl


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_citys(url):
    html=requests.get(url,headers=headers).text.encode('iso-8859-1').decode('gbk','ignore')
    table=BeautifulSoup(html,'lxml').find('div',{'class':'content'}).find('table',{'class':'sy'}).find_all('tr')
    citys=[]
    for item in table:
        try:
            for i in item.find_all('td')[1].find_all('a'):
                try:
                    name=i.get_text()
                    url=i.get('href')
                    citys.append([name,url])
                except:
                    continue
        except:
            continue
    return citys

def get_text(url):
    html=requests.get(url,headers=headers,timeout=30).text.encode('iso-8859-1').decode('gbk','ignore')
    text=BeautifulSoup(html,'lxml').find('div',{'class':'viewbox'}).get_text().replace('\r','').replace('\n','').split('。')
    result=''
    page=2
    while True:
        page_url=url.replace('.html','_%s.html'%page)
        html=requests.get(page_url,headers=headers,timeout=30).text.encode('iso-8859-1').decode('gbk','ignore')
        if '您正在搜索的页面可能已经删除、更名或暂时不可用。' in html:
            break
        text+=BeautifulSoup(html,'lxml').find('div',{'class':'viewbox'}).get_text().replace('\r','').replace('\n','').split('。')
        page+=1
    for item in text:
        if '专利' in item:
            result+=item+'\n'
    return result

def get_failed():
    failed=[eval(line) for line in open('./failed.txt','r')]
    for item in failed:
        try:
            text=get_text('http://www.tjcn.org'+item[-1])
        except:
            failed=open('failed_1.txt','a')
            failed.write(str(item)+'\n')
            failed.close()
            continue
        f=open('result.txt','a')
        f.write(str([item[0],item[1:],text])+'\n')
        f.close()
        print(item)

def main():
    years={'2009':'http://www.tjcn.org/tjgbsy/nd/3595.html','2010':'http://www.tjcn.org/tjgbsy/nd/17848.html','2011':'http://www.tjcn.org/tjgbsy/nd/23306.html'}
    for key in years:
        citys=get_citys(years[key])
        for city in citys:
            try:
                text=get_text('http://www.tjcn.org'+city[1])
            except:
                failed=open('failed.txt','a')
                failed.write(str([key]+city)+'\n')
                failed.close()
                continue
            f=open('result.txt','a')
            f.write(str([key,city,text])+'\n')
            f.close()
            print(city,key)

def write_to_excel():
    data=[eval(line) for line in open('result.txt','r')]
    result={}
    for item in data:
        try:
            result[item[1][0]][item[0]]=item[-1]
        except:
            result[item[1][0]]={}
            result[item[1][0]][item[0]]=item[-1]
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    keys=['2009','2010','2011','2012','2013','2014','2015']
    for key in result:
        line=[]
        for year in keys:
            try:
                line.append(result[key][year])
            except:
                line.append('')
                print(year,key)
        sheet.append([key]+line)
    excel.save('result.xlsx')

write_to_excel()
