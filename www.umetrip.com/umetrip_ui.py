import requests
from bs4 import BeautifulSoup
import time
import random
import os
import math
import datetime
import re
import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog


def get_headers():
    headers = {
        "X-Forwarded-For":'%s.%s.%s.%s'%(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
        'Host':"www.umetrip.com",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    return headers

def load_route(filename):
    routes=[]
    for line in open(filename,'r',encoding='utf-8'):
        try:
            line=line.replace('\r','').replace('\n','').replace('\t','').replace(' ','').split('-')
        except:
            continue
        routes.append(line)
    return routes

def get_flights_by_route(from_city,to_city,need_date):
    url='http://www.umetrip.com/mskyweb/fs/fa.do?dep={}&arr={}&date={}&channel='.format(from_city,to_city,need_date)
    while True:
        try:
            html=requests.get(url,headers=get_headers(),timeout=30).text.replace('\r','').replace('\n','').replace('\t','')
            break
        except:
            print(url,"获取网页失败，重试中")
    flights=re.findall('temp.push\((.*?)\);i\+\+;',html)
    result=[]
    for item in flights:
        spans=BeautifulSoup(item,'lxml').find_all('span')
        flight_num=spans[0].find('b').get_text().replace('"+"','')
        flight_company=spans[0].find_all('a')[-1].get_text()
        line=[need_date,from_city,to_city,flight_num[:2],flight_num,flight_company]
        for span in spans[1:-1]:
            line.append(span.get_text().replace('"+"',''))
        result.append(line)
    return result

def get_flight_info(flight_num,need_date,from_city,to_city):
    url='http://www.umetrip.com/mskyweb/fs/fc.do?flightNo={}&date={}&channel='.format(flight_num,need_date)
    while True:
        try:
            html=requests.get(url,headers=get_headers(),timeout=20).text
            break
        except:
            print(url,"获取网页失败，重试中")
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'flydetail'})
    flight_info=soup.find('div',{'class':'p_info'})
    fly_box=soup.find_all('div',{'class':'fly_box'})
    line=[]
    num=0
    index=0
    for box in fly_box:
        fly_name=box.find('h2').get('title').replace(' 始发','')
        fly_date=box.find('span').get_text()
        date=re.findall('(\d+-\d+-\d+)',fly_date)[0]
        if from_city in fly_name:
            line+=[fly_name,fly_date.replace(date,''),date]
            index=num
        if to_city in fly_name:
            line+=[fly_name,fly_date.replace(date,''),date]
        num+=1
    for class_name in ['mileage','time','age']:
        try:
            line.append(flight_info.find_all('li',{'class':class_name})[index].find('span').get_text())
        except:
            line.append('-')
    try:
        pre_flight=re.findall('前序航班(.*?)\[',str(fly_box[index]))[0]
    except:
        pre_flight='-'
    try:
        tit=soup.find('div',{'class':'tit'})
        if '主飞航班' in str(tit):
            is_zhufei='主飞航班'
        else:
            is_zhufei='-'
    except:
        is_zhufei='-'
    line=[is_zhufei,pre_flight]+line
    return line

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
        self.label_5.setText(_translate("MainWindow", "航线："))
        self.pushButton.setText(_translate("MainWindow", "开始抓取"))
        self.pushButton_2.setText(_translate("MainWindow", "打开文件*"))
        self.menu.setTitle(_translate("MainWindow", "菜单"))
        self.action.setText(_translate("MainWindow", "退出"))
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.dateEdit_2.setDisplayFormat("yyyy-MM-dd")

def day_get(d):
    oneday = datetime.timedelta(days=1)
    day = d+oneday
    day=str(day).split(' ')[0]
    return day

def flights(date,filepath,crawl_time_from,crawl_time_to):
    try:
        routes=load_route(filepath)
    except:
        print("Load routes Failed!")
        return
    for route in routes:
        timenow=time.strftime("%H%M",time.localtime())
        timenow=int(timenow)
        while timenow<crawl_time_from or timenow>crawl_time_to:
            time.sleep(1*60)
            timenow=time.strftime("%H%M",time.localtime())
            timenow=int(timenow)
        try_num=0
        while True:
            try:
                flights=get_flights_by_route(route[0], route[1], date)
                break
            except Exception as e:
                try:
                    print('抓取航线信息失败',route,'ERROR:',e)
                except:
                    pass
                try_num+=1
                if try_num<10:
                    continue
                else:
                    f=open('failed/'+date.replace('-','')+'_route_failed.txt','a',encoding='utf-8')
                    f.write('-'.join(route)+'\r\n')
                    f.close()
                    flights=[]
                    break
        while(len(flights)):
            flight=flights.pop()
            try_num=0
            while True:
                try:
                    info=get_flight_info(flight[4], flight[0], flight[1], flight[2])
                    try:
                        print(route,flight[:5],'OK')
                    except:
                        pass
                    f=open('result/'+date.replace('-','')+'航旅纵横航班信息.txt','a',encoding='utf-8')
                    flight[6]=info[4]+' '+flight[6]
                    flight[7]=info[4]+' '+flight[7]
                    flight[9]=info[7]+' '+flight[9]
                    flight[10]=info[7]+' '+flight[10]
                    write_line=','.join(flight+info)+'\r\n'
                    f.write(write_line.replace('  ',' '))
                    f.close()
                    break
                except Exception as e:
                    try:
                        print('抓取航班信息失败',route,'ERROR:',e)
                    except:
                        pass
                    try_num+=1
                    if try_num<10:
                        continue
                    else:
                        f=open('failed/'+date.replace('-','')+'_flight_failed.txt','a',encoding='utf-8')
                        f.write(','.join(flight)+'\r\n')
                        f.close()
                        break

class Crawler(QtCore.QThread):
    _finish_signal=QtCore.pyqtSignal(str)
    _page_ok_signal=QtCore.pyqtSignal(str)
    def __init__(self,date_from,date_to,filepath,crawl_time_from,crawl_time_to):
        super(Crawler,self).__init__()
        self.date_from=date_from
        self.date_to=date_to
        self.filepath=filepath
        self.crawl_time_from=crawl_time_from
        self.crawl_time_to=crawl_time_to

    def run(self):
        try:
            os.mkdir('result')
        except:
            pass
        try:
            os.mkdir('failed')
        except:
            pass
        while True:
            try:
                flights(self.date_from,self.filepath,self.crawl_time_from,self.crawl_time_to)
            except Exception as e:
                print(self.date_from,'failed','ERROR:',e)
            if self.date_from==self.date_to:
                break
            date_now=datetime.datetime.strptime(self.date_from, "%Y-%m-%d")
            self.date_from=day_get(date_now)
        self._finish_signal.emit("OK")

class UmetripCrawl(Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self):
        super(UmetripCrawl,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("航旅纵横采集器")
        self.baseinit()
        self.filepath='./routes.txt'
        timenow=time.strftime("%Y-%m-%d",time.localtime())
        self.dateEdit.setDate(QtCore.QDate.fromString(timenow,'yyyy-MM-dd'))
        self.dateEdit_2.setDate(QtCore.QDate.fromString(timenow,'yyyy-MM-dd'))

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
        self.date_from=self.dateEdit.text()
        self.date_to=self.dateEdit_2.text()

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

if __name__ == '__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    management=UmetripCrawl()
    management.show()
    sys.exit(app.exec_())

