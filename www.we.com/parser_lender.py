import json
import openpyxl
import time
import csv


def write_csv(lines,filename):
    csvfile = open(filename, 'w', encoding='gbk')
    spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for line in lines:
        spamwriter.writerow(line)
    csvfile.close()
        

def load_txt():
    for line in open('./files/lender_result','r'):
        try:
            item=json.loads(line)
        except:
            continue
        item[-3]=time.strftime('%Y-%m-%d',time.localtime(int(item[-3])/1000))
        yield item


write_csv(load_txt(),'lender_result.csv')
        