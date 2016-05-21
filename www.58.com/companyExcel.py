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

def getUrl():
    need_place=['http://sz.58.com/longgang/job/pn{}/?key=%E5%A4%96%E8%B4%B8&final=1&PGTID=0d302408-0071-58f4-3029-be8d66a87263&ClickID=1','http://sz.58.com/buji/job/pn{}/?key=%E5%A4%96%E8%B4%B8&final=1&PGTID=0d302408-0073-f61f-4c28-4b6858e1ad08&ClickID=2','http://sz.58.com/pingshanxinqu/job/pn{}/?key=%E5%A4%96%E8%B4%B8&final=1&PGTID=0d302408-02c5-3892-1dd5-f756b777b251&ClickID=1']
    result=[]
    urls=[]
    for placeurl in need_place:
        page=1
        statue=True
        while statue:
            try:
                html=requests.get(placeurl.format(page),headers=headers,timeout=30).text
                table=BeautifulSoup(html,'lxml').find('div',id='infolist').find_all('dl')
                for item in table:
                    url=item.find('a',{'class':'fl'}).get('href')
                    companyname=item.find('a',{'class':'fl'}).get('title')
                    if companyname in urls:
                        continue
                    urls.append(companyname)
                    date=item.find_all('dd')[-1].get_text().replace('\r','').replace('\n','').replace(' ','')
                    if date!='精准' and date!='今天' and '小时' not in date and '分钟' not in date:
                        statue=False
                        break
                    com=[]
                    area=item.find_all('dd')[-2].get_text()
                    job=item.find('a').get_text()
                    com=[companyname,job,area,url]
                    result.append(com)
            except:
                break
            time.sleep(2)
            print(page,'--ok')
            page+=1
    return result


def companyInfor(url):
    html=requests.get(url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'basicMsg'})
    try:
        instro=table.find('div',{'class':'compIntro'}).get_text().replace('\r','').replace('\n','').replace(' ','')
    except:
        instro=''
    td=table.find_all('td')
    th=table.find_all('th')
    result=[]
    labels=['公司地址','公司性质','公司行业','公司规模','企业网址']
    for title in labels:
        text=''
        for index in range(len(th)):
            if th[index].get_text().replace('\r','').replace('\n','').replace(' ','')==title:
                text=td[index].get_text().replace('\r','').replace('\n','').replace(' ','').replace('查看地图','')
        result.append(text)
    result.append(instro)
    return result

def main():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    count=0
    urls=getUrl()
    for item in urls:
        try:
            company=companyInfor(item[-1])
        except:
            continue
        print(count)
        count+=1
        sheet.append(item+company)
        time.sleep(1)
    excel.save('result.xls')

main()
