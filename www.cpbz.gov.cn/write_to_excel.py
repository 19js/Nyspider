import openpyxl

def load_result():
    result=[]
    for line in open('result.txt','r'):
        item=eval(line)
        baseinfor=[item['url']]
        for key in ['机构名称','法定代表人','组织机构代码','邮政编码','注册地址','行政区划']:
            try:
                baseinfor.append(item['企业基本信息'][key])
            except:
                baseinfor.append('')
        numbers=[]
        try:
            for num_line in item['技术指标']:
                numbers+=num_line
        except:
            pass
        for key in ['标准名称','标准编号','公开时间','url']:
            try:
                baseinfor.append(item['标准信息'][key])
            except:
                baseinfor.append('')
        try:
            products=item['产品信息']
        except:
            f=open('empty.txt','a')
            f.write(line)
            f.close()
            continue
        for product in products:
            product[-1]=item['standardStatus']
            yield baseinfor+product+numbers

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    count=0
    for line in load_result():
        sheet.append(line)
        count+=1
        print(count)
    excel.save('result.xlsx')

write_to_excel()
