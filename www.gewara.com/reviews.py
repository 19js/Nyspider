import requests
from bs4 import BeautifulSoup
import openpyxl
import time


headers = {
    'X-Requested-With':"XMLHttpRequest",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    'Referer':"http://www.gewara.com/movie/282568860",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def getreviews(page,relatedid):
    html=requests.get('http://www.gewara.com/activity/ajax/sns/qryComment.xhtml?pageNumber={}&relatedid={}&topic=&issue=false&hasMarks=true&isCount=true&tag=movie&isPic=true&isVideo=false&userLogo=&newWalaPage=true&isShare=false&isNew=true&maxCount=200&isWide=true&isTicket=false'.format(page,relatedid),headers=headers).text
    table=BeautifulSoup(html,'lxml').find_all('div',{'class':'page_wala'})
    result=[]
    for item in table:
        try:
            grade=item.find('span',{'class':'ui_grades left ui_grade10'}).get('title')
            reviewid=item.find('div',{'class':'wala_txt'}).get('data-id')
            if reviewid==None:
                review=item.find('div',{'class':'wala_miniTxt'}).get_text().replace('\r','').replace('\n','').replace('\t','')
                result.append({'grade':grade,'review':review})
                continue
            result.append({'grade':grade,'id':reviewid})
        except:
            continue
    return result

def getcontent(id):
    html=requests.get('http://www.gewara.com/activity/sns/ajaxCommentDetail.xhtml?id=%s&isNew=true'%id).text
    text=BeautifulSoup(html,'lxml').get_text().replace('\r','').replace('\n','').replace('\t','')
    return text

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in open('result.txt','r'):
        item=eval(line)
        sheet.append([item['grade'],item['review']])
    excel.save('result.xlsx')

def main():
    f=open('result.txt','a')
    page=1
    count=0
    while True:
        try:
            result=getreviews(page,'282568860')
        except:
            print('failed')
            time.sleep(3)
            continue
        for item in result:
            try:
                dataid=item['id']
            except:
                count+=1
                print(count)
                f.write(str(item)+'\n')
                continue
            try:
                review=getcontent(dataid)
            except:
                continue
            item['review']=review
            f.write(str(item)+'\n')
            count+=1
            print(count)
            time.sleep(0.5)
        print(page,'ok')
        page+=1
        if page==200:
            break
    f.close()

write_to_excel()
