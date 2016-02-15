#coding:utf-8

import requests
from bs4 import BeautifulSoup
import threading
import re
import os
import xlwt3

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def Get_Quarter():
    statue=True
    while statue:
        try:
            html=requests.get('https://duapp2.drexel.edu/webtms_du/app?page=Home&service=page',headers=headers,timeout=30).text
            statue=False
        except:
            continue
    table=BeautifulSoup(html,'lxml').find_all('table',attrs={'class':'termPanel'})
    quarter={}
    for item in table[0].find_all('a'):
        quarter[item.get_text()]='https://duapp2.drexel.edu'+item.get('href')
    for item in table[1].find_all('a'):
        quarter[item.get_text()]='https://duapp2.drexel.edu'+item.get('href')
    return quarter

def Get_College(url):
    statue=True
    while statue:
        try:
            html=requests.get(url,headers=headers,timeout=30).text
            statue=False
        except:
            continue
    table=BeautifulSoup(html,'lxml').find('div',id='sideLeft').find_all('a')
    colleges={}
    for item in table:
        colleges[item.get_text()]='https://duapp2.drexel.edu'+item.get('href')
    return colleges

def Get_subjects(url):
    statue=True
    while statue:
        try:
            html=requests.get(url,headers=headers,timeout=30).text
            statue=False
        except:
            continue
    table=BeautifulSoup(html,'lxml').find('table',attrs={'class':'collegePanel'}).find_all('a')
    subjects={}
    for item in table:
        subjects[item.get_text()]='https://duapp2.drexel.edu'+item.get('href')
    return subjects

class CourseInfor(threading.Thread):
    def __init__(self,url,name):
        super(CourseInfor,self).__init__()
        self.url=url
        self.name=name

    def run(self):
        statue=True
        while statue:
            try:
                html=requests.get(self.url,headers=headers,timeout=30).text
                statue=False
            except:
                continue
        table=BeautifulSoup(html,'lxml').find('td',attrs={'align':'center'}).find('table').find_all('tr')
        self.course_list=[]
        courses=[]
        for item in table[1:-1]:
            course=self.subject_parser(item)
            if course==False:
                continue
            courses.append(course)
        for course in courses:
            course=self.course_parser(course)
            self.course_list.append(course)
        print('------'+self.name+'--OK')

    def course_parser(self,course):
        statue=True
        while statue:
            try:
                html=requests.get(course['url'],headers=headers,timeout=30).text
                statue=False
            except:
                continue
        soup=BeautifulSoup(html,'lxml').find('table',attrs={'align':'center','valign':'top'})
        baseInforTable=soup.find('td',attrs={'align':'left'}).find_all('td',attrs={'align':'center'})
        trs=baseInforTable[0].find_all('tr')
        lists=['SubjectCode','CourseNumber','Section','Credits','Title','Campus','Instructors','Instruction_Type','Instruction_Method','Max_Enroll','Enroll','Section_Comments']
        for num in range(len(lists)):
            try:
                course[lists[num]]=trs[num+1].find_all('td')[1].get_text()
            except:
                course[lists[num]]='--'
        table=baseInforTable[1].find('tr',attrs={'class':'even'}).find_all('td')
        course['Building']=table[-2].get_text()
        course['Room']=table[-1].get_text()
        subjectInforText=soup.find('td',attrs={'align':'center','valign':'top'}).get_text()
        reText={'College':'College:([\s\S]*)Department','Restrictions':'Restrictions:([\s\S]*)Co-Requisites','Co-Requisites':'Co-Requisites:([\s\S]*)Pre-Requisites','Pre-Requisites':'Pre-Requisites:([\s\S]*)Repeat Status','Repeat Status':'Repeat Status:([\s\S]*)'}
        for key in reText:
            try:
                course[key]=re.findall(reText[key],subjectInforText)[0]
            except:
                course[key]='--'
        return course

    def subject_parser(self,item):
        course={}
        try:
            url='https://duapp2.drexel.edu'+item.find('a').get('href')
        except:
            return False
        course['url']=url
        course['CRN']=item.find('a').get_text()
        course['Times']=item.find('table').get_text()
        return course

def Get_Course(Quarter,college,subjects):
    print(Quarter+'--'+college+'--Start')
    excel=xlwt3.Workbook()
    threadings=[]
    for subject in subjects:
        work=CourseInfor(subjects[subject], subject)
        threadings.append(work)
    for work in threadings:
        work.setDaemon(True)
        work.start()
    for work in threadings:
        work.join()
    sheet=excel.add_sheet(college)
    count=0
    lists=['SubjectCode','CourseNumber','CRN','Section','Credits','Times','Title','Campus','Instructors','Instruction_Type'
    ,'Instruction_Method','Max_Enroll','Enroll','Section_Comments','Building','Room','College','Restrictions','Co-Requisites','Pre-Requisites','Repeat Status','url']
    for work in threadings:
        for course in work.course_list:
            for num in range(len(lists)):
                sheet.write(count,num,course[lists[num]])
            count+=1
    print(Quarter+'--'+college+'--OK')
    excel.save(Quarter+'/'+college+'.xls')

def main():
    quarter=Get_Quarter()
    for key in quarter:
        colleges=Get_College(quarter[key])
        try:
            os.mkdir(key)
        except:
            print('--')
        excel=xlwt3.Workbook()
        threadings=[]
        for college in colleges:
            subjects=Get_subjects(colleges[college])
            work=threading.Thread(target=Get_Course,args=(key, college, subjects))
            threadings.append(work)
        for work in threadings:
            work.setDaemon(True)
            work.start()
        for work in threadings:
            work.join()
        print('----------'+key+'--OK----------')

main()
