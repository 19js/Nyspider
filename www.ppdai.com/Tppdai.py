#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

class Get_infor():
    def __init__(self):
        self.login()

    def login(self):
        data={
        'IsAsync':'true',
        'Redirect':'',
        'UserName':'',
        'Password':'',
        'RememberMe':'true'
        }
        self.session=requests.session()
        self.session.post('https://ac.ppdai.com/User/Login',data=data,headers=headers).text
        self.session.get('http://www.ppdai.com/account/lend',headers=headers).text

    def main(self):
        f=open('Tdata.txt','a',encoding='utf-8')
        for text in open('Tperson.txt','r').readlines():
            text=text.replace('\n','')
            line=self.PersonInfor(text)
            if line!=False:
                f.write(line+'\n')
            print(text+'---OK')
        f.close()

    def PersonInfor(self,text):
        rel='实名认证：|身份认证\(10分\)|视频认证\(10分\)|学历认证\(5分\)|手机认证\(10分\)|网上银行充值认证\(3分\)|邀请朋友评价\（5分\）\[已停用\]|【逾期未还清用户无法正常发布列表】|\[非实时更新\]|\(1分/次,每个月最多加一分\)|\(-2分/次\)|\(非实时\)| '
        url=text.split('|')[4]
        try:
            html=requests.get(url,headers=headers,timeout=50).text.encode('ISO-8859-1').decode('utf-8','ignore')
        except:
            return False
        try:
            soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'user_homepage_nav clearfix'})
            left=soup.find('div',attrs={'class':'my-f-left left_user_nav  fl'}).find('ul').find_all('li')
            userinfor=text
            lists=[]
            for item in left[1].find_all('p'):
                userinfor+='|'+item.get_text().replace(' ','').replace('\r','').replace('\n','')
            for item in left[2].find_all('p'):
                userinfor+='|'+item.get_text().replace(' ','').replace('\r','').replace('\n','')
            infor=soup.find('table',attrs={'class':'lendegreetab mb5'}).find_all('tr')
            for tr in infor:
                userinfor+='|'+tr.get_text().replace('\r','').replace('\n','')
            userinfor+='|'+soup.find('div',attrs={'class':'borrowlevelalt_nav'}).find('p').get_text().replace('\r','').replace('\n','')
            userinfor=re.sub(rel,'',userinfor)
            try:
                tozi=self.touzi(url)
            except:
                tozi=''
            text=userinfor+tozi
            return text
        except:
            return False

    def touzi(self,url):
        html=self.session.get(url,headers=headers).text.encode('ISO-8859-1').decode('utf-8','ignore')
        soup=BeautifulSoup(html,'lxml').find('div',id='memberinfocontent')
        tableone=soup.find('table',attrs={'class':'returnstatictab mt10'}).find_all('tr')
        text=''
        for tr in tableone:
            text+='|'+tr.get_text().replace(' ','').replace('\r','').replace('\n','')
        tabletwo=soup.find('table',attrs={'class':'lendegreetab mb50'}).find_all('tr')
        for tr in tabletwo:
            text+='|'+tr.get_text().replace(' ','').replace('\r','').replace('\n','')
        return text

def get_person(Id):
    try:
        html=requests.get('http://www.ppdai.com/list/%s'%Id,headers=headers,timeout=50).text
        soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'wrapNewLendDetailInfoLeft'})
        infor=soup.find('div',attrs={'class':'newLendDetailInfoLeft'})
        biao_table=soup.find('div',attrs={'class':'newLendDetailMoneyLeft'}).find_all('dl')
        jin_table=soup.find('div',attrs={'class':'newLendDetailRefundLeft'}).find_all('div',attrs={'class':'part'})[1].find_all('div')
        text=infor.find('a',attrs={'class':'username'}).get_text()+'|'+infor.find('a',attrs={'class':'altQust'}).find('span').get('class')[1]+'|'+infor.find('span',attrs={'class':'bidinfo'}).get_text()+'|'+infor.find('a').get('href')
        for i in biao_table:
            text+='|'+i.get_text().replace('\r','').replace('\n','').replace(' ','')
        for i in jin_table:
            text+='|'+i.get_text().replace('\r','').replace('\n','').replace(' ','')
        return text
    except:
        return False

def main():
    f_person=open('Tperson.txt','a',encoding='utf-8')
    startId=9158271
    endId=9158371
    while startId<endId:
        text=get_person(startId)
        startId+=1
        if text==False:
            continue
        print(startId)
        f_person.write(text.replace('｜','|')+'\n')
    f_person.close()
    work=Get_infor()
    work.main()

main()
