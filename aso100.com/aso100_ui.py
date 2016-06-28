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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(662, 444)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 60, 64, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(170, 60, 91, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(350, 60, 64, 20))
        self.label_3.setObjectName("label_3")
        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox.setGeometry(QtCore.QRect(60, 60, 85, 30))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox_2.setGeometry(QtCore.QRect(250, 60, 81, 30))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_3 = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox_3.setGeometry(QtCore.QRect(400, 60, 121, 30))
        self.comboBox_3.setObjectName("comboBox_3")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(550, 60, 96, 28))
        self.pushButton.setObjectName("pushButton")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 110, 641, 291))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 662, 28))
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
        self.menu.setTitle(_translate("MainWindow", "菜单"))
        self.action.setText(_translate("MainWindow", "退出"))


class Aso100(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Aso100,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("ASO100数据采集")
        self.genre={'购物': '6024', '图书': '6018', '游戏 ': '6014', '导航':'6010', '商品指南': '6022', '工具': '6002', '教育': '6017', '商务': '6000', '效率': '6007', '娱乐': '6016', '美食佳饮': '6023', '体育': '6004', '新闻': '6009', '摄影与录像': '6008', '社交': '6005', '参考': '6006', '财务': '6015', '报刊杂志 ': '6021', '天气': '6001', '旅游': '6003', '音乐': '6011', '生活': '6012', '医疗': '6020', '健康健美': '6013'}
        self.brand={'付费':'paid','免费':'free','畅销':'grossing'}
        self.basicInit()

    def basicInit(self):
        self.pushButton.clicked.connect(self.getData)
        self.action.triggered.connect(self.close)
        for key in self.genre:
            self.comboBox_3.addItem(key)

    def getBrowser(self):
        self.browser=webdriver.Firefox()
        self.browser.get('http://aso100.com/account/signin')
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_id('username').send_keys('username')
        self.browser.find_element_by_id('password').send_keys('passwd')
        self.browser.find_element_by_id('submit').click()
        time.sleep(4)

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
            app=[rank,name]
            result.append(app)
        return result

    def inputCap(self):
        box=QtWidgets.QMessageBox.question(self,"滑动验证","请在浏览器中验证",QtWidgets.QMessageBox.Ok)
        if box==QtWidgets.QMessageBox.Ok:
            return True
        else:
            return False

    def getData(self):
        de=self.comboBox.currentText()
        key_brand=self.comboBox_2.currentText()
        key_genre=self.comboBox_3.currentText()
        url='http://aso100.com/rank/more/device/%s/country/cn/brand/%s/genre/%s/?page='%(de,self.brand[key_brand],self.genre[key_genre])
        startpage=1
        result=[]
        apptype=[de,'中国',key_brand,key_genre]
        filename=de+'_'+key_brand+'_'+key_genre+'.xls'
        while startpage<9:
            try:
                self.browser.get(url+str(startpage))
            except:
                self.getBrowser()
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
                result.append(apptype+app)
            self.textBrowser.append(de+'-'+key_brand+'-'+key_genre+'-'+str(startpage)+'-ok\n')
            startpage+=1
        self.writeToExcel(result,filename)
        self.textBrowser.append(de+'-'+key_brand+'-'+key_genre+'-ok\n')


if __name__=='__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    management=Aso100()
    management.show()
    sys.exit(app.exec_())
