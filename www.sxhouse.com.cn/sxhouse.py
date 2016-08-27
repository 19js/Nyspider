import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import re
import os


headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def get_list(hid):
    html=requests.get('http://www.sxhouse.com.cn/com/ajaxpage/ajaxnewhousesall.aspx?hid='+str(hid),headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find_all('div',{'class':'cont'})
    result=[]
    for div in table:
        item={}
        date=div.find('h4').get_text().split(' ')[0]
        item['date']=date
        item['list']=[]
        for li in div.find_all('li'):
            try:
                house={}
                try:
                    housenum=re.findall('\d+幢',str(li))[0]
                except:
                    try:
                        housenum=li.find('p').get_text().split(' ')[0]
                    except:
                        housenum='-'
                house['housenum']=housenum
                try:
                    allnum=re.findall('总(\d+)套',str(li))[0]
                except:
                    allnum='-'
                house['allnum']=allnum
                try:
                    salednum=re.findall('已售：(\d+)套',str(li))[0]
                except:
                    salednum='-'
                house['salednum']=salednum
                history=re.findall('showHistoryCJ(\(\d+,\d+,\d+\))',str(li))[0]
                history=eval(history)
                house['pid']=history[0]
                house['hid']=history[1]
                house['secid']=history[2]
                item['list'].append(house)
            except:
                continue
        result.append(item)
    return result

def get_saledetail(house):
    html=requests.get('http://www.sxhouse.com.cn/Loupan/saledetail.aspx?pid=%s&hid=%s&sectionID=%s'%(house['pid'],house['hid'],house['secid']),headers=headers).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'floordetail'})
    house['saleable']={}
    house['saled']={}
    house['unable']={}
    house['anjie']={}
    house['yuding']={}
    house['fufang']={}
    keys=[]
    for item in soup.find_all('td',{'bgcolor':'#66ff66'}):
        if '商业' in str(item):
            continue
        try:
            areanum=re.findall("showFlow\('show_\d+',(.*?),.*?\)",str(item))[0]
            keys.append(areanum)
            try:
                house['saleable'][areanum]+=1
            except:
                house['saleable'][areanum]=1
        except:
            continue

    for item in soup.find_all('td',{'bgcolor':'#ffff66'}):
        if '商业' in str(item):
            continue
        try:
            areanum=re.findall("建筑面积：(.*?)㎡",str(item))[0]
            keys.append(areanum)
            try:
                house['saleable'][areanum]+=1
            except:
                house['saleable'][areanum]=1
        except:
            continue

    for item in soup.find_all('td',{'bgcolor':'#ff0000'}):
        if '商业' in str(item):
            continue
        try:
            areanum=re.findall("建筑面积：(.*?)㎡",str(item))[0]
            keys.append(areanum)
            try:
                house['saled'][areanum]+=1
            except:
                house['saled'][areanum]=1
        except:
            continue

    for item in soup.find_all('td',{'bgcolor':'#666666'}):
        if '商业' in str(item):
            continue
        try:
            areanum=re.findall("建筑面积：(.*?)㎡",str(item))[0]
            keys.append(areanum)
            try:
                house['unable'][areanum]+=1
            except:
                house['unable'][areanum]=1
        except:
            continue

    for item in soup.find_all('td',{'bgcolor':'#990000'}):
        if '商业' in str(item):
            continue
        try:
            areanum=re.findall("建筑面积：(.*?)㎡",str(item))[0]
            keys.append(areanum)
            try:
                house['anjie'][areanum]+=1
            except:
                house['anjie'][areanum]=1
        except:
            continue
    for item in soup.find_all('td',{'bgcolor':'#0033ff'}):
        if '商业' in str(item):
            continue
        try:
            areanum=re.findall("建筑面积：(.*?)㎡",str(item))[0]
            keys.append(areanum)
            try:
                house['yuding'][areanum]+=1
            except:
                house['yuding'][areanum]=1
        except:
            continue
    for item in soup.find_all('td',{'bgcolor':'#0099ff'}):
        if '商业' in str(item):
            continue
        try:
            areanum=re.findall("建筑面积：(.*?)㎡",str(item))[0]
            keys.append(areanum)
            try:
                house['fufang'][areanum]+=1
            except:
                house['fufang'][areanum]=1
        except:
            continue

    keys=list(set(keys))
    names=''
    for item in soup.find_all('tr')[-1].find_all('td'):
        names+=item.find('b').get_text()+';\n'
    house['names']=names
    house['keys']=keys
    return house

def main():
    while True:
        try:
            houseid=input('输入楼盘id:')
            if houseid=='':
                continue
            houseid=int(houseid)
            break
        except:
            continue
    try:
        houselist=get_list(houseid)
    except:
        print('Failed!')
        time.sleep(50)
        return
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    header=['日期','楼号','总套数','已售','面积','已售','面积','未售','面积','不可售','面积','按揭/抵押','面积','预订','面积','附房']
    sheet.append(header)
    for item in houselist:
        for house in item['list']:
            infor=get_saledetail(house)
            if len(infor['keys'])==0:
                line=[item['date'],infor['housenum'],infor['allnum'],infor['salednum']]
                sheet.append(line)
                sheet.append([])
                continue
            for key in infor['keys']:
                line=[item['date'],infor['housenum'],infor['allnum'],infor['salednum']]
                try:
                    line+=[key,infor['saled'][key]]
                except:
                    line+=[key,0]
                try:
                    line+=[key,infor['saleable'][key]]
                except:
                    line+=[key,0]
                try:
                    line+=[key,infor['unable'][key]]
                except:
                    line+=[key,0]
                try:
                    line+=[key,infor['anjie'][key]]
                except:
                    line+=[key,0]
                try:
                    line+=[key,infor['yuding'][key]]
                except:
                    line+=[key,0]
                try:
                    line+=[key,infor['fufang'][key]]
                except:
                    line+=[key,0]
                line.append(infor['names'])
                sheet.append(line)
            sheet.append([])
            print(item['date'],infor['housenum'],'ok')
    try:
        os.mkdir('result')
    except:
        pass
    excel.save('result/%s.xlsx'%houseid)

main()
