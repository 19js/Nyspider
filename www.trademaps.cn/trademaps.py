import requests
import json
import openpyxl
import time
import re
from bs4 import BeautifulSoup

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def load_login_data():
    f=open('./logindata.json','r',encoding='utf-8')
    data=json.loads(f.read())
    return data

def login():
    try:
        logindata=load_login_data()
    except:
        print("Load Login data Failed!")
        return False
    session=requests.session()
    html=session.get('http://www.trademaps.cn/',headers=headers).text
    token=BeautifulSoup(html,'lxml').find('input',{'name':'__RequestVerificationToken'}).get('value')
    data={
    "tboxAccount":logindata["username"],
    "tboxPassword":logindata['passwd'],
    "__RequestVerificationToken":token
    }
    session.post('http://www.trademaps.cn/Common/CheckLogin',data=data,headers=headers)
    html=session.get('http://www.trademaps.cn/OneSearch/Hemo',headers=headers).text.replace("\n",'').replace(' ','')
    custid=re.findall("custid='(.*?)'",html)[0]
    return session,custid

class TradeMaps():
    def __init__(self):
        self.keyword="bicycle"#input("输入关键词:")
        self.custid=''
        self.login()

    def login(self):
        while True:
            try:
                self.session,self.custid=login()
                break
            except:
                print("登录失败，尝试重新登录")
                continue

    def crawler(self):
        pass

    def crawl(self):
        data={
            "Keydoc":self.keyword,
            "SearchType":"desc",
            "IsWords":"true",
            "CountryCode":"",
            "Country":"",
            "BillNo":"",
            "Importer":"",
            "Product":"",
            "HsCode":"",
            "Exporter":"",
            "StartDate":"",
            "EndDate":"",
            "Ie":"false",
            "PageIndex":1,
            "PageSize":30,
            "PageTotal":0,
            "IsNotNull":"true",
            "PagePager":0,
            "CustomerId":self.custid,
            "SortType":0
        }
        print(data)
        html=self.session.post("http://www.trademaps.cn/api/RestOneSearch",data=data,headers=headers).text
        print(html)

if __name__=="__main__":
    trademaps=TradeMaps()
    trademaps.crawl()
