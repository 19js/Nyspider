#coding:utf-8

import xlwt3
import re

def excel():
    f=open('data.txt','r')
    ex=xlwt3.Workbook()
    sheet=ex.add_sheet('sheet')
    count=0
    rels=['品牌等级：(.*?)\|\|','关注指数：(.*?)\|\|','\|\|.*?董事.*?：(.*?)品牌创立','时间：(.*?)\|\|','发源地：(.*?)\|\|','官方网站：(.*?)\|\|','客服电话：(.*?)\|\|','告词：(.*?)\|\|','(产品\d+)]','(网点\d+)]','(新闻\d+)]','(网店.*?)]']
    for line in f.readlines():
        line=line.replace('\n','').replace('信用指数：','')
        lists=[]
        for rel in rels:
            try:
                i=re.findall(rel,line)[0]
            except:
                i='--'
            lists.append(i)
        strs=line.split('||')
        sheet.write(count,0,strs[0])
        sheet.write(count,1,strs[1])
        sheet.write(count,2,strs[2])
        sheet.write(count,3,strs[3])
        sheet.write(count,4,strs[4])
        sheet.write(count,5,strs[5])
        num=6
        for i in lists:
            sheet.write(count,num,i)
            num+=1
        sheet.write(count,num,strs[-1])
        count+=1
    ex.save('data.xls')

excel()
