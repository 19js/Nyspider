#coding=utf-8

import requests
from bs4 import BeautifulSoup
import openpyxl
import json
import codecs

#用户名
j_username=""
#加密后的密码
j_password=''

class Renrendai():
    def __init__(self):
        self.session=requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
        self.keys=['id','Loan_Title','Loan_type', 'Loan_Status','Amount', 'Interest_Rate', 'Term','Next_Payment_Day','Term_Remain', 'Repayment_Type','Des','Guarantee_Type','Early_Repayment_Rate',
                'Borrower_Id','Userid','Age','Education',  'Marital status','Working_City','Company_Scale','Position','Employment_Sector', 'Emploment_Length','Homeowner', 'Mortgage', 'Car', 'Car_Loan',
                'Total_Amount','Number_of_Succesful_Loan', 'Income_Range_Monthly', 'Number_of_Borrow', 'Number_of_Repaid', 'Outstanding','Overdue_amount','Severe_overdue','Credit_Score',  'Number_Arrears', 'Credit_Limit']
        self.credit_keys=['work', 'identification', 'borrowStudy', 'video', 'mobileReceipt', 'child', 'identificationScanning', 'graduation','mobile', 'other', 'house','incomeDuty', 'account','fieldAudit', 'residence', 'marriage', 'detailInformation', 'album', 'credit', 'mobileAuth','kaixin', 'car', 'renren']
        self.passtime_keys=['credit','identificationScanning','fieldAudit','identification','lastUpdateTime','openTime','startTime','readyTime','passTime','jsondata']
        self.count=1
        self.excel=openpyxl.Workbook(write_only=True)
        self.sheet=self.excel.create_sheet()
        self.sheet.append(self.keys+self.credit_keys+self.passtime_keys)
        self.login()
        self.text_f=codecs.open('text.txt','a',encoding='utf-8')
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
        id_from=800000
        id_to=800075
        for load_id in range(int(id_from),int(id_to)+1):
            line=self.get_page('http://www.we.com/lend/detailPage.action?loanId='+str(load_id),load_id)
            try:
                line=self.get_page('http://www.we.com/lend/detailPage.action?loanId='+str(load_id),load_id)
            except:
                try:
                    self.login()
                except:
                    pass
                self.failed_f.write(str(load_id)+'\n')
                continue
            print(load_id)
            self.write_to_text(line)
            self.write_to_excel(line)
        self.excel.save('result.xlsx')

    def get_page(self,url,load_id):
        html=self.session.get(url,headers=self.headers,timeout=30).text
        try:
            credit_infor=self.get_credit_infor(html)
        except:
            credit_infor=[]
        base_infor=self.parser(html,load_id)
        return base_infor+credit_infor

    def write_to_text(self,line):
        text='|'.join(line)
        self.text_f.write(text+'\n')

    def write_to_excel(self,line):
        try:
            self.sheet.append(line)
        except:
            pass

    def get_credit_infor(self,html):
        json_data=BeautifulSoup(html,'lxml').find('script',id='credit-info-data').get_text()
        data=json.loads(json_data)['data']
        credit=data['creditInfo']
        credit_infor=[]
        for key in self.credit_keys:
            try:
                value=credit[key]
                if value=='VALID':
                    value='1'
                else:
                    value='0'
                credit_infor.append(value)
            except:
                credit_infor.append('0')
        creditPassedTime=data['creditPassedTime']
        passed_time=[]
        for key in ['credit','identificationScanning','fieldAudit','identification','lastUpdateTime']:
            try:
                passed_time.append(creditPassedTime[key])
            except:
                passed_time.append('')
        loan=data['loan']
        for key in ['openTime','startTime','readyTime','passTime']:
            try:
                passed_time.append(loan[key])
            except:
                passed_time.append('')
        passed_time.append(str(data))
        return credit_infor+passed_time

    def parser(self,html,load_id):
        soup=BeautifulSoup(html,'lxml').find('div',id='pg-loan-invest')
        infor_one=soup.find('div',id='loan-basic-panel')
        infor={}
        infor['id']=str(load_id)
        infor['Loan_type']=infor_one.find('div',attrs={'class':'fn-text-overflow'}).get('title')
        infor['Loan_Title']=infor_one.find('em',attrs={'class':'title-text'}).get_text()
        em=infor_one.find('div',attrs={'class':'pl25 pr25 fn-clear'}).find_all('em')
        infor['Amount']=em[0].get_text()
        infor['Interest_Rate']=em[1].get_text()
        infor['Term']=em[3].get_text()
        ul=infor_one.find('div',attrs={'class':'loaninfo'}).find('ul').find_all('li')
        infor['Guarantee_Type']=ul[0].find('span',attrs={'class':'basic-value'}).get_text()
        infor['Early_Repayment_Rate']=ul[0].find('span',attrs={'class':'fn-left basic-value num'}).get_text()
        infor['Repayment_Type']=ul[1].find('span',attrs={'class':'basic-value'}).get_text()
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
        infor['Userid']=table[0].find('em').find('a').get('href').replace('/account/myInfo.action?userId=','')
        infor['Credit_Score']=table[0].find_all('em')[1].get('title')
        infor['Des']=soup.find('div',attrs={'class':'ui-tab-list color-dark-text'}).get_text().replace('\n','').replace('\t','')
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
            if item.get_text()[:4]==u'公司行业':
                infor['Employment_Sector']=item.find('em').get_text()
            if item.get_text()[:4]==u'公司规模':
                infor['Company_Scale']=item.find('em').get_text()
            if item.get_text()[:4]==u'岗位职位':
                infor['Position']=item.find('em').get_text()
        line=[]
        for key in self.keys:
            try:
                line.append(infor[key].replace(' ',''))
            except:
                line.append('-')
        return line

if __name__=='__main__':
    work=Renrendai()
    work.run()
