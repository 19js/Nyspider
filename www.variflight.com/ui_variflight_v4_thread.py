# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from bs4 import BeautifulSoup
import time
import random
import os
from PIL import Image
import math
import datetime
import threading
from PyQt5.QtWidgets import QFileDialog
import re


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(375, 528)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 71, 31))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(90, 20, 81, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(180, 20, 16, 31))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(200, 20, 81, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 71, 21))
        self.label_3.setObjectName("label_3")
        self.dateEdit = QtWidgets.QDateEdit(self.centralWidget)
        self.dateEdit.setGeometry(QtCore.QRect(90, 130, 191, 31))
        self.dateEdit.setDate(QtCore.QDate(2016, 8, 21))
        self.dateEdit.setObjectName("dateEdit")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(90, 170, 31, 31))
        self.label_4.setObjectName("label_4")
        self.dateEdit_2 = QtWidgets.QDateEdit(self.centralWidget)
        self.dateEdit_2.setGeometry(QtCore.QRect(90, 210, 191, 31))
        self.dateEdit_2.setDate(QtCore.QDate(2016, 9, 1))
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.label_5 = QtWidgets.QLabel(self.centralWidget)
        self.label_5.setGeometry(QtCore.QRect(10, 80, 61, 17))
        self.label_5.setObjectName("label_5")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(90, 70, 191, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(80, 300, 191, 101))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 70, 80, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 375, 22))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.menu.addAction(self.action)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "定时抓取："))
        self.label_2.setText(_translate("MainWindow", "~"))
        self.label_3.setText(_translate("MainWindow", "抓取范围："))
        self.label_4.setText(_translate("MainWindow", "到"))
        self.label_5.setText(_translate("MainWindow", "航班号："))
        self.pushButton.setText(_translate("MainWindow", "开始抓取"))
        self.pushButton_2.setText(_translate("MainWindow", "打开文件*"))
        self.menu.setTitle(_translate("MainWindow", "菜单"))
        self.action.setText(_translate("MainWindow", "退出"))
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.dateEdit_2.setDisplayFormat("yyyy-MM-dd")


def convert_image(image):
    image=image.convert('L')
    image2=Image.new('L',image.size,255)
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix=image.getpixel((x,y))
            if pix<150:
                image2.putpixel((x,y),0)
    return image2

def cut_image(image):
    inletter=False
    foundletter=False
    letters=[]
    start=0
    end=0
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix=image.getpixel((x,y))
            if(pix==0):
                inletter=True
        if foundletter==False and inletter ==True:
            foundletter=True
            start=x
        if foundletter==True and inletter==False:
            end=x
            letters.append((start,end))
            foundletter=False
        inletter=False
    images=[]
    for letter in letters:
        img=image.crop((letter[0],0,letter[1],image.size[1]))
        images.append(img)
    return images

def buildvector(image):
    result={}
    count=0
    for i in image.getdata():
        result[count]=i
        count+=1
    return result


