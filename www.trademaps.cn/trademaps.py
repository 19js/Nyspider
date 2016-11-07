import requests
import json
import openpyxl
import time
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
    html=requests.get('http://www.trademaps.cn/',headers=headers).text
    token=BeautifulSoup(html,'lxml').find('input',{'name':'__RequestVerificationToken'}).get('value')
    data={
    "tboxAccount":logindata["username"],
    "tboxPassword":logindata['passwd'],
    "__RequestVerificationToken":token
    }
    session.post('http://www.trademaps.cn/Common/CheckLogin',data=data,headers=headers)
    return session

class TradeMaps():
    def __init__(self):
        self.keyword=input("输入关键词:")
        self.login()

    def login(self):
        while True:
            try:
                self.session=login()
                break
            except:
                print("登录失败，尝试重新登录")
                continue

    def crawler(self):


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
            "PageSize":50
            "PageTotal":0
            IsNotNull:true
            PagePager:0
            CustomerId:CFA7A20BD3EE1E3CF3BB2D0290BD71F8176B45BC8953EB539C808EA8E25A701AE449AEA23663E5C6E47E47BE58B566FBE30D680A595B0B3B
            SortType:0
        }
