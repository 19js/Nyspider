#coding:utf-8

import xlwt3

def write():
    f=xlwt3.Workbook()
    sheet=f.add_sheet('sheet')
    file_f=open('D.txt','r')
    num=1
    head=['项目','id','进展数','评论数','最小金额','人数','video','类型','地区','支持人数','已筹款','比例','目标筹资','关注']
    count=0
    for item in head:
        sheet.write(0,count,item)
        count+=1
    for line in file_f.readlines():
        lists=line.replace('\n','').split('|')
        for count in range(14):
            sheet.write(num,count,lists[count])
        num+=1
    f.save('data.xls')

write()
