import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import os

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def getshop(url):
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'mk-shops mt10 fr'}).find_all("a")
    try:
        maintitle=BeautifulSoup(html,'lxml').find('title').get_text().split('-')[0].replace('\r','').replace('\n','')
    except:
        maintitle='--'
    result=[]
    for item in table:
        try:
            title=item.get_text()
            try:
                i=item.find('i',{'class':'vvicon'}).get_text()
                title=title.replace(i,'')
            except:
                pass
            title=title.replace('\r','').replace('\n','').replace(' ','')
            url='http://www.vvic.com/'+item.get('href')
            result.append({'title':title,'url':url,'maintitle':maintitle})
        except:
            continue
    return result

def getitems(shop):
    page=1
    result=[]
    while True:
        try:
            html=requests.get(shop['url']+'?&currentPage=%s'%page,headers=headers,timeout=30).text
        except:
            time.sleep(2)
            print(shop['title'],page,'failed,retrying')
            continue
        table=BeautifulSoup(html,'lxml').find('div',{'class':'goods-list shop-list clearfix'}).find_all('div',{'class':'item'})
        if len(table)==0:
            break
        for item in table:
            try:
                imgurl='http:'+item.find('img').get('data-original')
                name=item.find('div',{'class':'title'}).find('a').get('title').replace('\r','').replace('\n','')
                itemurl='http://www.vvic.com/'+item.find('div',{'class':'title'}).find('a').get('href')
            except:
                continue
            try:
                price=item.find('div',{'class':'price'}).get_text().replace('\r','').replace('\n','').replace('\t','').replace(' ','')
            except:
                price='-'
            try:
                number=item.find('div',{'class':'j_clip_button'}).get_text().replace('\r','').replace('\n','')
            except:
                number=''
            result.append({'maintitle':shop['maintitle'],'title':shop['title'],'shopurl':shop['url'],'imgurl':imgurl,'name':name,'itemurl':itemurl,'price':price,'number':number})
        print(shop['title'],page,'ok')
        page+=1
        time.sleep(2)
    return result

def write_to_excel(maintitle):
    if maintitle=='--':
        maintitle='result'
    filename=maintitle
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in open('result.txt','r',encoding='utf-8'):
        line=line.replace('\n','')
        sheet.append(line.split('||'))
    excel.save('result/%s.xlsx'%filename)

def getimg(item):
    try:
        os.mkdir('result')
    except:
        pass
    try:
        os.mkdir('result/imgs')
    except:
        pass
    try:
        content=requests.get(item['imgurl'],headers=headers,timeout=30).content
        filename=item['itemurl'].split('/')[-1]+'.'+item['imgurl'].split('.')[-1]
        with open('result/imgs/'+filename,'wb') as img:
            img.write(content)
    except:
        return False
    return True

def main():
    while True:
        mainurl=input('输入链接(如：http://www.vvic.com/shops/12):')
        try:
            shops=getshop(mainurl)
        except:
            print('Failed!')
            continue
        break
    keys=['maintitle','title','name','price','number','imgurl','itemurl']
    f=open('result.txt','w',encoding='utf-8')
    for shop in shops:
        try:
            result=getitems(shop)
        except:
            print(shop['title'],'failed')
            continue
        for item in result:
            counter=0
            while True:
                if(getimg(item)):
                    break
                counter+=1
                if counter==3:
                    break
            line=''
            for key in keys:
                line+=item[key]+'||'
            filename=item['itemurl'].split('/')[-1]+'.'+item['imgurl'].split('.')[-1]
            filename=filename.replace('/','')
            line+=filename
            f.write(line+'\n')
    f.close()
    write_to_excel(item['maintitle'])

while True:
    try:
        main()
    except:
        print('Failed!')
    key=input("输入Y退出：")
    if key=='Y':
        break
