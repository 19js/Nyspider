import requests
from bs4 import BeautifulSoup
import json
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import datetime

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1102, 733)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralWidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 220, 1081, 481))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 60, 41, 31))
        self.label.setObjectName("label")
        self.name_lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.name_lineEdit.setGeometry(QtCore.QRect(80, 60, 101, 31))
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(200, 60, 71, 31))
        self.label_2.setObjectName("label_2")
        self.person_num_lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.person_num_lineEdit.setGeometry(QtCore.QRect(270, 60, 71, 31))
        self.person_num_lineEdit.setObjectName("person_num_lineEdit")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(350, 60, 41, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(400, 66, 81, 21))
        self.label_4.setObjectName("label_4")
        self.tang1_lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.tang1_lineEdit.setGeometry(QtCore.QRect(480, 60, 81, 31))
        self.tang1_lineEdit.setObjectName("tang1_lineEdit")
        self.tang1_lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.tang1_lineEdit_2.setGeometry(QtCore.QRect(560, 60, 91, 31))
        self.tang1_lineEdit_2.setObjectName("tang1_lineEdit_2")
        self.tang1_lineEdit_3 = QtWidgets.QLineEdit(self.centralWidget)
        self.tang1_lineEdit_3.setGeometry(QtCore.QRect(650, 60, 81, 31))
        self.tang1_lineEdit_3.setObjectName("tang1_lineEdit_3")
        self.label_5 = QtWidgets.QLabel(self.centralWidget)
        self.label_5.setGeometry(QtCore.QRect(750, 66, 71, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralWidget)
        self.label_6.setGeometry(QtCore.QRect(946, 60, 16, 31))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralWidget)
        self.label_7.setGeometry(QtCore.QRect(10, 110, 51, 31))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralWidget)
        self.label_8.setGeometry(QtCore.QRect(220, 110, 21, 21))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralWidget)
        self.label_9.setGeometry(QtCore.QRect(400, 110, 61, 31))
        self.label_9.setObjectName("label_9")
        self.month_in_lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.month_in_lineEdit.setGeometry(QtCore.QRect(480, 110, 81, 31))
        self.month_in_lineEdit.setObjectName("month_in_lineEdit")
        self.label_10 = QtWidgets.QLabel(self.centralWidget)
        self.label_10.setGeometry(QtCore.QRect(570, 110, 21, 31))
        self.label_10.setObjectName("label_10")
        self.month_in_lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.month_in_lineEdit_2.setGeometry(QtCore.QRect(590, 110, 81, 31))
        self.month_in_lineEdit_2.setObjectName("month_in_lineEdit_2")
        self.label_11 = QtWidgets.QLabel(self.centralWidget)
        self.label_11.setGeometry(QtCore.QRect(750, 110, 71, 31))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralWidget)
        self.label_12.setGeometry(QtCore.QRect(920, 116, 21, 21))
        self.label_12.setObjectName("label_12")
        self.newprice_lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.newprice_lineEdit.setGeometry(QtCore.QRect(820, 110, 91, 31))
        self.newprice_lineEdit.setObjectName("newprice_lineEdit")
        self.newprice_lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.newprice_lineEdit_2.setGeometry(QtCore.QRect(940, 110, 91, 31))
        self.newprice_lineEdit_2.setObjectName("newprice_lineEdit_2")
        self.label_13 = QtWidgets.QLabel(self.centralWidget)
        self.label_13.setGeometry(QtCore.QRect(10, 160, 71, 31))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralWidget)
        self.label_14.setGeometry(QtCore.QRect(180, 166, 21, 21))
        self.label_14.setObjectName("label_14")
        self.last_tang_lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.last_tang_lineEdit.setGeometry(QtCore.QRect(80, 160, 91, 31))
        self.last_tang_lineEdit.setObjectName("last_tang_lineEdit")
        self.last_tang_lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.last_tang_lineEdit_2.setGeometry(QtCore.QRect(210, 160, 81, 31))
        self.last_tang_lineEdit_2.setObjectName("last_tang_lineEdit_2")
        self.label_15 = QtWidgets.QLabel(self.centralWidget)
        self.label_15.setGeometry(QtCore.QRect(400, 166, 71, 21))
        self.label_15.setObjectName("label_15")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(750, 160, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_1 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_1.setGeometry(QtCore.QRect(850, 160, 91, 31))
        self.pushButton_1.setText("重新计算")
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(950, 160, 91, 31))
        self.pushButton_2.setText("停止")
        self.pushButton_2.setObjectName("pushButton_2")
        self.upload_dateEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.upload_dateEdit.setGeometry(QtCore.QRect(820, 60, 113, 31))
        self.upload_dateEdit.setObjectName("upload_dateEdit")
        self.update_dateEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.update_dateEdit_2.setGeometry(QtCore.QRect(960, 60, 113, 31))
        self.update_dateEdit_2.setObjectName("update_dateEdit_2")
        self.share_dateEdit_1 = QtWidgets.QLineEdit(self.centralWidget)
        self.share_dateEdit_1.setGeometry(QtCore.QRect(80, 110, 131, 31))
        self.share_dateEdit_1.setObjectName("share_dateEdit_1")
        self.share_dateEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.share_dateEdit_2.setGeometry(QtCore.QRect(240, 110, 131, 31))
        self.share_dateEdit_2.setObjectName("share_dateEdit_2")
        self.newdate_dateEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.newdate_dateEdit.setGeometry(QtCore.QRect(480, 160, 171, 31))
        self.newdate_dateEdit.setObjectName("newdate_dateEdit")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1102, 22))
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
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "代码"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "府名"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "卖一价格"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "挂单数量"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "月收益"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "糖块1"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "分糖日"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "计算结果"))
        self.label.setText(_translate("MainWindow", "府名："))
        self.label_2.setText(_translate("MainWindow", "府内人数:"))
        self.label_3.setText(_translate("MainWindow", "~ 500"))
        self.label_4.setText(_translate("MainWindow", "所含大糖块:"))
        self.label_5.setText(_translate("MainWindow", "上架日期:"))
        self.label_6.setText(_translate("MainWindow", "~"))
        self.label_7.setText(_translate("MainWindow", "分糖日:"))
        self.label_8.setText(_translate("MainWindow", "~"))
        self.label_9.setText(_translate("MainWindow", "月收益："))
        self.label_10.setText(_translate("MainWindow", "~"))
        self.label_11.setText(_translate("MainWindow", "最新价格："))
        self.label_12.setText(_translate("MainWindow", "~"))
        self.label_13.setText(_translate("MainWindow", "上期分糖："))
        self.label_14.setText(_translate("MainWindow", "~"))
        self.label_15.setText(_translate("MainWindow", "最新时间："))
        self.pushButton.setText(_translate("MainWindow", "查询"))
        self.menu.setTitle(_translate("MainWindow", "菜单"))
        self.action.setText(_translate("MainWindow", "退出"))

