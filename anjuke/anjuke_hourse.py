import requests
from bs4 import BeautifulSoup
import openpyxl
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_url(url,page):
    html=requests.get(url+'/p'+str(page),headers=headers).text
    table=BeautifulSoup(html,'lxml').find('ul',id='houselist-mod').find_all('li',{'class':'list-item'})
    result=[]
    for li in table:
        item={}
        try:
            item['title']=li.find('a').get('title')
            item['url']=li.find('a').get('href')
        except:
            continue
        try:
            item['price']=li.find('div',{'class':'pro-price'}).find('span').get_text()
        except:
            pass
        result.append(item)
    return result

def get_infor(item):
    html=requests.get(item['url'],headers=headers).text
    soup=BeautifulSoup(html,'lxml').find('div',id='content')
    detail=soup.find('div',{'class':'houseInfo-detail'})
    tits=detail.find_all('dt')
    values=detail.find_all('dd')
    keys=[]
    for index in range(len(tits)):
        item[tits[index].get_text().replace('\r','').replace('\n','').replace(' ','').replace('：','')]=values[index].get_text()
    try:
        houseInfoBox=soup.find('div',{'class':'commuFacility-wrap'})
        item['评级']=houseInfoBox.find('div',{'class':'commuFacility-hot'}).get_text()
        item['tags']=houseInfoBox.find('div',{'class':"commuFacility-tags clearfix"}).get_text()
        tits=houseInfoBox.find('div',{'class':'commuFacility-detail clearfix'}).find_all('dt')
        values=houseInfoBox.find('div',{'class':'commuFacility-detail clearfix'}).find_all('dd')
        for index in range(len(tits)):
            item[tits[index].get_text().replace('\r','').replace('\n','').replace(' ','').replace('：','')]=values[index].get_text()
    except:
        pass
    return item

def main():
    url=input('Input url:')
    url=url.split('?')[0]
    url=url.split('#')[0]
    url=re.sub('/p\d+/','',url)
    print(url)
    page=1
    pre=[]
    f=open('result.txt','w',encoding='utf-8')
    while True:
        try:
            result=get_url(url,page)
        except:
            print('failed')
            break
        if pre==result:
            break
        if page==1:
            pre=result
        for item in result:
            try:
                hourse=get_infor(item)
            except:
                failed=open('failed.txt','a',encoding='utf-8')
                failed.write(str(item)+'\n')
                failed.close()
                continue
            f.write(str(hourse)+'\n')
            time.sleep(2)
            print(item['title'],'ok')
        print(page,'ok')
        page+=1
        if page==50:
            break
    f.close()
    write_to_excel()

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    keys=['title','url','price','小区', '位置', '年代', '类型', '房型', '面积', '朝向', '楼层', '装修程度', '房屋单价', '参考首付', '参考月供','tags','评级','小区名', '开发商', '物业公司', '物业类型', '物业费用', '总建面', '总户数', '建造年代', '容积率', '出租率', '停车位', '绿化率']
    sheet.append(keys)
    for line in open('result.txt','r',encoding='utf-8'):
        try:
            item=eval(line)
        except:
            continue
        hourse=[]
        for key in keys:
            try:
                hourse.append(item[key].replace('\r','').replace('\n','').replace('\t','').replace('\ue003','').replace('\ue002',''))
            except:
                hourse.append('-')
        sheet.append(hourse)
    excel.save('result.xlsx')

main()
