import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import random

"""
Python版本：Python3
依赖库：BeautifulSoup4,requests,openpyxl
依赖库安装方式：
在命令行使用pip安装，具体可百度
pip install BeautifulSoup4
pip install requests
pip install openpyxl
"""

def get_headers():
    """
    构造请求头
    """
    pc_headers = {
        "X-Forwarded-For": '%s.%s.%s.%s' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }
    return pc_headers

def get_error_info(error_code):
    url='http://www.zdobd.com/obd2.php'
    data={
        'num':error_code
    }
    #POST 请求，获取结果列表
    res_text=requests.post(url,data=data,headers=get_headers(),timeout=20).text.encode('iso-8859-1').decode('utf-8')
    #BeautifulSoup解析网页，需要结合具体网页
    table=BeautifulSoup(res_text).find('div',id='company').find('table').find_all('tr')
    result=[]
    for tr in table[1:]:
        tds=tr.find_all('td')
        line=[]
        for td in tds:
            #获取具体的文本
            line.append(td.get_text())
        result.append(line)
    return result

def write_to_excel(lines,filename,write_only=True):
    """
    写入Excel,使用openpyxl库
    """
    excel=openpyxl.Workbook(write_only=write_only)
    sheet=excel.create_sheet()
    for line in lines:
        sheet.append(line)
    excel.save(filename)

def crawl():
    result=[]
    for i in range(0,3090):
        #构造故障码
        err_code="P%04d"%(i)
        try:
            #获取故障码信息
            result+=get_error_info(err_code)
        except Exception as e:
            #捕捉异常
            print('error',err_code,e)
            continue
        print(err_code,'OK')
    #将结果写入Excel
    write_to_excel(result,'result.xlsx')

if __name__=='__main__':
    crawl()
