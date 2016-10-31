import requests
import openpyxl
import json
import time


def get_flowhistory(stockid):
    html=requests.get('http://zj.flashdata2.jrj.com.cn/flowhistory/share/%s.js'%stockid).text
    data=json.loads(html.replace('var stock_flow=',''))
    result=[]
    header=['序号','日期','涨跌幅','收盘价','换手率','净流入金额','主力净流入净额','主力净流入净占比','中单净流入净额','中单净流入净占比','散户净流入净额','散户净流入净占比','第二天']
    result.append(header)
    keys=['date','pl','cp','tr','tin','zin','zpit','min','mpit','sin','spit']
    count=1
    pre_line=''
    for line in data:
        item=[count]
        count+=1
        for key in keys:
            item.append(line[key])
        try:
            item.append(pre_line['pl'])
        except:
            pass
        result.append(item)
        pre_line=line
    return result

def write_to_excel(result,stockid):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for item in result:
        sheet.append(item)
    excel.save('%s.xlsx'%stockid)

def main():
    stockid=input("输入股票代码:")
    try:
        result=get_flowhistory(stockid)
    except:
        print('Failed!')
        time.sleep(10)
        return
    write_to_excel(result,stockid)

main()