class CaptchaRecognize:
    def __init__(self):
        self.letters=['0','1','2','3','4','5','6','7','8','9','24','44','b','m','s']
        self.loadSet()

    def loadSet(self):
        self.imgset=[]
        for letter in self.letters:
            temp=[]
            for img in os.listdir('./icon/%s'%(letter)):
                temp.append(buildvector(Image.open('./icon/%s/%s'%(letter,img))))
            self.imgset.append({letter:temp})

    #计算矢量大小
    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    #计算矢量之间的 cos 值
    def relation(self,concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

    def recognise(self,content):
        if content==False:
            return '--'
        with open('temp.png','wb') as f:
            f.write(content)
        image=Image.open('temp.png')
        image=convert_image(image)
        images=cut_image(image)
        vectors=[]
        for img in images:
            vectors.append(buildvector(img))
        result=[]
        for vector in vectors:
            guess=[]
            for image in self.imgset:
                for letter,temp in image.items():
                    relevance=0
                    num=0
                    for img in temp:
                        relevance+=self.relation(vector,img)
                        num+=1
                    relevance=relevance/num
                    guess.append((relevance,letter))
            guess.sort(reverse=True)
            result.append(guess[0])
        result_str=''
        for item in result:
            result_str+=item[1]
        result_str=result_str.replace('b','%').replace('m',':').replace('s','.')
        return result_str

def get_headers():
    headers = {
        "X-Forwarded-For":'%s.%s.%s.%s'%(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
        'Host':"www.variflight.com",
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    return headers

def flights():
    html=requests.get('http://www.variflight.com/sitemap.html?AE71649A58c77',headers=get_headers()).text
    table=BeautifulSoup(html,'html.parser').find('div',{'class':'list'}).find_all('a')
    f=open('flights.txt','a',encoding='utf-8')
    for item in table:
        try:
            url='http://www.variflight.com/'+item.get('href')+'&fdate='
            if 'flight/fnum/' not in url:
                continue
            name=item.get_text()
            f.write(name+'|'+url+'\n')
        except:
            continue
    f.close()

def get_image(img_url,session):
    headers = {
        "X-Forwarded-For":'%s.%s.%s.%s'%(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Host':"www.variflight.com",
        'Accept':"image/png,image/*;q=0.8,*/*;q=0.5",
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    count=0
    while True:
        try:
            content=session.get(img_url,headers=headers,timeout=30).content
            return content,session
        except:
            count+=1
            if count==4:
                return False,session

def get_flight_infor(url):
    count=0
    while True:
        try:
            html=requests.get(url,headers=get_headers(),timeout=30).text
            break
        except:
            count+=1
            if count==5:
                return False
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'flyProc'})
    item={}
    try:
        item['distance']=soup.find('div',{'class':'p_ti'}).find('span').get_text()
    except:
        item['distance']='-'
    try:
        item['time_length']=soup.find('div',{'class':'p_ti'}).find_all('span')[1].get_text()
    except:
        item['time_length']='-'
    try:
        item['mileage']=soup.find('li',{'class':'mileage'}).get_text().replace('机型：','')
    except:
        item['mileage']='-'
    try:
        item['age']=soup.find('li',{'class':'time'}).get_text().replace('机龄：','')
    except:
        item['age']='-'
    try:
        item['pre_time']=soup.find('li',{'class':'age'}).get_text()
        if '提前' in item['pre_time']:
            item['add_sub']='-'
        elif '晚点' in item['pre_time']:
            item['add_sub']='+'
        else:
            item['add_sub']=0
    except:
        item['pre_time']='-'
        item['add_sub']=0
    try:
        item['minutes']=int(re.findall('(\d+)分钟',item['pre_time'])[0])
    except:
        item['minutes']=0
    try:
        item['hour']=int(re.findall('(\d+)小时',item['pre_time'])[0])
    except:
        item['hour']=0
    return item

class GetFlight(threading.Thread):
    def __init__(self,url,num):
        super(GetFlight,self).__init__()
        self.url=url
        self.num=num

    def run(self):
        self.status=True
        self.result=''
        try:
            self.result=parser(self.url)
        except:
            self.status=False

def parser(url):
    count=0
    session=requests.session()
    while True:
        try:
            html=session.get(url,headers=get_headers(),cookies={"orderRole":"1"},timeout=30).text
            break
        except:
            count+=1
            if count==4:
                return 'Error'
    if '抱歉，没有找到您输入的航班信息' in html:
        return []
    table=BeautifulSoup(html.replace('\n','').replace('\t',''),'lxml').find('ul',id='list').find_all('li')
    result=[]
    for item in table:
        try:
            flight={}
            url='http://www.variflight.com/'+item.find('a').get('href')
            infor=get_flight_infor(url)
            if infor=='Error':
                return 'Error'
            for key in infor:
                flight[key]=infor[key]
            spans=item.find_all('span')
            try:
                flight['share']=item.find('a',{'class':'list_share'}).get_text()
            except:
                flight['share']='-'
            flight['name']=spans[0].find('a').get_text()
            flight['flight']=spans[0].get_text().replace(flight['name'],'')
            flight['fly_time']=spans[1].get_text()
            try:
                r_fly_time_url='http://www.variflight.com/'+spans[2].find('img').get('src')
                content,session=get_image(r_fly_time_url,session)
                flight['r_fly_time_img']=content
            except:
                flight['r_fly_time_img']=False
            try:
                flight['r_fly_time_str']=spans[2].find('em').get_text()
            except:
                flight['r_fly_time_str']=''
            flight['from']=spans[3].get_text()
            flight['arrive_time']=spans[4].get_text()
            try:
                r_arrive_time_url='http://www.variflight.com/'+spans[5].find('img').get('src')
                content,session=get_image(r_arrive_time_url,session)
                flight['r_arrive_time_img']=content
            except:
                flight['r_arrive_time_img']=False
            try:
                flight['r_arrive_time_str']=spans[5].find('em').get_text()
            except:
                flight['r_arrive_time_str']=''
            flight['to']=spans[6].get_text()
            try:
                on_time_url='http://www.variflight.com/'+spans[7].find('img').get('src')
                content,session=get_image(on_time_url,session)
                flight['on_time_img']=content
            except:
                flight['on_time_img']=False
            try:
                flight['status']=spans[8].get_text()
            except:
                flight['status']='-'
            result.append(flight)
        except:
            continue
    return result

def change(flight):
    if flight['add_sub']==0:
        if flight['arrive_time']!=flight['r_arrive_time_img']:
            flight['r_arrive_time_img'],flight['r_fly_time_img']=flight['r_fly_time_img'],flight['r_arrive_time_img']
    elif flight['add_sub']=='+':
        ar_hour=int(flight['arrive_time'].split(':')[0])
        ar_minutes=int(flight['arrive_time'].split('当地')[0].split(':')[1])
        ar_hour=ar_hour+flight['hour']
        ar_minutes+=flight['minutes']
        if ar_minutes>=60:
            ar_minutes=ar_minutes-60
            ar_hour+=1
        if ar_hour>23:
            ar_hour=ar_hour-24
        num=ar_hour*100+ar_minutes
        num1=int(flight['r_arrive_time_img'].split('当地')[0].replace(':',''))
        if num!=num1:
            flight['r_arrive_time_img'],flight['r_fly_time_img']=flight['r_fly_time_img'],flight['r_arrive_time_img']
    else:
        ar_hour=int(flight['arrive_time'].split(':')[0])
        ar_minutes=int(flight['arrive_time'].split('当地')[0].split(':')[1])
        ar_hour=ar_hour-flight['hour']
        ar_minutes-=flight['minutes']
        if ar_minutes<0:
            ar_hour-=1
            ar_minutes+=60
        if ar_hour<0:
            ar_hour+=24
        num=ar_hour*100+ar_minutes
        num1=int(flight['r_arrive_time_img'].split('当地')[0].replace(':',''))
        if num!=num1:
            flight['r_arrive_time_img'],flight['r_fly_time_img']=flight['r_fly_time_img'],flight['r_arrive_time_img']
    return flight

def flights(date,filepath,timefrom,timeto):
    recognise=CaptchaRecognize()
    lines=[line.replace('\r','').replace('\n','') for line in open(filepath,'r',encoding='utf-8')]
    while len(lines):
        timenow=time.strftime("%H%M",time.localtime())
        timenow=int(timenow)
        while timenow<timefrom or timenow>timeto:
            time.sleep(1*60)
            timenow=time.strftime("%H%M",time.localtime())
            timenow=int(timenow)
        threadings=[]
        count=0
        while count<20:
            try:
                line=lines.pop()
                url='http://www.variflight.com//flight/fnum/%s.html?AE71649A58c77=&fdate='%line
                crawler=GetFlight(url+date,line)
                crawler.setDaemon(True)
                threadings.append(crawler)
                count+=1
            except:
                break
        for crawler in threadings:
            crawler.start()
        for crawler in threadings:
            crawler.join()
        f=open('result/'+date+'.txt','a',encoding='utf-8')
        for crawler in threadings:
            if crawler.result==[]:
                print(crawler.num,'False')
                f.write(crawler.num+'\tFalse\n')
                continue
            while(crawler.status==False or crawler.result=='Error'):
                print(crawler.num,'Error')
                continue_or_break=input("错误！输入1重新抓取，0放弃抓取该航班")
                if continue_or_break=='1':
                    continue
                else:
                    crawler.result=[]
                    f.write(crawler.num+'\tFalse\n')
                    break
                crawler.run()
            for flight in crawler.result:
                keys=['r_arrive_time_img','r_fly_time_img','on_time_img']
                for key in keys:
                    content=flight[key]
                    if content==False:
                        flight[key]='-'
                        continue
                    str_time=recognise.recognise(content)
                    try:
                        flight[key]=str_time+flight[key.replace('img','str')]
                    except:
                        flight[key]=str_time
                try:
                    flight=change(flight)
                except:
                    pass
                keys=['name','share','flight','fly_time','r_fly_time_img','from','arrive_time','r_arrive_time_img','to','on_time_img','status','distance','time_length','mileage','age','pre_time']
                write_line=crawler.num+'\tTrue\t'+date+'\t'
                for key in keys:
                    write_line+=flight[key].replace('\t','')+'\t'
                write_line=write_line.replace('\r','').replace('\n','')
                f.write(write_line+'\r\n')
                try:
                    print(flight['name'],flight['flight'],'ok')
                except:
                    pass
        f.close()
        threadings.clear()

def day_get(d):
    oneday = datetime.timedelta(days=1)
    day = d+oneday
    day=str(day).split(' ')[0].replace('-','')
    return day

class Flight(Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self):
        super(Flight,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("非常准航班采集")
        self.baseinit()
        self.filepath='./flights_num.txt'
        timenow=time.strftime("%Y-%m-%d",time.localtime())
        self.dateEdit.setDate(QtCore.QDate.fromString(timenow,'yyyy-MM-dd'))
        self.dateEdit_2.setDate(QtCore.QDate.fromString(timenow,'yyyy-MM-dd'))
        try:
            os.mkdir('result')
        except:
            pass

    def baseinit(self):
        self.action.triggered.connect(self.close)
        self.pushButton.clicked.connect(self.crawl)
        self.pushButton_2.clicked.connect(self.get_filepath)

    def get_filepath(self):
        try:
            filepath,filetype=QFileDialog.getOpenFileName(self,"选取文件",".","All Files (*);;Text Files (*.txt)")
        except:
            filepath='./flights_num.txt'
        self.filepath=filepath
        self.lineEdit_3.setText(self.filepath)

    def get_input(self):
        timefrom=self.lineEdit.text().replace(' ','').replace('\r','').replace('\n','').replace(':','').replace('：','')
        timeto=self.lineEdit_2.text().replace(' ','').replace('\r','').replace('\n','')
        try:
            self.timefrom=int(timefrom)
        except:
            self.timefrom=0
        try:
            self.timeto=int(timeto)
        except:
            self.timeto=2400
        self.date_from=self.dateEdit.text().replace('-','')
        self.date_to=self.dateEdit_2.text().replace('-','')

    def crawl(self):
        self.get_input()
        self.crawler=Crawler(self.date_from,self.date_to,self.filepath,self.timefrom,self.timeto)
        self.crawler._finish_signal.connect(self.crawl_ok)
        self.crawler.start()
        self.pushButton.setEnabled(False)
        self.pushButton.setText("抓取中")

    def crawl_ok(self,infor):
        self.pushButton.setEnabled(True)
        self.pushButton.setText("开始抓取")


class Crawler(QtCore.QThread):
    _finish_signal=QtCore.pyqtSignal(str)
    _page_ok_signal=QtCore.pyqtSignal(str)
    def __init__(self,date_from,date_to,filepath,timefrom,timeto):
        super(Crawler,self).__init__()
        self.date_from=date_from
        self.date_to=date_to
        self.filepath=filepath
        self.timefrom=timefrom
        self.timeto=timeto

    def run(self):
        while True:
            try:
                flights(self.date_from,self.filepath,self.timefrom,self.timeto)
            except:
                print(self.date_from,'failed')
            if self.date_from==self.date_to:
                break
            date_now=datetime.datetime.strptime(self.date_from, "%Y%m%d")
            self.date_from=day_get(date_now)
        self._finish_signal.emit("OK")

if __name__ == '__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    management=Flight()
    management.show()
    sys.exit(app.exec_())
