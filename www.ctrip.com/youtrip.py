import requests
from bs4 import BeautifulSoup
import time

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def getUrl():
    f=open('urls.txt','a')
    page=1
    while True:
        html=requests.get('http://you.ctrip.com/travels/guilin28/t3-p{}.html'.format(page),headers=headers).text
        table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'journalslist cf'}).find_all('a',attrs={'class':'journal-item cf'})
        for item in table:
            title=item.find('dt').get_text().replace('\r','').replace('\n','')
            f.write(title+'||'+item.get('href')+'\n')
        print(page,'--ok')
        page+=1
        if page==991:
            break
        time.sleep(2)
    f.close()

def getcontent(url):
    html=requests.get(url,headers=headers).text
    soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'ctd_content'})
    body=soup.get_text()
    place=soup.find('div',{'class':'ctd_content_controls cf'}).get_text()
    result=body.replace(place,'')
    return result


def main():
    excel=xlwt3.Workbook()
    sheet=excel.add_sheet('sheet')
    count=0
    for line in open('urls.txt','r'):
        line=line.replace('\n','')
        title=line.split('||')[0]
        url='http://you.ctrip.com'+line.split('||')[-1]
        try:
            content=getcontent(url)
        except:
            failed=open('failed.txt','a')
            failed.write(line+'\n')
            failed.close()
            continue
        sheet.write(count,0,count)
        sheet.write(count,1,title)
        sheet.write(count,2,content)
        count+=1
        excel.save('result.xls')
        time.sleep(2)
        print(count,'--ok')
        
