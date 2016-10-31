#coding:utf-8
from langconv import *
import xlrd
import xlwt3

# 转换繁体到简体
def run():
    name='相机'
    f=xlwt3.Workbook(encoding='utf-8')
    sheet=f.add_sheet('sheet')
    data=xlrd.open_workbook(name+'.xls')
    table=data.sheets()[0]
    for i in range(table.nrows):
        line=table.cell(i,0).value
        line=fan_jian(line)
        sheet.write(i,0,line)
    f.save(name+'_.xls')


def fan_jian(line):
    line = Converter('zh-hans').convert(line)#.decode('utf-8'))
    line = line#.encode('utf-8')
    return line

def jian_fan(line):
    line = Converter('zh-hant').convert(line.decode('utf-8'))
    line = line.encode('utf-8')
    return line

run()
