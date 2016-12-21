import openpyxl
import os

def write_to_excel():
    for filename in os.listdir('data'):
        excel=openpyxl.Workbook(write_only=True)
        sheet=excel.create_sheet()
        for line in open('data/'+filename,'r',encoding='utf-8'):
            line=line.replace('\r','').replace('\xa0','')
            line=eval(line)
            sheet.append(line)
        excel.save('excel/'+filename.replace('.txt','.xlsx'))
        print(filename,'ok')

write_to_excel()
