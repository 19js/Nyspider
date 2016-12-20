import requests
from bs4 import BeautifulSoup
import os
import time
import threading
import copy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent
from PyQt5.QtCore import QTimer

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(429, 490)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit.setGeometry(QtCore.QRect(80, 120, 341, 341))
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(10, 120, 71, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 51, 31))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 20, 341, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 70, 211, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 70, 81, 31))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(310, 70, 113, 32))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 429, 22))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.menu.addAction(self.actionClose)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "挂号信息："))
        self.label_3.setText(_translate("MainWindow", "关键词："))
        self.label.setText(_translate("MainWindow", "查询日期："))
        self.pushButton.setText(_translate("MainWindow", "开始抓取"))
        self.menu.setTitle(_translate("MainWindow", "菜单"))
        self.actionClose.setText(_translate("MainWindow", "close"))

def load_keywords():
    keywords=[]
    for line in open('./keywords.txt','r',encoding='utf-8'):
        keywords.append(line.replace('\r','').replace('\n','').replace(' ',''))
    return keywords

def local_time():
    loc_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    return loc_time

def get_department(hospital_id,keywords):
    html=requests.get('http://yyghwx.bjguahao.gov.cn/hp/search4department.htm?hId=%s&type=1'%hospital_id, headers=headers,timeout=30).text
    table=BeautifulSoup(html,'html.parser').find('div',{'class':'xuanzekshi_box_list'}).find_all('li')
    departments=[]
    for item in table:
        try:
            url=item.find('a').get('href').replace('javascript:getDeptDutySource','').replace(';','')
            department=eval(url)
            departments.append(department)
        except:
            continue
    result=[]
    for department in departments:
        for key in keywords:
            if key in department[2]:
                result.append(department)
    return result

def ok_date(department,date):
    url='http://yyghwx.bjguahao.gov.cn/common/dutysource/appoints/%s,%s.htm?departmentName=%s&type=%s'%department
    html=requests.get(url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'html.parser').find('ul',{'class':'date_nr_ul'}).find_all('li')
    result=[]
    for li in table:
        try:
            a=li.find('a')
            class_name=a.get('class')[0]
            if class_name=='data_bgcol3':
                continue
            url=a.get('href')
            item=url.replace('javascript:getDeptDutySourceByDate','').replace(';','')
            item=eval(item)
            if date not in item[-1]:
                continue
            result.append(item)
        except:
            continue
    return result

def register_infor(item):
    url=url='http://yyghwx.bjguahao.gov.cn/common/dutysource/appoint/%s,%s.htm?departmentName=%s&dutyDate=%s'%item
    html=requests.get(url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'html.parser').find('div',{'class':'hyxzym_box'}).find_all('div',{'class':'hyxzym_b_sj'})
    result=[]
    for div in table:
        try:
            hospital='北京协和医院'
            department_name=item[2]
            date=item[-1]
            if '约满' in str(div):
                continue
            if '电话预约' in str(div):
                date=date+'（114电话预约可挂号）'
            if '微信预约' in str(div):
                date+='（微信预约）'
            spans=div.find_all('span')
            doctor=spans[0].get_text().replace('\xa0','')
            price=spans[1].get_text().replace('\xa0','')
            try:
                price_value=float(price.replace('￥',''))
            except:
                price_value=200
            if price_value<=5:
                continue
            result.append([hospital,department_name,date,doctor,price])
        except:
            continue
    return result

class Book(threading.Thread):
    def __init__(self,department,date):
        super(Book,self).__init__()
        self.department=department
        self.date=date

    def run(self):
        self.result=[]
        try_count=0
        while True:
            try:
                ok_list=ok_date(self.department,self.date)
                break
            except:
                try_count+=1
                if try_count==4:
                    ok_list=[]
                    break
        for item in ok_list:
            try_count=0
            while True:
                try:
                    self.result+=register_infor(item)
                    break
                except:
                    try_count+=1
                    if try_count==4:
                        break

def update_infor(departments,date):
    result=[]
    while len(departments):
        count=0
        threadings=[]
        while count<10:
            try:
                department=departments.pop()
                count+=1
            except:
                break
            work=Book(department,date)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()
        for work in threadings:
            work.join()
        for work in threadings:
            result+=work.result
        threadings.clear()
    return result

class BookMainwindow(Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self):
        super(BookMainwindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("挂号信息采集器")
        self.departments=[]
        try:
            self.keywords=load_keywords()
        except:
            self.keywords=['内分泌','肾内科','免疫内科','消化内科','神经内科','妇科','皮','乳腺','中医','感染内科','呼吸内科']
        self.exists=[]
        self.is_start=False
        self.init()

    def init(self):
        self.pushButton.clicked.connect(self.click_pushbutton)
        self.actionClose.triggered.connect(self.close)
        text=''
        for keyword in self.keywords:
            text+=keyword+','
        self.lineEdit_2.setText(text)

    def click_pushbutton(self):
        self.pushButton.setText("抓取中")
        self.pushButton.setEnabled(False)
        self.get_book_infor()

    def get_keywords(self):
        text=self.lineEdit_2.text()
        self.keywords.clear()
        for keyword in text.split(','):
            keyword=keyword.replace(' ','')
            if keyword!='':
                self.keywords.append(keyword)

    def get_book_infor(self):
        self.get_keywords()
        date=self.lineEdit.text().replace(' ','')
        self.crawler=BookInfor(self.keywords,date)
        self.crawler._finish_signal.connect(self.load_result)
        self.crawler.start()

    def warning(self,text):
        box=QtWidgets.QMessageBox.information(self,"更新",text)
        set_text=''
        for item in self.exists:
            set_text+=item
        self.textEdit.setText(set_text)

    def load_result(self,result):
        text=''
        for item in result:
            if item not in self.exists:
                text+=item
        self.exists.clear()
        self.exists=result
        if text!='':
            self.warning(text)

class BookInfor(QtCore.QThread):
    _finish_signal=QtCore.pyqtSignal(list)
    def __init__(self,keywords,date):
        super(BookInfor,self).__init__()
        self.keywords=keywords
        self.date=date


    def run(self):
        while True:
            try:
                self.departments=get_department('1',self.keywords)
                break
            except:
                continue
        while True:
            template="\r\n医院:%s\r\n科室:%s\r\n医院号源:%s\r\n医生:%s\r\n费用:%s\r\n"
            print(local_time(),"开始抓取")
            depart_items=copy.deepcopy(self.departments)
            items=update_infor(depart_items,self.date)
            result=[]
            for item in items:
                if self.date not in item[2]:
                    continue
                text=template%tuple(item)
                result.append(text)
            print(local_time(),"抓取完成")
            self._finish_signal.emit(result)
            time.sleep(1)

if __name__ == '__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    management=BookMainwindow()
    management.show()
    sys.exit(app.exec_())
