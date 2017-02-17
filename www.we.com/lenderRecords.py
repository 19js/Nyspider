#coding:utf-8

import requests
from bs4  import BeautifulSoup
import json
import openpyxl
import codecs

#用户名
j_username=""
#加密后的密码
j_password=''

class Get_lenderRecords():
    def __init__(self):
        self.session=requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
        self.login()
        self.keys=['loanId','lenderType','lendTime','userId','userNickName','financeCategory','amount']
        self.excel=openpyxl.Workbook(write_only=True)
        self.sheet=self.excel.create_sheet()
        self.sheet.append(self.keys)
        self.failed_f=codecs.open('failed.txt','a',encoding='utf-8')

    def login(self):
        data={
            'j_username':j_username,
            'j_password':j_password,
            'rememberme':'on',
            'targetUrl':'http://www.we.com/',
            'returnUrl':'https://www.we.com/account/index.action'}
        self.session.post('https://www.we.com/j_spring_security_check',data=data,headers=self.headers)

    def run(self):
        id_from=70000#起始id
        id_to=70050#结束id
        for load_id in range(int(id_from),int(id_to)+1):
            try:
                items=self.get_page('http://www.we.com/lend/getborrowerandlenderinfo.action?id=lenderRecords&loanId='+str(load_id))
            except:
                self.login()
                self.failed_f.write(str(load_id)+'\r\n')
                continue
            print(load_id)
            self.write_to_excel(items)
        self.excel.save('lenderRecords.xlsx')

    def get_page(self,url):
        html=self.session.get(url,headers=self.headers,timeout=40).text
        try:
            infor=self.parser(html)
        except:
            infor=[]
        return infor

    def write_to_excel(self,items):
        for item in items:
            try:
                self.sheet.append(item)
            except:
                continue

    def parser(self,html):
        records=json.loads(html)['data']['lenderRecords']
        results=[]
        for item in records:
            line=[]
            for key in self.keys:
                try:
                    line.append(item[key])
                except:
                    line.append('')
            results.append(line)
        return results

if __name__=='__main__':
    work=Get_lenderRecords()
    work.run()
