import requests
from bs4 import BeautifulSoup
import time
import json
import openpyxl
import re

Cookie='Hm_lvt_780f12646b56ec5caa7e64e2d303666b=1491010933; Hm_lpvt_780f12646b56ec5caa7e64e2d303666b=1491010933; ASP.NET_SessionId=mx1t3sl3j2hizhekjift24bk; SERVERID=s1'
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cookie':Cookie,
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def get_year_and_batch(subject='理工类',year='2016',min_value=0,max_value=50):
    data={
    'Area':'',
    'MajorName':'',
    'MaxValue':max_value,
    'MinValue':min_value,
    'SchoolName':'',
    'ScoreType':'最低分',
    'Subject':subject,
    'Type':'线差',
    'Year':year+'/',
    'schoolFeature':''
    }
    html=requests.post('http://zyfz.cqzk.com.cn/WillAssistance/SearchYearAndBatch/', data=data, headers=headers).text
    data=json.loads(html)['model']
    return data

def get_school_infor(subject,year,batch,batch_no,min_value=0,max_value=50):
    data={
    'Area':'',
    'MajorName':'',
    'MaxValue':max_value,
    'MinValue':min_value,
    'SchoolName':'',
    'ScoreType':'最低分',
    'Subject':subject,
    'Type':'线差',
    'Year':year+'/',
    'schoolFeature':'',
    'batchSearch':batch,
    'yearSearch':year,
    'batchNoSearch':batch_no
    }
    html=requests.post('http://zyfz.cqzk.com.cn/WillAssistance/SearchSchoolInfo/',data=data,headers=headers).text
    data=json.loads(html)['model']
    return data

def get_major_infor(subject,year,batch,batch_no,school_no,school_name,low_score,min_value,max_value):
    data={
    'Area':'',
    'MajorName':'',
    'MaxValue':max_value,
    'MinValue':min_value,
    'SchoolName':'',
    'ScoreType':'最低分',
    'Subject':subject,
    'Type':'线差',
    'Year':year+'/',
    'schoolFeature':'',
    'batchSearch':batch,
    'yearSearch':year,
    'batchNoSearch':batch_no,
    'schoolNoSearch':school_no,
    'schoolNameSearch':school_name,
    'lowScore':low_score,
    }
    html=requests.post('http://zyfz.cqzk.com.cn/WillAssistance/SearchMajorInfo/',data=data,headers=headers).text
    data=json.loads(html)['model']
    return data

def get_university_and_score():
    year='2016'
    subject='理工类'
    min_value=0
    max_value=50
    while(max_value<250):
        batchs=get_year_and_batch(subject, year,min_value,max_value)
        for batch in batchs:
            batch_name=batch['Batch']
            batch_no=batch['BatchId']
            print(batch_name)
            schools=get_school_infor(subject, year, batch_name, batch_no,min_value,max_value)
            f=open('school_2016.txt','a')
            for school in schools:
                school['min_value']=min_value
                school['max_value']=max_value
                school['batch_name']=batch_name
                school['batch_no']=batch_no
                school['subject']=subject
                school['year']=year
                f.write(str(school)+'\n')
            f.close()
        min_value+=50
        max_value+=50

def get_student_infor(major_no,school_no,year,batch_no,subject):
    data={
    'majorNo':major_no,
    'schoolNo':school_no,
    'year':year,
    'batchNo':batch_no,
    'subjectName':subject
    }
    html=requests.post('http://zyfz.cqzk.com.cn/WillAssistance/SearchStudentInfo/',data=data,headers=headers).text
    models=json.loads(html)['model']
    result=[]
    for model in models:
        try:
            result.append(model['Score'])
        except:
            continue
    result=sorted(result)
    if result==[]:
        return '-','-'
    return result[0],result[-1]

def get_majors():
    school_keys=['院校代号','院校名称','院校官网','招生章程','院校录取最高分','院校录取最高分位次','院校录取平均分','院校录取最低分','院校录取最低分位次','院校录取平均分线差','院校录取最低分线差']
    major_keys=['专业代号','专业名称','专业原始计划数','专业实际录取人数','专业录取平均分']
    for school in open('./school_2016.txt','r'):
        school=eval(school)
        line=[school['subject'],school['batch_name']]
        for key in school_keys:
            try:
                line.append(school['modelInfo'][key])
            except:
                line.append('')
        try:
            school_no=school['modelInfo']['院校代号']
            school_name=school['modelInfo']['院校名称']
            low_score=school['modelInfo']['院校录取最低分']
            min_value=school['min_value']
            max_value=school['max_value']
            majors=get_major_infor(school['subject'],school['year'],school['batch_name'],school['batch_no'],school_no,school_name,low_score,min_value,max_value)
        except:
            failed=open('failed.txt','a')
            failed.write(str(school)+'\n')
            failed.close()
            continue
        f=open('result.txt','a')
        for major in majors:
            try:
                grade1,grade2=get_student_infor(major['modelInfo']['专业代号'], school_no, school['year'], school['batch_no'], school['subject'])
            except:
                continue
            major_line=[]
            for key in major_keys:
                try:
                    major_line.append(major['modelInfo'][key])
                except:
                    major_line.append('')
            f.write(str(line+major_line+[grade1,grade2])+'\n')
        f.close()
        print(line)

def write_to_excel():
    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    school_keys=['院校代号','院校名称','院校官网','招生章程','院校录取最高分','院校录取最高分位次','院校录取平均分','院校录取最低分','院校录取最低分位次','院校录取平均分线差','院校录取最低分线差']
    major_keys=['专业代号','专业名称','专业原始计划数','专业实际录取人数','专业录取平均分']
    sheet.append(school_keys+major_keys)
    num=0
    for line in open('./result.txt','r'):
        line = ILLEGAL_CHARACTERS_RE.sub(r'', line)
        item=eval(line)
        try:
            sheet.append(item)
        except:
            failed=open('failed.txt','a')
            failed.write(line)
            failed.close()
            continue
        num+=1
        print(num)
    excel.save('result.xlsx')

write_to_excel()
