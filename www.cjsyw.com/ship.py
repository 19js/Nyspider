#coding:utf-8

import requests
from bs4 import BeautifulSoup
import xlwt3

class Get_infor():
    def __init__(self):
        self.session=requests.session()
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
        self.login()
        self.f=xlwt3.Workbook()
        self.sheet=self.f.add_sheet('sheet')
        self.count=0

    def login(self):
        html=self.session.get('http://www.cjsyw.com/zhuce/login.aspx',headers=self.headers).text
        table=BeautifulSoup(html,'html.parser').find('form',id='form1')
        VIEWSTATE=table.find('input',id='__VIEWSTATE').get('value')
        EVENTVALIDATION=table.find('input',id='__EVENTVALIDATION').get('value')
        data={
            '__VIEWSTATE':VIEWSTATE,
            '__EVENTVALIDATION':EVENTVALIDATION,
            'TextBoxyhm':"fion111472",
            'TextBoxmm':"yh1234",
            'Cokes':"",
            'DropDownList1':"7",
            'Button1':"立即登录"
        }
        self.session.post('http://www.cjsyw.com/zhuce/login.aspx',data=data,headers=self.headers).text

    def main(self):
        num=input('输入抓取页数:')
        for page in range(int(num)):
            items=self.get_url(page+1)
            for item in items:
                infor=self.get_item(item)
                self.sheet.write(self.count,0,infor['name'])
                self.sheet.write(self.count,1,infor['size'])
                self.sheet.write(self.count,2,'吨')
                self.sheet.write(self.count,4,infor['from'])
                self.sheet.write(self.count,5,infor['to'])
                self.sheet.write(self.count,6,infor['date'])
                self.sheet.write(self.count,7,infor['phone'])
                self.sheet.write(self.count,8,infor['company'])
                self.sheet.write(self.count,9,infor['style'])
                self.count+=1
                print(self.count)
            self.f.save('data.xls')

    def get_url(self,page):
        html=self.session.get('http://www.cjsyw.com/huoyuan/hy_index.aspx?page='+str(page),headers=self.headers).text
        table=BeautifulSoup(html).find('div',attrs={'class':'TabADSCon2'}).find('dl').find_all('dd')
        infors=[]
        for item in table:
            infor={}
            lists=item.find_all('a')
            infor['url']='http://www.cjsyw.com/huoyuan/'+lists[0].get('href')
            infor['name']=lists[1].get_text()
            infor['from']=lists[2].get_text()
            infor['to']=lists[3].get_text()
            infor['size']=lists[4].get_text()
            infor['date']=lists[6].get_text()
            infors.append(infor)
        return infors

    def get_item(self,item):
        html=self.session.get(item['url'],headers=self.headers).text
        tables=BeautifulSoup(html).find('div',attrs={'class':'ms_midd ml10'}).find_all('div',attrs={'class':'ms_midd'})
        style=''
        for dd in tables[0].find('dl').find_all('dd'):
            if dd.get_text()[0]=='包':
                style=dd.find('span',attrs={'class':'mmsp2'}).get_text()
        company=''
        phone=''
        for dd in tables[1].find_all('dd'):
            if dd.get_text()[0]=='公':
                company=dd.find('span',attrs={'class':'mmsp2'}).get_text()
            if dd.get_text()[0]=='联':
                phone=dd.find('span',attrs={'class':'mmsp2'}).get_text()
        item['style']=style
        item['company']=company
        item['phone']=phone
        return item

if __name__=='__main__':
    work=Get_infor()
    work.main()
