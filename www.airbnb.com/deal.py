import os
import re
import xlwt3


def deal_userdata():
    userresult=open('userresult.txt','w')
    for line in open('userdata.txt','r'):
        line=line.replace('\n','')
        lists=line.split('||')
        try:
            allreview=int(lists[-2].replace('Reviews',''))
        except:
            allreview=0
        try:
            hostreview=int(lists[-1])
        except:
            hostreview=0
        try:
            prereview=allreview-hostreview
        except:
            prereview='--'
        result=''
        for i in lists:
            result+=i+'||'
        result+=str(prereview)
        userresult.write(result+'\n')
    userresult.close()

def replace_r():
    room=open('roomtxt.txt','w')
    f=open('roomdata.txt','r').readlines()
    for line in f:
        line=line.replace('\r','').replace('\n','')
        room.write(line+'\n')
    room.close()

def Excel():
    Response_rate='Response rate:(.*?)Response'
    Response_time='Response time:(.*?hours)'
    users=open('userresult.txt','r').readlines()
    rooms=open('roomtxt.txt','r').readlines()
    excel=xlwt3.Workbook()
    usersheet=excel.add_sheet('user')
    roomsheet=excel.add_sheet('room')
    count=0
    for line in rooms:
        lists=line.replace('\n','').split('||')
        for user in users:
            if lists[5] in user:
                try:
                    rate=re.findall(Response_rate,line)[0]
                except:
                    rate='--'
                try:
                    time=re.findall(Response_time,line)[0]
                except:
                    time='--'
                num=0
                for i in lists:
                    try:
                        i=i.split('?')[0]
                        i=i.split(':')[-1]
                        i=i.replace('/rooms/','')
                        i=i.replace('/users/show/','')
                    except:
                        pass
                    roomsheet.write(count,num,i)
                    num+=1
                roomsheet.write(count,num,rate)
                num+=1
                roomsheet.write(count,num,time)
                num=0
                for i in user.replace('\n','').split('||'):
                    try:
                        i=i.split('?')[0]
                        i=i.split(':')[-1]
                        i=i.replace('/rooms/','')
                        i=i.replace('/users/show/','')
                    except:
                        pass
                    usersheet.write(count,num,i)
                    num+=1
                count+=1
    excel.save('result.xls')

Excel()