class Ukers(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Ukers,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Ukers')
        self.base_init()
        self.table_result=[]

    def base_init(self):
        self.action.triggered.connect(self.close)
        self.pushButton.clicked.connect(self.crawl)
        self.newdate_dateEdit.setText('2016-09-16')
        self.pushButton_1.clicked.connect(self.recalculate)
        self.pushButton_2.clicked.connect(self.stop_crawl)

    def stop_crawl(self):
        try:
            self.crawler.terminate()
        except:
            pass
        self.pushButton.setEnabled(True)
        self.pushButton.setText("查询")

    def get_input_data(self):
        data={}
        data['fu_name']=self.name_lineEdit.text()
        data['dtk1']=self.tang1_lineEdit.text()
        data['dtk2']=self.tang1_lineEdit_2.text()
        data['dtk3']=self.tang1_lineEdit_3.text()
        data['price_floor']=self.newprice_lineEdit.text()
        data['price_cell']=self.newprice_lineEdit_2.text()
        data['stock_avg_bonus_floor']=self.month_in_lineEdit.text()
        data['stock_avg_bonus_cell']=self.month_in_lineEdit_2.text()
        data['pop_floor']=self.person_num_lineEdit.text()
        data['ft_floor']=self.last_tang_lineEdit.text()
        data['ft_cell']=self.last_tang_lineEdit_2.text()
        data['sj_date_floor']=self.upload_dateEdit.text().replace(' ','')
        data['sj_date_cell']=self.update_dateEdit_2.text().replace(' ','')
        data['ft_date_floor']=self.share_dateEdit_1.text().replace(' ','')
        data['ft_date_cell']=self.share_dateEdit_2.text().replace(' ','')
        data['page']=1
        data['order']=''
        data['sort']=''
        self.newest_date=self.newdate_dateEdit.text().replace(' ','')
        return data

    def table_show(self):
        self.tableWidget.clearContents()
        #self.tableWidget.setHorizontalHeaderLabels(['代码','府名','卖一价格','挂单数量',
                                              #'月收益','糖块1','分糖日期','计算结果'])
        result=sorted(self.table_result,key=lambda x:x[-1],reverse=True)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(len(result))
        for num in range(len(result)):
            for i in range(8):
                newItem=QtWidgets.QTableWidgetItem()
                newItem.setText(str(result[num][i]))
                self.tableWidget.setItem(num,i,newItem)

    def crawl(self):
        self.pushButton.setEnabled(False)
        self.pushButton.setText("查询中")
        self.table_result.clear()
        self.table_show()
        data=self.get_input_data()
        self.crawler=Crawl(data)
        self.crawler._page_ok_signal.connect(self.load_result)
        self.crawler._ok_signal.connect(self.crawl_ok)
        self.crawler.start()

    def crawl_ok(self):
        self.pushButton.setEnabled(True)
        self.pushButton.setText("查询")

    def load_result(self,result):
        keys=['code','name','sell_one','sell_one_amount','stock_avg_bonus','dtk_1','ft_date']
        for item in result:
            line=[]
            for key in keys:
                try:
                    line.append(item[key])
                except:
                    line.append('-')
            line.append(self.calculate(item))
            if line in self.table_result:
                continue
            self.table_result.append(line)
        self.table_show()

    def recalculate(self):
        self.newest_date=self.newdate_dateEdit.text()
        for index in range(len(self.table_result)):
            line=self.table_result[index]
            self.table_result[index][-1]=self.calculate({'sell_one':line[2],'stock_avg_bonus':line[4],'ft_date':line[6]})
        self.table_show()

    def calculate(self,item):
        if item['sell_one']==-1:
            return 0
        if item['sell_one']==0:
            return 0
        try:
            result=float(item['stock_avg_bonus'])+27.72-float(item['sell_one'])
            d1=time.strptime(self.newest_date,'%Y-%m-%d')
            d2=time.strptime(item['ft_date'],'%Y-%m-%d')
            d1=datetime.date(d1[0],d1[1],d1[2])
            d2=datetime.date(d2[0],d2[1],d2[2])
            days=(d1-d2).days+1
            result=result/(days*30)
            result=result/float(item['sell_one'])
        except:
            return 0
        return result


class Crawl(QtCore.QThread):
    _page_ok_signal=QtCore.pyqtSignal(list)
    _ok_signal=QtCore.pyqtSignal(int)
    def __init__(self,data):
        super(Crawl,self).__init__()
        self.data=data
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

    def login(self):
        self.session=requests.session()
        self.session.get('http://www.ukers.cn/identity/sign/sign_location',headers=self.headers)
        data={
        'phone':'',
        'password':''
        }
        self.session.post('http://www.ukers.cn/identity/sign/signin_action',data=data,headers=self.headers)

    def run(self):
        self.login()
        page=1
        while True:
            self.data['page']=page
            result=[]
            try:
                html=self.session.post('http://www.ukers.cn/stock/stocksenior/get_senior_info',data=self.data,headers=self.headers,timeout=30).text
            except:
                break
            try:
                if html.startswith(u'\ufeff'):
                    html=html.encode('utf8')[3:].decode('utf8')
                items=json.loads(html)['data']
            except:
                break
            if items==[]:
                break
            for item in items:
                try:
                    office_id=item['office_id']
                    selldata=self.get_sell(office_id)
                    item['sell_one']=selldata['sell_one']
                    item['sell_one_amount']=selldata['sell_one_amount']
                    result.append(item)
                except:
                    continue
            page+=1
            self._page_ok_signal.emit(result)
        self._ok_signal.emit(1)


    def get_sell(self,office_id):
        html=self.session.get('http://www.ukers.cn/stock/stocksenior/get_utcard_ten?id='+str(office_id),headers=self.headers,timeout=30).text
        if html.startswith(u'\ufeff'):
            html=html.encode('utf8')[3:].decode('utf8')
        data=json.loads(html)
        return data['data']

if __name__ == '__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    management=Ukers()
    management.show()
    sys.exit(app.exec_())
