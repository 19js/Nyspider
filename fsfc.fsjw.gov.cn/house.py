import requests
from bs4 import BeautifulSoup
import json
import openpyxl
import time


headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}


def get_buildings(house_id):
    html=requests.get('http://fsfc.fsjw.gov.cn/hpms_project/roomView.jhtml?id='+house_id,headers=headers).text
    table=BeautifulSoup(html,'html.parser').find('div',{'class':'lp-list-con'}).find('p',{'class':'bot-a'}).find_all('a')
    buildings=[]
    for item in table:
        name=item.get_text()
        building_id=item.get('id')
        buildings.append({'name':name,'id':building_id})
    return buildings

def buildinfor(building_id):
    html=requests.get('http://fsfc.fsjw.gov.cn/hpms_project/room.jhtml?id='+str(building_id),headers=headers).text
    data=json.loads(html)
    result=[]
    keys=['roomno','ghyt','jzmj','tnmj','zt']
    for item in data:
        build=[]
        for key in keys:
            try:
                if key in ['jzmj','tnmj']:
                    build.append(float(item[key]))
                    continue
                build.append(item[key])
            except:
                build.append('')
        result.append(build)
    return result

def main():
    house_id=input("输入楼盘id:")#楼盘链接中的id
    excel=openpyxl.Workbook(write_only=True)
    buildings=get_buildings(house_id)
    header=['房号','用途','总面积(㎡)','套内面积(㎡)','销售状态']
    count=0
    for item in buildings:
        sheet=excel.create_sheet(str(count))
        count+=1
        sheet.append([item['name']])
        sheet.append(header)
        result=buildinfor(item['id'])
        for line in result:
            sheet.append(line)
    filename=time.strftime('%Y%m%d_%H%M%S')+'.xlsx'
    excel.save(filename)

main()
