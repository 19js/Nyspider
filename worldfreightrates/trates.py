#coding:utf-8

import requests
import re
import xlrd
import xlwt3

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_port(name):
    name=name.replace(' ','+')
    count=0
    statue=True
    while statue:
        try:
            html=requests.get('http://worldfreightrates.com/calculator/ports?term=%s'%name,headers=headers,timeout=30).text
            statue=False
        except:
            count+=1
            if count==3:
                return False
            continue
    try:
        data=eval(html)
        Id=data[0]['id']
        return Id
    except:
        return False

def get_infor(fromid,toid,commodityName):
    url='http://worldfreightrates.com/en/calculator/ocean/rate?fromId='+fromid+'&toId='+toid+'&oceanType=FCL&commodityName='+commodityName+'&commodityValue=100&includeInsurance=false&includeReefer=false&includeHazardous=false&unit=lb&containerSize=40'
    html=requests.get(url,headers=headers,timeout=50).text.replace('\\','')
    rel='"result">(.*?)</p>'
    try:
        result=re.findall(rel,html)[0]
    except:
        result=''
    return result

def main():
    data = xlrd.open_workbook('data/data.xlsx')
    table = data.sheets()[0]
    excel=xlwt3.Workbook()
    sheet=excel.add_sheet('sheet')
    for row in range(table.nrows):
        print(row)
        fromport=table.cell(row,0).value
        toport=table.cell(row,1).value
        commodityName=table.cell(row,2).value
        Load_Type=table.cell(row,3).value
        fromid=get_port(fromport)
        toid=get_port(toport)
        if fromid==False or toid==False:
            sheet.write(row,0,fromport)
            sheet.write(row,1,toport)
            sheet.write(row,2,commodityName)
            sheet.write(row,3,Load_Type)
            sheet.write(row,4,'')
            excel.save('data/result.xls')
            continue
        try:
            result=get_infor(fromid,toid,commodityName.replace('&','%26').replace(' ','+').replace(',','%2C'))
        except:
            result=''
        sheet.write(row,0,fromport)
        sheet.write(row,1,toport)
        sheet.write(row,2,commodityName)
        sheet.write(row,3,Load_Type)
        sheet.write(row,4,result)
        excel.save('data/result.xls')
main()
