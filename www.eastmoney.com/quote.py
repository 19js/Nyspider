import requests
import openpyxl
import json


def get_data(code,market):
    url='http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/CompatiblePage.aspx?Type=OB&stk=%s&Reference=xml&limit=0&page=%s'
    html=requests.get(url%(code+market,1)).text
    data=json.loads(html.replace('var jsTimeSharingData=','').replace(';','').replace('pages','"pages"').replace('data','"data"'))
    if data['pages']==0:
        return False
    pages=data['pages']
    page=2
    result=[]
    for item in data['data']:
        result.append(item.split(','))
    while page<=pages:
        html=requests.get(url%(code+market,page)).text
        data=json.loads(html.replace('var jsTimeSharingData=','').replace(';','').replace('pages','"pages"').replace('data','"data"'))
        for item in data['data']:
            result.append(item.split(','))
        page+=1
    return result

def write_to_excel(code,result):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for item in result:
        sheet.append(item)
    excel.save('%s.xlsx'%code)
    print(code,'OK')

def main():
    try:
        code=input('输入股票代码：')
    except:
        print("Faliled")
        return
    result=[]
    for market in ['1','2']:
        try:
            result=get_data(code,market)
        except:
            continue
        if result==False:
            continue
        break
    if result==[] or result==False:
        print('Failed')
        return
    write_to_excel(code,result)

while True:
    main()