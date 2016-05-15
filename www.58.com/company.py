import requests
from bs4 import BeautifulSoup
import xlwt3
import imbox
import time


headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def getUrl():
    need_place=['http://sz.58.com/longgang/job/pn{}/?key=%E5%A4%96%E8%B4%B8&final=1&PGTID=0d302408-0071-58f4-3029-be8d66a87263&ClickID=1','http://sz.58.com/buji/job/pn{}/?key=%E5%A4%96%E8%B4%B8&final=1&PGTID=0d302408-0073-f61f-4c28-4b6858e1ad08&ClickID=2','http://sz.58.com/pingshanxinqu/job/pn{}/?key=%E5%A4%96%E8%B4%B8&final=1&PGTID=0d302408-02c5-3892-1dd5-f756b777b251&ClickID=1']
    try:
        exists=[line.replace('\n','') for line in open('exists.txt','r')]
    except:
        exists=[]
    result=[]
    for placeurl in need_place:
        page=1
        statue=True
        while statue:
            html=requests.get(placeurl.format(page),headers=headers).text
            table=BeautifulSoup(html,'lxml').find('div',id='infolist').find_all('dl')
            for item in table:
                url=item.find('a',{'class':'fl'}).get('href')
                if url in exists:
                    continue
                date=item.find_all('dd')[-1].get_text().replace('\r','').replace('\n','').replace(' ','')
                if date!='精准' and date!='今天':
                    statue=False
                    break
                if date=='今天':
                    com=[]
                    exists.append(url)
                    area=item.find_all('dd')[-2].get_text()
                    job=item.find('a').get_text()
                    companyname=item.find('a',{'class':'fl'}).get('title')
                    com=[companyname,job,area,url]
                    result.append(com)
            time.sleep(2)
            print(page,'--ok')
            page+=1

    f=open('exists.txt','w')
    for line in exists:
        f.write(line+'\n')
    f.close()
    return result

def companyInfor(url):
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'basicMsg'})
    baseinfor=table.find('table').get_text()
    print(baseinfor)

companyInfor('http://qy.58.com/23857034411527/?psid=191689477191801011918967017&entinfo=23575053058313_0&PGTID=0d302408-02c5-348c-ea66-a85c27a375b0&ClickID=1')
