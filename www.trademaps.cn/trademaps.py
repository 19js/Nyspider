import requests
import json
import openpyxl
import time
import re
import os
from bs4 import BeautifulSoup

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def load_login_data():
    f = open('./logindata.json', 'r', encoding='utf-8')
    data = json.loads(f.read())
    return data


def login():
    try:
        logindata = load_login_data()
    except:
        print("Load Login data Failed!")
        return False
    session = requests.session()
    html = session.get('http://pro.sunmaps.cn/', headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    token = soup.find(
        'input', {'name': '__RequestVerificationToken'}).get('value')
    skin = soup.find('input', {'name': 'skin'}).get('value')
    data = {
        "tboxAccount": logindata["username"],
        "tboxPassword": logindata['passwd'],
        "__RequestVerificationToken": token,
        "skin": skin
    }
    session.post('http://pro.sunmaps.cn/Common/CheckLogin',
                 data=data, headers=headers)
    html = session.get('http://pro.sunmaps.cn/OneSearch/Hemo',
                       headers=headers).text.replace("\n", '').replace(' ', '')
    custid = re.findall("custid='(.*?)'", html)[0]
    return session, custid


class TradeMaps():
    def __init__(self):
        self.keyword = input("输入关键词:")
        self.custid = ''
        self.login()
        self.result = []
        self.page_total = 0
        self.end = False
        try:
            os.remove('result/temp.txt')
        except:
            pass

    def login(self):
        while True:
            try:
                self.session, self.custid = login()
                break
            except:
                print("登录失败，尝试重新登录")
                continue

    def crawler(self):
        page = 1
        while True:
            try:
                self.crawl(page)
            except:
                print("获取 %s 页 失败" % page)
                time.sleep(1)
                continue
            print("获取 %s 页 成功" % page)
            if page == self.page_all or self.end:
                break
            page += 1
        self.write_to_excel()

    def crawl(self, page):
        data = {
            "Keydoc": self.keyword,
            "SearchType": "desc",
            "IsWords": "true",
            "CountryCode": "",
            "Country": "",
            "BillNo": "",
            "Importer": "",
            "Product": "",
            "HsCode": "",
            "Exporter": "",
            "StartDate": "",
            "EndDate": "",
            "Ie": "false",
            "PageIndex": page,
            "PageSize": 30,
            "PageTotal": self.page_total,
            "IsNotNull": "true",
            "PagePager": 0,
            "CustomerId": self.custid,
            "SortType": 0
        }
        html = self.session.post(
            "http://pro.sunmaps.cn/api/RestOneSearch", data=data, headers=headers, timeout=30).text
        try:
            self.parser(html)
        except:
            print(html)

    def parser(self, json_data):
        data = json.loads(json_data)
        if self.page_total == 0:
            self.page_total = data['PageTotal']
            self.page_all = data['PagePager']
            print(self.page_all, self.page_total)
        data = data['Datas']
        if len(data) == 0:
            self.end = True
            return
        keys = ['DataCountry', 'Date', 'HsCode', 'Importer', 'Exporter', 'Product',
                'Country', 'Weight', 'WeightUnit', 'Quantity', 'QuantityUnit', 'Value']
        f = open('result/temp.txt', 'a', encoding='utf-8')
        for item in data:
            line = []
            for key in keys:
                try:
                    line.append(item[key])
                except:
                    line.append('')
            f.write(
                '|'.join([str(i).replace('\r', '').replace('\n', '') for i in line])+'\r\n')
            self.result.append(line)
        f.close()

    def write_to_excel(self):
        excel = openpyxl.Workbook(write_only=True)
        sheet = excel.create_sheet()
        for line in self.result:
            try:
                sheet.append(line)
            except:
                continue
        timenow = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        excel.save('result/%s.xlsx' % timenow)


try:
    import os
    os.mkdir('result')
except:
    pass
trademaps = TradeMaps()
trademaps.crawler()
