# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time
from selenium import webdriver
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(957, 558)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 60, 64, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(150, 60, 91, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(490, 60, 64, 20))
        self.label_3.setObjectName("label_3")
        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox.setGeometry(QtCore.QRect(60, 60, 85, 30))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox_2.setGeometry(QtCore.QRect(230, 60, 81, 30))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_3 = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox_3.setGeometry(QtCore.QRect(540, 60, 121, 30))
        self.comboBox_3.setObjectName("comboBox_3")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(850, 60, 96, 28))
        self.pushButton.setObjectName("pushButton")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 110, 841, 411))
        self.textBrowser.setObjectName("textBrowser")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(320, 60, 64, 20))
        self.label_4.setObjectName("label_4")
        self.comboBox_4 = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox_4.setGeometry(QtCore.QRect(370, 60, 111, 30))
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.date_lineEdit=QtWidgets.QLineEdit(self.centralWidget)
        self.date_lineEdit.setGeometry(QtCore.QRect(680, 60, 161, 30))
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 857, 28))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.menu.addAction(self.action)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "设备："))
        self.label_2.setText(_translate("MainWindow", "榜单类型："))
        self.label_3.setText(_translate("MainWindow", "类别："))
        self.comboBox.setItemText(0, _translate("MainWindow", "iphone"))
        self.comboBox.setItemText(1, _translate("MainWindow", "ipad"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "付费"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "免费"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "畅销"))
        self.pushButton.setText(_translate("MainWindow", "采集"))
        self.label_4.setText(_translate("MainWindow", "地区："))
        self.comboBox_4.setItemText(0, _translate("MainWindow", "中国"))
        self.comboBox_4.setItemText(1, _translate("MainWindow", "美国"))
        self.comboBox_4.setItemText(2, _translate("MainWindow", "香港"))
        self.comboBox_4.setItemText(3, _translate("MainWindow", "台湾"))
        self.comboBox_4.setItemText(4, _translate("MainWindow", "日本"))
        self.comboBox_4.setItemText(5, _translate("MainWindow", "韩国"))
        self.menu.setTitle(_translate("MainWindow", "菜单"))
        self.action.setText(_translate("MainWindow", "退出"))


class Aso100(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Aso100,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("ASO100数据采集")
        self.genre={'购物': '6024', '图书': '6018', '游戏 ': '6014', '导航':'6010', '商品指南': '6022', '工具': '6002', '教育': '6017', '商务': '6000', '效率': '6007', '娱乐': '6016', '美食佳饮': '6023', '体育': '6004', '新闻': '6009', '摄影与录像': '6008', '社交': '6005', '参考': '6006', '财务': '6015', '报刊杂志': '6021', '天气': '6001', '旅游': '6003', '音乐': '6011', '生活': '6012', '医疗': '6020', '健康健美': '6013'}
        self.brand={'付费':'paid','免费':'free','畅销':'grossing'}
        self.country_labels={'中国':'cn','香港':'hk','台湾':'tw','美国':'us','日本':'jp','韩国':'kr'}
        self.basicInit()

    def basicInit(self):
        date=time.strftime("%Y-%m-%d",time.localtime())
        self.date_lineEdit.setText(date)
        self.pushButton.clicked.connect(self.getData)
        self.action.triggered.connect(self.close)
        for key in self.genre:
            self.comboBox_3.addItem(key)

    def getBrowser(self):
        self.browser=webdriver.Firefox()#.Chrome("./chromedriver")
        self.browser.get('http://aso100.com/account/signin')
        self.browser.implicitly_wait(10)
        '''
        self.browser.find_element_by_id('username').send_keys('username')
        self.browser.find_element_by_id('password').send_keys('passwd')
        self.browser.find_element_by_id('submit').click()
        '''
        time.sleep(3)

    def writeToExcel(self,data,filename):
        excel=Workbook(write_only=True)
        sheet=excel.create_sheet()
        for item in data:
            sheet.append(item)
        excel.save(filename)

    def parser(self,html):
        if '请完成验证后继续访问' in html:
            return False
        table=BeautifulSoup(html,'html.parser').find_all('h5')
        result=[]
        for item in table:
            item=item.get_text()
            rank=item.split('.')[0]
            name=item.replace('%s.'%rank,'')
            app=[name,rank]
            result.append(app)
        return result

    def inputCap(self):
        box=QtWidgets.QMessageBox.question(self,"滑动验证","请在浏览器中验证",QtWidgets.QMessageBox.Ok)
        if box==QtWidgets.QMessageBox.Ok:
            return True
        else:
            return False

    def login(self):
        box=QtWidgets.QMessageBox.question(self,"登录","请在浏览器中登录",QtWidgets.QMessageBox.Ok)
        if box==QtWidgets.QMessageBox.Ok:
            return True
        else:
            return False

    def getData(self):
        de=self.comboBox.currentText()
        key_brand=self.comboBox_2.currentText()
        key_genre=self.comboBox_3.currentText()
        country=self.comboBox_4.currentText()
        country_type=self.country_labels[country]
        date=self.date_lineEdit.text()
        url='http://aso100.com/rank/more/date/%s/device/%s/country/%s/brand/%s/genre/%s/?page='%(date,de,country_type,self.brand[key_brand],self.genre[key_genre])
        startpage=1
        result=[]
        hour=time.strftime("_%H%M%S",time.localtime())
        filename=date.replace('-','')+hour+'_'+de+'_'+key_brand+'_'+key_genre+'_'+country+'.xlsx'
        try:
            os.mkdir(country)
        except:
            pass
        try:
            os.mkdir("%s/%s"%(country,key_genre))
        except:
            pass
        while startpage<9:
            try:
                self.browser.get(url+str(startpage))
            except:
                self.getBrowser()
                self.login()
                continue
            time.sleep(3)
            try:
                html=self.browser.page_source
            except:
                self.getBrowser()
                continue
            apps=self.parser(html)
            if apps==False:
                self.inputCap()
                continue
            if len(apps)==0:
                break
            for app in apps:
                result.append([de,key_brand]+app+[key_genre,country])
            self.textBrowser.append(de+'-'+key_brand+'-'+key_genre+'-'+str(startpage)+'-ok\n')
            startpage+=1
        self.writeToExcel(result,'%s/%s/%s'%(country,key_genre,filename))
        self.textBrowser.append(de+'-'+key_brand+'-'+key_genre+'-ok\n')


if __name__=='__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    management=Aso100()
    management.show()
    sys.exit(app.exec_())
