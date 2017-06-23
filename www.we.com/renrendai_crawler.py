#coding=utf-8

import requests
from bs4 import BeautifulSoup
import csv
import json
import codecs
import threading
import logging
import random
import os
import cStringIO

def get_headers():
    headers = {
        "X-Forwarded-For":'%s.%s.%s.%s'%(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Host':'www.renrendai.com',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    return headers

def login(j_username,j_password):
    session=requests.session()
    data={
        'j_username':j_username,
        'j_password':j_password,
        'rememberme':'on',
        'targetUrl':'http://www.renrendai.com/',
        'returnUrl':'https://www.renrendai.com/account/index.action'}
    html=session.post('https://www.renrendai.com/pc/passport/index/doLogin',data=data,headers=get_headers(),timeout=20).text
    if u'登录成功' in html:
        return session
    else:
        print(html)
        return False

class RenrendaiSpider(threading.Thread):
    def __init__(self,session,loan_id):
        super(RenrendaiSpider,self).__init__()

        self.session=session
        self.loan_id=loan_id

        self.keys=['id','Loan_Title','Loan_type', 'Loan_Status','Amount', 'Interest_Rate', 'Term','Next_Payment_Day','Term_Remain', 'Repayment_Type','Des','Guarantee_Type','Early_Repayment_Rate',
                'Borrower_Id','Userid','Age','Education',  'Marital status','Working_City','Company_Scale','Position','Employment_Sector', 'Emploment_Length','Homeowner', 'Mortgage', 'Car', 'Car_Loan',
                'Total_Amount','Number_of_Succesful_Loan', 'Income_Range_Monthly', 'Number_of_Borrow', 'Number_of_Repaid', 'Outstanding','Overdue_amount','Severe_overdue','Credit_Score',  'Number_Arrears', 'Credit_Limit']
        self.credit_keys=['work', 'identification', 'borrowStudy', 'video', 'mobileReceipt', 'child', 'identificationScanning', 'graduation','mobile', 'other', 'house','incomeDuty', 'account','fieldAudit', 'residence', 'marriage', 'detailInformation', 'album', 'credit', 'mobileAuth','kaixin', 'car', 'renren']
        self.passtime_keys=['credit','identificationScanning','fieldAudit','identification','lastUpdateTime','openTime','startTime','readyTime','passTime']
        self.lender_keys=keys=['loanId','lenderType','lendTime','user','userId','userNickName','financeCategory','amount','autoCheckout','bussNo','financePlanId','financePlanSubPointId','orderNo','tradeMethod']

    def run(self):
        self.status=True
        try:
            self.result=self.crawl()
        except Exception as e:
            self.status=False


    def crawl(self):
        loan_info=self.get_page('http://www.renrendai.com/lend/detailPage.action?loanId='+str(self.loan_id),self.loan_id)
        user_img_src=self.get_user_info(loan_info[14])
        loan_info=[user_img_src]+loan_info
        records=self.get_lender_records(self.loan_id)
        result=[]
        if len(records)==0:
            result=[loan_info]
        else:
            for line in records:
                result.append(loan_info+line)
        return result

    def get_user_info(self,user_id):
        html=self.session.get('https://www.renrendai.com/account/myInfo.action?userId='+str(user_id),headers=get_headers(),timeout=20).text
        user_img_src='https://www.renrendai.com'+BeautifulSoup(html,'lxml').find('img',{'class':'avatar'}).get('src')
        try:
            download_img(user_img_src, str(user_id)+'.png')
        except Exception as e:
            pass
        return user_img_src

    def get_page(self,url,loan_id):
        html=self.session.get(url,headers=get_headers(),timeout=20).text
        try:
            credit_infor=self.get_credit_infor(html)
        except:
            credit_infor=[]
        base_infor=self.parser(html,loan_id)
        return base_infor+credit_infor

    def get_lender_records(self,loan_id):
        try:
            html=self.session.get('http://www.renrendai.com/lend/getborrowerandlenderinfo.action?id=lenderRecords&loanId='+str(loan_id),headers=get_headers(),timeout=20).text
            records=self.parser_lender_records(html)
        except Exception as e:
            records=[]
        return records

    def parser_lender_records(self,html):
        records=json.loads(html)['data']['lenderRecords']
        results=[]
        for item in records:
            line=[]
            for key in self.lender_keys:
                try:
                    line.append(str(item[key]))
                except:
                    line.append('-')
            results.append(line)
        return results

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
                passed_time.append('-')
        loan=data['loan']
        for key in ['openTime','startTime','readyTime','passTime']:
            try:
                passed_time.append(loan[key])
            except:
                passed_time.append('-')
        return credit_infor+passed_time

    def parser(self,html,loan_id):
        soup=BeautifulSoup(html,'lxml').find('div',id='pg-loan-invest')
        infor_one=soup.find('div',id='loan-basic-panel')
        infor={}
        infor['id']=str(loan_id)
        infor['Loan_type']=infor_one.find('h1',{'class':'fn-text-overflow'}).get('title')
        infor['Loan_Title']=infor_one.find('em',{'class':'title-text'}).get_text()
        em=infor_one.find('div',{'class':'pl25 pr25 fn-clear'}).find_all('em')
        infor['Amount']=em[0].get_text()
        infor['Interest_Rate']=em[1].get_text()
        infor['Term']=em[3].get_text()
        ul=infor_one.find('div',{'class':'loaninfo'}).find('ul').find_all('li')
        infor['Guarantee_Type']=ul[0].find('span',{'class':'basic-value'}).get_text()
        infor['Early_Repayment_Rate']=ul[0].find('span',{'class':'fn-left basic-value num'}).get_text()
        infor['Repayment_Type']=ul[1].find('span',{'class':'basic-value'}).get_text()
        statue=infor_one.find('div',{'class':'pl25 pr25 fn-clear'}).find('div',{'class':'stamp'}).find('em').get('class')
        infor['Loan_Status']=statue[0]
        if statue==['REPAYING']:
            infor['Term_Remain']=infor_one.find('div',{'class':'pl25 pr25 fn-clear'}).find('div',{'class':'box box-top'}).find('i').get_text()
            infor['Next_Payment_Day']=infor_one.find('div',{'class':'pl25 pr25 fn-clear'}).find('div',{'class':'box box-bottom'}).find('i').get_text()
        else:
            infor['Term_Remain']=''
            infor['Next_Payment_Day']=''
        table=soup.find('div',id='loan-details').find('table',{'class':'ui-table-basic-list'}).find_all('tr')
        infor['Borrower_Id']=table[0].find('em').get_text()
        infor['Userid']=table[0].find('em').find('a').get('href').replace('/account/myInfo.action?userId=','')
        infor['Credit_Score']=table[0].find_all('em')[1].get('title')
        infor['Des']=soup.find('div',{'class':'ui-tab-list color-dark-text'}).get_text().replace('\n','').replace('\t','')
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
        for item in soup.find('div',id='loan-details').find('table',{'class':'ui-table-basic-list'}).find_all('td'):
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

def download_img(imgurl,filename):
    content=requests.get(imgurl,timeout=20).content
    with open('image/'+filename,'wb') as f:
        f.write(content)

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def write_to_csv(result):
    with open('result.csv','a') as f:
        writer = UnicodeWriter(f)
        writer.writerows(result)

def write_to_failed(loan_id):
    f=codecs.open('failed_ids.txt','a',encoding='utf-8')
    f.write(str(loan_id)+'\r\n')
    f.close()

if __name__=='__main__':
    try:
        os.mkdir('image')
    except:
        pass
    #用户名
    j_username=""
    #密码
    j_password=""
    
    thread_size=10

    loan_id_from=800000
    loan_id_to=800200

    session=login(j_username,j_password)
    if session!=False:
        while True:
            threadings=[]
            for i in range(thread_size):
                spider=RenrendaiSpider(session, loan_id_from)
                spider.setDaemon(True)
                threadings.append(spider)
                loan_id_from+=1
                if loan_id_to<loan_id_from:
                    break
            for spider in threadings:
                spider.start()
            for spider in threadings:
                spider.join()
            for spider in threadings:
                if spider.status==False:
                    print(spider.loan_id,'False')
                    write_to_failed(spider.loan_id)
                else:
                    write_to_csv(spider.result)
                    print(spider.loan_id,'OK')
            if loan_id_to<loan_id_from:
                break
