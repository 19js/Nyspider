import json
import openpyxl
import time
import csv

def write_to_excel(lines,filename,write_only=True):
    excel=openpyxl.Workbook(write_only=write_only)
    sheet=excel.create_sheet()
    for line in lines:
        sheet.append(line)
    excel.save(filename)

def write_csv(lines,filename):
    csvfile = open(filename, 'w', encoding='utf-8')
    spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for line in lines:
        spamwriter.writerow(line)
    csvfile.close()

def load_txt():
    info_keys = ['officeScale', 'carLoan', 'realName', 'creditLevel', 'office', 'province', 'officeType', 'idNo', 'sumCreditPoint', 'houseLoan', 'marriage', 'userId', 'city', 'position', 'university', 'workYears', 'birthDay', 'graduation', 'homeTown', 'carYear', 'hasHouse', 'gender', 'hasCar', 'officeDomain', 'availableCredits', 'promotion', 'nickName', 'salary', 'carBrand']
    loan_keys=['loanId','title','amount','status','interest','repayType','verifyState','borrowerLevel','borrowType','months','leftMonths','description','startTime','passTime','nickName','address','jobType']
    detail_keys=['totalCount','successCount','alreadyPayCount','borrowAmount','notPayTotalAmount','overdueAmount','overdueCount']
    credit_keys=['identification','borrowStudy','incomeDuty','credit','identificationScanning','work']
    yield loan_keys+info_keys+detail_keys+credit_keys
    for line in open('./files/loan_result_1.txt', 'r'):
        try:
            item = json.loads(line)
        except:
            continue
        info=[]
        for key in loan_keys:
            try:
                value=item['info']['loan'][key]
                if 'Time' in key:
                    try:
                        value=time.strftime('%Y-%m-%d',time.localtime(int(value)/1000))
                    except Exception as e:
                        print(e)
                info.append(str(value))
            except:
                info.append('')
        for key in info_keys:
            try:
                info.append(str(item['info']['borrower'][key]))
            except:
                info.append('')
        for key in detail_keys:
            try:
                info.append(str(item['info']['userLoanRecord'][key]))
            except:
                info.append('')
        for key in credit_keys:
            try:
                info.append(str(item['info']['creditInfo'][key]))
            except:
                info.append('')
        yield info
    for line in open('./files/loan_result_2.txt', 'r'):
        try:
            item = json.loads(line)
        except:
            continue
        info=[]
        for key in loan_keys:
            try:
                value=item['info']['loan'][key]
                if 'Time' in key:
                    try:
                        value=time.strftime('%Y-%m-%d',time.localtime(int(value)/1000))
                    except Exception as e:
                        print(e)
                        pass
                info.append(str(value))
            except:
                info.append('')
        for key in info_keys:
            try:
                info.append(str(item['info']['borrower'][key]))
            except:
                info.append('')
        for key in detail_keys:
            try:
                info.append(str(item['info']['userLoanRecord'][key]))
            except:
                info.append('')
        for key in credit_keys:
            try:
                info.append(str(item['info']['creditInfo'][key]))
            except:
                info.append('')
        yield info


write_csv(load_txt(),'loan_result.csv')


