#coding:utf-8

import requests
from bs4 import BeautifulSoup
import threading
import re
import os
import sqlite3
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def Get_Semesters():
    statue=True
    while statue:
        try:
            html=requests.get('https://duapp2.drexel.edu/webtms_du/app?page=Home&service=page',headers=headers,timeout=50).text
            statue=False
        except:
            continue
    table=BeautifulSoup(html,'lxml').find_all('table',attrs={'class':'termPanel'})
    semesters={}
    for item in table[0].find_all('a'):
        semesters[item.get_text()]='https://duapp2.drexel.edu'+item.get('href')
    for item in table[1].find_all('a'):
        semesters[item.get_text()]='https://duapp2.drexel.edu'+item.get('href')
    return semesters

def Get_College(url):
    statue=True
    while statue:
        try:
            html=requests.get(url,headers=headers,timeout=50).text
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
            html=requests.get(url,headers=headers,timeout=50).text
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
                html=requests.get(self.url,headers=headers,timeout=50).text
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
                html=requests.get(course['url'],headers=headers,timeout=50).text
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

def Get_Course(semester,college,subjects):
    rel='[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）-]+'
    conn=sqlite3.connect(semester+'/data.db')
    cursor=conn.cursor()
    cursor.execute("create table if not exists %s(SubjectCode varchar(80),CourseNumber varchar(20) primary key,Title varchar(80),College varchar(80),Co_Requisites TEXT,Pre_Requisites TEXT,Repeat_Status TEXT)"%(re.sub(rel,'',college)))
    print(semester+'--'+college+'--Start')
    threadings=[]
    for subject in subjects:
        work=CourseInfor(subjects[subject], subject)
        threadings.append(work)
    for work in threadings:
        work.setDaemon(True)
        work.start()
    for work in threadings:
        work.join()
    static_label=['SubjectCode','CourseNumber','Title','College','Co-Requisites','Pre-Requisites','Repeat Status']
    dynamic_label=['CRN','Section','Restrictions','Credits','Campus','Instructors','Instruction_Type','Instruction_Method','Max_Enroll','Enroll','Section_Comments','Times','Building','Room','url']
    for work in threadings:
        cursor.execute("create table if not exists %s(CRN varchar(10) primary key,Section varchar(80),Restrictions TEXT,Credits varchar(50),Campus varchar(80),Instructors varchar(80),Instruction_Type varchar(80),Instruction_Method varchar(80),Max_Enroll varchar(50),Enroll varchar(50),Section_Comments varchar(80),Times TEXT,Building varchar(80),Room varchar(80),url TEXT)"%(re.sub(rel,'',work.name)))
        for course in work.course_list:
            static=[]
            dynamic=[]
            for index in range(len(static_label)):
                static.append(course[static_label[index]])
            for index in range(len(dynamic_label)):
                dynamic.append(course[dynamic_label[index]])
            try:
                cursor.execute("insert into %s(SubjectCode,CourseNumber,Title,College,Co_Requisites,Pre_Requisites,Repeat_Status) values"%(re.sub(rel,'',college))+str(tuple(static)))
            except:
                pass
            try:
                cursor.execute("insert into %s(CRN,Section,Restrictions,Credits,Campus,Instructors,Instruction_Type,Instruction_Method,Max_Enroll,Enroll,Section_Comments,Times,Building,Room,url) values"%(re.sub(rel,'',work.name))+str(tuple(dynamic)))
            except:
                pass
    conn.commit()
    cursor.close()
    conn.close()
    print(semester+'--'+college+'--OK')

def Get_all(semesters):
    for key in semesters:
        colleges=Get_College(semesters[key])
        try:
            os.mkdir(key)
        except:
            print('--')
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

def Get_One(semester,url):
    try:
        os.remove(semester+'/data.db')
    except:
        pass
    colleges=Get_College(url)
    try:
        os.mkdir(semester)
    except:
        print('--')
    threadings=[]
    for college in colleges:
        subjects=Get_subjects(colleges[college])
        work=threading.Thread(target=Get_Course,args=(semester, college, subjects))
        threadings.append(work)
    for work in threadings:
        work.setDaemon(True)
        work.start()
    for work in threadings:
        work.join()
    print('----------'+semester+'--OK----------')

def Update(semester,url):
    colleges=Get_College(url)
    try:
        os.mkdir(semester)
    except:
        print('--')
    threadings=[]
    for college in colleges:
        subjects=Get_subjects(colleges[college])
        work=threading.Thread(target=Update_Course,args=(semester, college, subjects))
        threadings.append(work)
    for work in threadings:
        work.setDaemon(True)
        work.start()
    for work in threadings:
        work.join()
    print('----------'+semester+'--OK----------')

def Update_Course(semester,college,subjects):
    rel='[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+'
    conn=sqlite3.connect(semester+'/data.db')
    cursor=conn.cursor()
    print(semester+'--'+college+'--Start')
    threadings=[]
    for subject in subjects:
        work=CourseInfor(subjects[subject], subject)
        threadings.append(work)
    for work in threadings:
        work.setDaemon(True)
        work.start()
    for work in threadings:
        work.join()
    dynamic_label=['CRN','Section','Restrictions','Credits','Campus','Instructors','Instruction_Type','Instruction_Method','Max_Enroll','Enroll','Section_Comments','Times','Building','Room','url']
    for work in threadings:
        tablename=re.sub(rel,'',work.name)
        for course in work.course_list:
            for label in dynamic_label:
                cursor.execute("UPDATE %s SET %s='%s' WHERE CRN='%s'"%(tablename,label,course[label],course['CRN']))
    conn.commit()
    cursor.close()
    conn.close()
    print(semester+'--'+college+'--OK')

def main():
    semesters=Get_Semesters()
    print('0.爬取所有学期数据')
    print('1.爬取一个学期数据')
    print('2.更新一个学期数据')
    print('3.更新一个学期动态数据')
    statue=input("输入序号：")
    if statue=='0':
        Get_all(semesters)
    elif statue=='1':
        lists=[]
        print('----------')
        for key in semesters:
            lists.append(key)
        for num in range(len(lists)):
            print(num,'--'+lists[num])
        index=input("Input number:")
        try:
            index=int(index)
            Get_One(lists[index], semesters[lists[index]])
        except:
            print("Error!")
            return
    elif statue=='2':
        lists=[]
        print('----------')
        for key in semesters:
            lists.append(key)
        for num in range(len(lists)):
            print(num,'--'+lists[num])
        index=input("Input number:")
        try:
            index=int(index)
            Get_One(lists[index], semesters[lists[index]])
        except:
            print("Error!")
            return
    elif statue=='3':
        lists=[]
        print('----------')
        for key in semesters:
            lists.append(key)
        for num in range(len(lists)):
            print(num,'--'+lists[num])
        index=input("Input number:")
        try:
            index=int(index)
            Update(lists[index], semesters[lists[index]])
        except:
            print("Error!")
            return
    else:
        print('Error!')

main()
