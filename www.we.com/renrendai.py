#coding:utf-8

import requests
from bs4 import BeautifulSoup
import xlwt3

#登录后的cookie,每次使用的时候更换cookie
cookie='Hm_lvt_16f9bb97b83369e62ee1386631124bb1=1449805903,1450175719; rrdLoginCartoon=rrdLoginCartoon; newuser=new; JSESSIONID=60C3753F3743FBEB65AD181218120A7D575957D8981BC4084DC0CB8747EA6FF5; Hm_lpvt_16f9bb97b83369e62ee1386631124bb1=1450175780; jforumUserInfo=c1fE1x9cq0BQTuRBRbrVLRb%2FrUmAs9jk%0A; IS_MOBLIE_IDPASS=true-false; activeTimestamp=2490435'

class Get_data():
    def __init__(self):
        self.session=requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
        self.f=xlwt3.Workbook()
        self.sheet=self.f.add_sheet('sheet')
        self.lists=['id','Loan_Title', 'Loan_Status','Amount', 'Interest_Rate', 'Term','Next_Payment_Day','Term_Remain', 'Repayment_Type','Guarantee_Type','Early_Repayment_Rate',
                'Borrower_Id', 'Age','Education',  'Marital status','Working_City','Company_Scale','Position','Employment_Sector', 'Emploment_Length','Homeowner', 'Mortgage', 'Car', 'Car_Loan',
                'Total_Amount','Number_of_Succesful_Loan', 'Income_Range_Monthly', 'Number_of_Borrow', 'Number_of_Repaid', 'Outstanding','Overdue_amount','Severe_overdue','Credit_Score',  'Number_Arrears', 'Credit_Limit']
        self.count=1
        num=0
        for key in self.lists:
            self.sheet.write(0,num,key)
            num+=1
        self.login()

    def login(self):
        data={
            'j_username':'18502793163',
            'j_password':'TWVqb89VKdl87RGdWgHZHbPjOik7noAQ0QErNQC+NAOJP6KeOw9+Thz1Ac0ZUehsTftixuPqRqA12s3/eovVHcWcfa/tr67llXr0zZkvaouYFshRQ31TfI4J5INhz7C8wuh7VOk2hXmUD2kX6SsTuvH/UnlUUj8ber5x1O2hM6c=',
            'rememberme':'on',
            'targetUrl':'http://www.we.com/',
            'returnUrl':'https://www.we.com/account/index.action'}
        self.session.post('https://www.we.com/j_spring_security_check',data=data,headers=self.headers)

    def run(self):
        id_from=input('输入起始id:')
        id_to=input("输入终止id:")
        for load_id in range(int(id_from),int(id_to)+1):
            try:
                items=self.get_page('http://www.we.com/lend/detailPage.action?loanId='+str(load_id))
            except:
                continue
            items['id']=str(load_id)
            print(load_id)
            self.write_to_excel(items)

    def get_page(self,url):
        html=self.session.get(url,headers=self.headers).text
        infor=self.parser(html)
        return infor

    def write_to_excel(self,items):
        num=0
        for key in self.lists:
            self.sheet.write(self.count,num,items[key].replace(' ',''))
            num+=1
        self.count+=1
        self.f.save('data.xls')

    def parser(self,html):
        soup=BeautifulSoup(html,'lxml').find('div',id='pg-loan-invest')
        infor_one=soup.find('div',id='loan-basic-panel')
        infor={}
        infor['Loan_Title']=infor_one.find('em',attrs={'class':'title-text'}).get_text()
        em=infor_one.find('div',attrs={'class':'fn-clear  mb25'}).find_all('em')
        infor['Amount']=em[0].get_text()
        infor['Interest_Rate']=em[1].get_text()
        infor['Term']=em[3].get_text()
        ul=infor_one.find('div',attrs={'class':'fn-left pt10 loaninfo '}).find('ul').find_all('li')
        infor['Guarantee_Type']=ul[0].find('span',attrs={'class':'fn-left basic-value last'}).get_text()
        infor['Early_Repayment_Rate']=ul[0].find('span',attrs={'class':'fn-left basic-value num'}).get_text()
        infor['Repayment_Type']=ul[1].find('span',attrs={'class':'fn-left basic-value'}).get_text()
        statue=infor_one.find('div',attrs={'class':'pl25 pr25 fn-clear'}).find('div',attrs={'class':'stamp'}).find('em').get('class')
        infor['Loan_Status']=statue[0]
        if statue==['REPAYING']:
            infor['Term_Remain']=infor_one.find('div',attrs={'class':'pl25 pr25 fn-clear'}).find('div',attrs={'class':'box box-top'}).find('i').get_text()
            infor['Next_Payment_Day']=infor_one.find('div',attrs={'class':'pl25 pr25 fn-clear'}).find('div',attrs={'class':'box box-bottom'}).find('i').get_text()
        else:
            infor['Term_Remain']=''
            infor['Next_Payment_Day']=''
        table=soup.find('div',id='loan-details').find('table',attrs={'class':'ui-table-basic-list'}).find_all('tr')
        infor['Borrower_Id']=table[0].find('em').get_text()
        infor['Credit_Score']=table[0].find_all('em')[1].get('title')
        em=table[2].find_all('em')
        infor['Age']=em[0].get_text().replace('\n','').replace('\t','')
        infor['Education']=em[1].get_text().replace('\n','').replace('\t','')
        infor['Marital status']=em[2].get_text().replace('\n','').replace('\t','')
        em=table[4].find_all('em')
        infor['Number_of_Borrow']=em[0].get_text().replace('\n','').replace('\t','')
        infor['Credit_Limit']=em[1].get_text().replace('\n','').replace('\t','')
        infor['Overdue_amount']=em[2].get_text().replace('\n','').replace('\t','')
        em=table[5].find_all('em')
        infor['Number_of_Succesful_Loan']=em[0].get_text().replace('\n','').replace('\t','')
        infor['Total_Amount']=em[1].get_text().replace('\n','').replace('\t','')
        infor['Number_Arrears']=em[2].get_text().replace('\n','').replace('\t','')
        em=table[6].find_all('em')
        infor['Number_of_Repaid']=em[0].get_text().replace('\n','').replace('\t','')
        infor['Outstanding']=em[1].get_text().replace('\n','').replace('\t','')
        infor['Severe_overdue']=em[2].get_text().replace('\n','').replace('\t','')
        em=table[8].find_all('em')
        infor['Income_Range_Monthly']=em[0].get_text().replace('\n','').replace('\t','')
        infor['Homeowner']=em[1].get_text().replace('\n','').replace('\t','')
        infor['Mortgage']=em[2].get_text().replace('\n','').replace('\t','')
        em=table[9].find_all('em')
        infor['Car']=em[0].get_text().replace('\n','').replace('\t','')
        infor['Car_Loan']=em[1].get_text().replace('\n','').replace('\t','')
        em=table[11].find_all('em')
        infor['Working_City']=em[0].get_text().replace('\n','').replace('\t','')
        infor['Emploment_Length']=em[1].get_text().replace('\n','').replace('\t','')
        for item in soup.find('div',id='loan-details').find('table',attrs={'class':'ui-table-basic-list'}).find_all('td'):
            if item.get_text()[:4]=='公司行业':
                infor['Employment_Sector']=item.find('em').get_text()
            if item.get_text()[:4]=='公司规模':
                infor['Company_Scale']=item.find('em').get_text()
            if item.get_text()[:4]=='岗位职位':
                infor['Position']=item.find('em').get_text()
        return infor

if __name__=='__main__':
    work=Get_data()
    work.run()
