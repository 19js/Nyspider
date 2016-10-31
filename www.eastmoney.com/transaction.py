import requests
import openpyxl
import re
import time
import os


def get_data(code,market):
    url='http://nufm3.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=%s&sty=DPTTFD&st=z&sr=1&p=1&ps=&cb=&token=beb0a0047196124721f56b0f0ff5a27c'
    html=requests.get(url%(code+market)).text
    if 'false' in html:
        return False
    text=re.findall('"(.*?)"',html)[0]
    lines=text.split('|')
    result=[]
    for line in lines:
        result.append(line.split('~'))
    return result

def write_to_excel(code,result):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for item in result:
        sheet.append(item)
    try:
        os.mkdir('result/'+code)
    except:
        pass
    date=timenow=time.strftime('%Y-%m-%d',time.localtime())
    excel.save('result/'+code+'/%s.xlsx'%date)

def get_transaction(code):
    global result
    for market in ['1','2']:
        try:
            data=get_data(code,market)
        except:
            continue
        if data==False:
            continue
        break
    if data==[] or data==False:
        print('Failed')
        return
    timenow=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    print(timenow,code,'ok')
    is_write=False
    for line in data:
        if line in result:
            continue
        result.append(line)
        is_write=True
    if is_write:
        write_to_excel(code,result)
    

code=input('输入股票代码：')
result=[]
while True:
    get_transaction(code)
    time.sleep(0.5)