import openpyxl
import os
from bs4 import BeautifulSoup
import re


def load_result_1():
    result=[]
    for line in open('result.txt','r'):
        item=eval(line)
        baseinfor=item['baseinfor']
        for word in item['words']:
            line=word[:-1]
            des=''
            for p in word[-1]:
                des+=p+'\n'
            result.append(line+baseinfor+[des,item['url']])
    return result

def load_result_2():
    result=[]
    for line in open('result.txt','r'):
        item=eval(line)
        baseinfor=item['baseinfor']
        for word in item['words']:
            line=word[:-1]
            num=1
            for p in word[-1]:
                text=BeautifulSoup(p,'lxml').get_text()
                text=re.sub('(\d+. )|◎ ','',text)
                result.append(line+baseinfor+[num,text,item['url']])
                num+=1
    return result

def write_to_excel(result,filename):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in result:
        sheet.append(line)
    excel.save(filename)

result=load_result_1()
write_to_excel(result,'result_1.xlsx')
