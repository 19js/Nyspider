#coding:utf-8
import xlwt3

def excel():
    file_d=open('data.txt','r')
    excel_f=xlwt3.Workbook()
    sheet=excel_f.add_sheet('sheet')
    count=0
    for line in file_d.readlines():
        lists=line.replace('\n','').split('|')
        num=0
        for item in lists:
            try:
                text=item.split('：')[1]
            except:
                text=item
            sheet.write(count,num,text)
            num+=1
        count+=1
    excel_f.save('data.xls')

excel()
