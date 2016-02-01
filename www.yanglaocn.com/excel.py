#coding:utf-8

import os
import xlwt3

def Excel():
    for filename in os.listdir('.'):
        if(filename.endswith('lts.txt')):
            page=0
            f_d=open(filename,'r')
            f_ex=xlwt3.Workbook(encoding='utf-8')
            sheet=f_ex.add_sheet('sheet')
            count=0
            for line in f_d.readlines():
                lists=line.split('||')
                try:
                    num=0
                    for text in lists:
                        sheet.write(count,num,text)
                        num+=1
                    count+=1
                except:
                    f_ex.save(str(page)+'.xls')
                    page+=1
                    f_ex=xlwt3.Workbook(encoding='utf-8')
                    sheet=f_ex.add_sheet('sheet')
                    count=0
                    num=0
                    for text in lists:
                        sheet.write(count,num,text)
                        num+=1
                    count+=1
            f_ex.save(str(page)+'.xls')

Excel()
