from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import scipy

class Ui_MainWindow(object):#建立用户界面
    def setupUi(self,MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1063, 705)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 80, 1061, 591))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.year1 = QtWidgets.QComboBox(self.tab)
        self.year1.setGeometry(QtCore.QRect(60, 30, 85, 31))
        self.year1.setObjectName("year1")
        self.year1.addItem("")
        self.year1.addItem("")
        self.year1.addItem("")
        self.province1 = QtWidgets.QComboBox(self.tab)
        self.province1.setGeometry(QtCore.QRect(210, 30, 101, 31))
        self.province1.setObjectName("province1")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(10, 30, 51, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(160, 30, 51, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(330, 30, 51, 21))
        self.label_3.setObjectName("label_3")
        self.type1 = QtWidgets.QComboBox(self.tab)
        self.type1.setGeometry(QtCore.QRect(380, 30, 85, 31))
        self.type1.setObjectName("type1")
        self.type1.addItem("")
        self.type1.addItem("")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(690, 30, 41, 21))
        self.label_4.setObjectName("label_4")
        self.professional1 = QtWidgets.QComboBox(self.tab)
        self.professional1.setGeometry(QtCore.QRect(740, 30, 151, 31))
        self.professional1.setObjectName("professional1")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(920, 30, 94, 29))
        self.pushButton.setObjectName("pushButton")
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setGeometry(QtCore.QRect(480, 30, 41, 21))
        self.label_10.setObjectName("label_10")
        self.school1 = QtWidgets.QComboBox(self.tab)
        self.school1.setGeometry(QtCore.QRect(530, 30, 151, 31))
        self.school1.setObjectName("school1")
        self.listWidget = QtWidgets.QListWidget(self.tab)
        self.listWidget.setGeometry(QtCore.QRect(10, 90, 1001, 461))
        self.listWidget.setObjectName("listWidget")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.professional2 = QtWidgets.QComboBox(self.tab_2)
        self.professional2.setGeometry(QtCore.QRect(610, 40, 141, 31))
        self.professional2.setObjectName("professional2")
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(550, 40, 41, 21))
        self.label_6.setObjectName("label_6")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(920, 90, 94, 29))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(180, 40, 51, 21))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(10, 40, 51, 21))
        self.label_8.setObjectName("label_8")
        self.type2 = QtWidgets.QComboBox(self.tab_2)
        self.type2.setGeometry(QtCore.QRect(230, 40, 85, 31))
        self.type2.setObjectName("type2")
        self.type2.addItem("")
        self.type2.addItem("")
        self.province2 = QtWidgets.QComboBox(self.tab_2)
        self.province2.setGeometry(QtCore.QRect(60, 40, 101, 31))
        self.province2.setObjectName("province2")
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        self.label_9.setGeometry(QtCore.QRect(770, 40, 66, 21))
        self.label_9.setObjectName("label_9")
        self.lineEdit = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit.setGeometry(QtCore.QRect(840, 40, 113, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.school2 = QtWidgets.QComboBox(self.tab_2)
        self.school2.setGeometry(QtCore.QRect(380, 40, 151, 31))
        self.school2.setObjectName("school2")
        self.label_11 = QtWidgets.QLabel(self.tab_2)
        self.label_11.setGeometry(QtCore.QRect(330, 40, 41, 21))
        self.label_11.setObjectName("label_11")
        self.listWidget_2 = QtWidgets.QListWidget(self.tab_2)
        self.listWidget_2.setGeometry(QtCore.QRect(10, 140, 1001, 411))
        self.listWidget_2.setObjectName("listWidget_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.label_5 = QtWidgets.QLabel(self.centralWidget)
        self.label_5.setGeometry(QtCore.QRect(380, 20, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("")
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1063, 29))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.menu.addAction(self.action)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "苏州大学录取分数线查询系统"))
        self.year1.setItemText(0, _translate("MainWindow", "2013"))
        self.year1.setItemText(1, _translate("MainWindow", "2014"))
        self.year1.setItemText(2, _translate("MainWindow", "2015"))
        self.label.setText(_translate("MainWindow", "年份："))
        self.label_2.setText(_translate("MainWindow", "省份："))
        self.label_3.setText(_translate("MainWindow", "文理："))
        self.type1.setItemText(0, _translate("MainWindow", "文科"))
        self.type1.setItemText(1, _translate("MainWindow", "理科"))
        self.label_4.setText(_translate("MainWindow", "专业："))
        self.pushButton.setText(_translate("MainWindow", "查询"))
        self.label_10.setText(_translate("MainWindow", "学院："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "查询"))
        self.label_6.setText(_translate("MainWindow", "专业："))
        self.pushButton_2.setText(_translate("MainWindow", "预测分数线"))
        self.label_7.setText(_translate("MainWindow", "文理："))
        self.label_8.setText(_translate("MainWindow", "省份："))
        self.type2.setItemText(0, _translate("MainWindow", "文科"))
        self.type2.setItemText(1, _translate("MainWindow", "理科"))
        self.label_9.setText(_translate("MainWindow", "一本线："))
        self.label_11.setText(_translate("MainWindow", "学院："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "预测"))
        self.label_5.setText(_translate("MainWindow", "苏州大学录取分数线查询系统"))
        self.menu.setTitle(_translate("MainWindow", "三"))
        self.action.setText(_translate("MainWindow", "退出"))


#查询模块
class Inquery(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Inquery,self).__init__()
        self.setupUi(self)
        self.getdata=Getdata()#连接数据库
        self.Init()

    def Init(self):
        year=self.year1.currentText()#获取年份
        provinces=self.getdata.getProvinces(year)#从数据库中获取省份
        for province in provinces:#将省份添加到选择框
            self.province1.addItem(province)
            self.province2.addItem(province)
        self.loadSchoolOne()#表一加载学院
        self.loadProfessionalOne()#表一加载专业
        self.loadSchoolTwo()#表二加载学院
        self.loadProfessionalTwo()#表二加载专业

        self.province1.currentIndexChanged.connect(self.loadSchoolOne)#槽函数，将选择框与具体操作连接
        self.type1.currentIndexChanged.connect(self.loadSchoolOne)
        self.year1.currentIndexChanged.connect(self.loadSchoolOne)
        self.year1.currentIndexChanged.connect(self.loadProfessionalOne)
        self.school1.currentIndexChanged.connect(self.loadProfessionalOne)

        self.province2.currentIndexChanged.connect(self.loadSchoolTwo)
        self.type2.currentIndexChanged.connect(self.loadSchoolTwo)
        self.school2.currentIndexChanged.connect(self.loadProfessionalTwo)

        self.pushButton.clicked.connect(self.inquery)
        self.pushButton_2.clicked.connect(self.calculateLine)

        self.action.triggered.connect(self.close)

    def loadSchoolOne(self):#表一加载学院
        self.school1.clear()#清空旋转框中学院
        year=self.year1.currentText()#获取选择的年份
        province=self.province1.currentText()#获取选择的省份
        category=self.type1.currentText()#获取选择的文理
        schools=self.getdata.getSchool(province,category,year)#从数据库中获取指定条件的学院
        for school in schools:#将学院添加进选择框
            self.school1.addItem(school)

    def loadProfessionalOne(self):#加载专业
        self.professional1.clear()#清空专业选择框
        year=self.year1.currentText()#获取选择的年份
        school=self.school1.currentText()#获取选择的学院
        province=self.province1.currentText()#获取选择的省份
        category=self.type1.currentText()#获取文理科
        professionals=self.getdata.getProfessional(province,year,school,category)#从数据库中获取专业
        for item in professionals:#将专业添加进选择框
            self.professional1.addItem(item)

    def loadSchoolTwo(self):#表二加载学院，同表一
        self.school2.clear()
        province=self.province2.currentText()
        category=self.type2.currentText()
        schools=self.getdata.getSchool(province,category,'2015')
        for school in schools:
            self.school2.addItem(school)

    def loadProfessionalTwo(self):#表二加载专业信息
        self.professional2.clear()
        school=self.school2.currentText()
        province=self.province2.currentText()
        category=self.type2.currentText()
        professionals=self.getdata.getProfessional(province,'2015',school,category)
        for item in professionals:
            self.professional2.addItem(item)

    def inquery(self):#查询
        self.listWidget.clear()#清空之前查询记录
        year=self.year1.currentText()#获取选择的年份
        province=self.province1.currentText()#获取选择的省份
        professional=self.professional1.currentText()#获取选择的专业
        category=self.type1.currentText()#获取选择的文理
        result=self.getdata.getLine(year,province,professional,category)#从数据库中获取数据
        for item in result:#显示
            line=''
            for i in item:
                line+=i+'\t'
            self.listWidget.addItem(line)

    def calculateLine(self):#预测
        self.listWidget_2.clear()#清空之前的预测记录

        province=self.province2.currentText()#获取选择的年份
        professional=self.professional2.currentText()#获取选择的省份
        category=self.type2.currentText()#获取选择的专业
        result=self.getdata.getLine('',province,professional,category)#从数据库中获取数据

        grade=self.lineEdit.text()#获取输入的本一线
        grade=float(grade)#将字符串转为浮点数

        if len(result)==1:#如果只有一年的数据，则计算录取线与本一线的差值，预测录取分数=输入的本一线+差值
            item=result[0]
            dif=float(item[-3])-float(item[-1])
            text=''
            for i in item[1:6]:
                text+=i+'\t'
            text+=str(grade+dif)
        else:#不止一年的数据，回归分析，求出预测分数
            lines=[]
            admittedlines=[]
            for item in result:
                lines.append(float(item[-1]))#本一线
                admittedlines.append(float(item[-3]))#录取线
            func=calculate(lines,admittedlines)#回归分析
            cal_grade=func(grade)#预测
            text=''
            for i in result[-1][1:6]:
                text+=i+'\t'
            text+=str(cal_grade)[:6]
        self.listWidget_2.addItem("历史分数线")
        for item in result:#显示历史数据
            line=''
            for i in item:
                line+=i+'\t'
            self.listWidget_2.addItem(line)
        self.listWidget_2.addItem('预测分数线')
        self.listWidget_2.addItem(text)#显示预测数据


#数据库模块，从数据库中获取数据
class Getdata():
    def __init__(self):
        self.conn=sqlite3.connect('markdata.db')#连接数据库
        self.cursor=self.conn.cursor()#创建游标

    def getSchool(self,province,category,year):#查询学院
        #选择学院
        self.cursor.execute('select school from markhistory where province="%s" and category="%s" and year="%s"'%(province,category,year))
        result=[]
        for row in self.cursor:
            result.append(row[0])
        result=list(set(result))#去重
        return result#返回查询结果

    def getProvinces(self,year):#获取省份
        self.cursor.execute("select province from markhistory where year='%s'"%year)
        result=[]
        for row in self.cursor:
            result.append(row[0])
        result=list(set(result))
        return result

    def getProfessional(self,province,year,school,category):#获取相应专业信息
        self.cursor.execute("select professional from markhistory where province='%s' and year='%s' and school='%s' and category='%s'"%(province,year,school,category))
        result=[]
        for row in self.cursor:
            result.append(row[0])
        result=list(set(result))
        return result

    def getLine(self,year,province,professional,category):#获取详细信息
        self.cursor.execute("select * from markhistory where year='%s' and province='%s' and professional='%s' and category='%s'"%(year,province,professional,category))
        if year=='':
            self.cursor.execute("select * from markhistory where province='%s' and professional='%s' and category='%s'"%(province,professional,category))
        result=[]
        for row in self.cursor:
            result.append(row)
        result=list(set(result))
        return result

def calculate(lines,admittedlines):#回归分析
    fp=scipy.polyfit(lines,admittedlines,1)#类似R语言，lm(a~b+1)
    func=scipy.poly1d(fp)
    return func

if  __name__=='__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    management=Inquery()
    management.show()
    sys.exit(app.exec_())
