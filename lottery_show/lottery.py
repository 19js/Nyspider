import requests
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(444, 592)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox.setGeometry(QtCore.QRect(90, 30, 201, 30))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 30, 91, 20))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(330, 530, 96, 28))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 70, 421, 451))
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 444, 28))
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
        self.comboBox.setItemText(0, _translate("MainWindow", "1秒"))
        self.comboBox.setItemText(1, _translate("MainWindow", "5秒"))
        self.comboBox.setItemText(2, _translate("MainWindow", "10秒"))
        self.comboBox.setItemText(3, _translate("MainWindow", "20秒"))
        self.comboBox.setItemText(4, _translate("MainWindow", "30秒"))
        self.comboBox.setItemText(5, _translate("MainWindow", "40秒"))
        self.comboBox.setItemText(6, _translate("MainWindow", "50秒"))
        self.comboBox.setItemText(7, _translate("MainWindow", "1分钟"))
        self.comboBox.setItemText(8, _translate("MainWindow", "2分钟"))
        self.comboBox.setItemText(9, _translate("MainWindow", "3分钟"))
        self.comboBox.setItemText(10, _translate("MainWindow", "4分钟"))
        self.comboBox.setItemText(11, _translate("MainWindow", "5分钟"))
        self.comboBox.setItemText(12, _translate("MainWindow", "10分钟"))
        self.comboBox.setItemText(13, _translate("MainWindow", "20分钟"))
        self.label.setText(_translate("MainWindow", "刷新时间："))
        self.pushButton.setText(_translate("MainWindow", "复制"))
        self.menu.setTitle(_translate("MainWindow", "菜单"))
        self.action.setText(_translate("MainWindow", "退出"))

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def hbbmwx():
    html=requests.get("http://hbbmwx.com/gw_getplandata.html",headers=headers,timeout=30).text.encode('ISO-8859-1').decode('utf-8','ignore')
    result=BeautifulSoup(html,'lxml').find('b').get_text().replace('千里马团队分析师推荐','')
    return result

def w_2727():
    html=requests.get("http://2727808.com/gw_getplandata.html",headers=headers,timeout=30).text.encode('ISO-8859-1').decode('utf-8','ignore')
    result=BeautifulSoup(html,'lxml').find('b').get_text().replace('黑金团队分析师推荐','')
    return result

def w_15050():
    html=requests.get("http://15050.com/gw_getplandata.html",headers=headers,timeout=30).text.encode('ISO-8859-1').decode('utf-8','ignore')
    result=BeautifulSoup(html,'lxml').find('b').get_text().replace('领头羊团队分析师推荐','')
    return result

def w_0077():
    html=requests.get("http://0077.la/gw_getplandata.html",headers=headers,timeout=30).text.encode('ISO-8859-1').decode('utf-8','ignore')
    result=BeautifulSoup(html,'lxml').find('b').get_text().replace('奔驰团队分析师推荐','')
    return result


class Lottery(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Lottery,self).__init__()
        self.setupUi(self)
        self.timeid=self.startTimer(2000)
        self.board=QtGui.QGuiApplication.clipboard()
        self.initSetting()
        self.result_hbb=[]
        self.result_2727=[]
        self.result_150=[]
        self.result_0077=[]
        self.setWindowTitle("时时彩")

    def initSetting(self):
        self.action.triggered.connect(self.close)
        self.comboBox.currentIndexChanged.connect(self.timeChanged)
        self.pushButton.clicked.connect(self.copy)

    def copy(self):
        text=''
        for item in self.result_hbb:
            text+=item+'\n'
        text+='----------\r\n'
        for item in self.result_2727:
            text+=item+'\n'
        text+='----------\r\n'
        for item in self.result_0077:
            text+=item+'\n'
        text+='----------\r\n'
        for item in self.result_150:
            text+=item+'\n'
        text+='----------\r\n'
        self.board.setText(text.replace(':',''))

    def timeChanged(self):
        self.killTimer(self.timeid)
        text=self.comboBox.currentText()
        if '秒' in text:
            delay=int(text.replace('秒',''))*1000
        else:
            delay=int(text.replace('分钟',''))*1000*60
        self.timeid=self.startTimer(delay)

    def timerEvent(self,event):
        text=''
        try:
            result=hbbmwx()
        except:
            result=''
        if result not in self.result_hbb and result!='':
            self.result_hbb.append(result)

        try:
            result=w_2727()
        except:
            result=''
        if result not in self.result_2727 and result!='':
            self.result_2727.append(result)

        try:
            result=w_0077()
        except:
            result=''
        if result not in self.result_0077 and result!='':
            self.result_0077.append(result)

        try:
            result=w_15050()
        except:
            result=''
        if result not in self.result_150 and result!='':
            self.result_150.append(result)

        for item in self.result_hbb:
            text+=item+'\n'
        text+='----------\r\n'
        for item in self.result_2727:
            text+=item+'\n'
        text+='----------\r\n'
        for item in self.result_0077:
            text+=item+'\n'
        text+='----------\r\n'
        for item in self.result_150:
            text+=item+'\n'
        text+='----------\r\n'
        self.textEdit.setText(text.replace(':',''))


if __name__=='__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    management=Lottery()
    management.show()
    sys.exit(app.exec_())
