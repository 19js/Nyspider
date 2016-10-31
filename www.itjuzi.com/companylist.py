import requests
from bs4 import BeautifulSoup
import time
import openpyxl

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_companylist(page):
    html=requests.get('http://www.itjuzi.com/company?page=%s'%page,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'html.parser').find_all('ul',{'class':'list-main-icnset'})[1].find_all('li')
    if len(table)==0:
        return []
    result=[]
    for li in table:
        try:
            img=li.find('img').get('src').split('?')[0]
            title=li.find('p',{'class':'title'}).get_text()
            url=li.find('a').get('href')
            des=li.find('p',{'class':'des'}).get_text()
            tags=li.find('span',{'class':'tags'}).get_text()
            loca=li.find('span',{'class':'loca'}).get_text()
            date=li.find('i',{'class':'date'}).get_text()
            round=li.find('i',{'class':'round'}).get_text()
        except:
            continue
        result.append([img,title,url,des,tags,loca,date,round])
    return result

def write_to_excel(result):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    filename=time.strftime("%Y%m%d_%H%M%S",time.localtime())+'.xlsx'
    for line in result:
        sheet.append(line)
    excel.save(filename)

def loadcompany():
    companys=[]
    for line in open('result.txt','r',encoding='utf-8'):
        companys.append(line.replace('\r','').replace('\n',''))
    return companys

def main():
    try:
        companys=loadcompany()
    except:
        companys=[]
    page=1
    f=open('result.txt','w',encoding='utf-8')
    flag=False
    new_list=[]
    while True:
        try:
            result=get_companylist(page)
        except:
            time.sleep(5)
            continue
        if result==[]:
            break
        for item in result:
            line='||'.join(item)
            line=line.replace('\r','').replace('\n','').replace('\t','')
            if line in companys:
                flag=True
                break
            new_list.append(item)
            f.write(line+'\r\n')
        if flag:
            break
        print(page,'ok')
        page+=1
        time.sleep(3)
    for company in companys:
        f.write(company+'\r\n')
    f.close()
    write_to_excel(new_list)

main()
