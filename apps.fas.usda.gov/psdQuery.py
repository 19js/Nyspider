# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import openpyxl
import time
from bs4 import BeautifulSoup
import re
import json


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(941, 563)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.listWidget = QtWidgets.QListWidget(self.centralWidget)
        self.listWidget.setGeometry(QtCore.QRect(240, 70, 321, 421))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(240, 36, 61, 31))
        self.label.setObjectName("label")
        self.add_pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.add_pushButton.setGeometry(QtCore.QRect(840, 290, 80, 25))
        self.add_pushButton.setObjectName("add_pushButton")
        self.del_pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.del_pushButton_2.setGeometry(QtCore.QRect(700, 290, 80, 25))
        self.del_pushButton_2.setObjectName("del_pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(610, 90, 81, 17))
        self.label_2.setObjectName("label_2")
        self.commodity_comboBox = QtWidgets.QComboBox(self.centralWidget)
        self.commodity_comboBox.setGeometry(QtCore.QRect(690, 90, 231, 25))
        self.commodity_comboBox.setObjectName("commodity_comboBox")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(620, 140, 71, 17))
        self.label_3.setObjectName("label_3")
        self.datatype_comboBox_2 = QtWidgets.QComboBox(self.centralWidget)
        self.datatype_comboBox_2.setGeometry(QtCore.QRect(690, 140, 231, 25))
        self.datatype_comboBox_2.setObjectName("datatype_comboBox_2")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(630, 190, 61, 17))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralWidget)
        self.label_5.setGeometry(QtCore.QRect(640, 240, 41, 17))
        self.label_5.setObjectName("label_5")
        self.country_comboBox_3 = QtWidgets.QComboBox(self.centralWidget)
        self.country_comboBox_3.setGeometry(QtCore.QRect(690, 190, 231, 25))
        self.country_comboBox_3.setObjectName("country_comboBox_3")
        self.year_comboBox_4 = QtWidgets.QComboBox(self.centralWidget)
        self.year_comboBox_4.setGeometry(QtCore.QRect(690, 240, 231, 25))
        self.year_comboBox_4.setObjectName("year_comboBox_4")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(690, 370, 231, 81))
        self.pushButton.setObjectName("pushButton")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralWidget)
        self.listWidget_2.setGeometry(QtCore.QRect(10, 70, 221, 421))
        self.listWidget_2.setObjectName("listWidget_2")
        self.addgroup_button = QtWidgets.QPushButton(self.centralWidget)
        self.addgroup_button.setGeometry(QtCore.QRect(10, 500, 80, 25))
        self.addgroup_button.setObjectName("addgroup_button")
        self.save_button = QtWidgets.QPushButton(self.centralWidget)
        self.save_button.setGeometry(QtCore.QRect(570, 460, 80, 31))
        self.save_button.setObjectName("save")
        self.label_6 = QtWidgets.QLabel(self.centralWidget)
        self.label_6.setGeometry(QtCore.QRect(10, 40, 51, 21))
        self.label_6.setObjectName("label_6")
        self.delgroup_button = QtWidgets.QPushButton(self.centralWidget)
        self.delgroup_button.setGeometry(QtCore.QRect(150, 500, 80, 25))
        self.delgroup_button.setObjectName("delgroup_button")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 941, 22))
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
        self.label.setText(_translate("MainWindow", "组合："))
        self.add_pushButton.setText(_translate("MainWindow", "添加"))
        self.del_pushButton_2.setText(_translate("MainWindow", "删除"))
        self.label_2.setText(_translate("MainWindow", "Commodity："))
        self.label_3.setText(_translate("MainWindow", "Data Type："))
        self.label_4.setText(_translate("MainWindow", "Country："))
        self.label_5.setText(_translate("MainWindow", "Year："))
        self.pushButton.setText(_translate("MainWindow", "开始抓取"))
        self.addgroup_button.setText(_translate("MainWindow", "添加分组"))
        self.save_button.setText(_translate("MainWindow", "保存"))
        self.label_6.setText(_translate("MainWindow", "分组："))
        self.delgroup_button.setText(_translate("MainWindow", "删除"))
        self.menu.setTitle(_translate("MainWindow", "菜单"))
        self.action.setText(_translate("MainWindow", "退出"))

class Psddata(Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self):
        super(Psddata,self).__init__()
        self.setupUi(self)
        self.datatype={}
        self.grouplist=[]
        self.commodity=[{'key': 'Almonds, Shelled Basis        ', 'value': '0577400'},{'key': 'Animal Numbers, Cattle        ', 'value': '0011000'}, {'key': 'Animal Numbers, Swine         ', 'value': '0013000'}, {'key': 'Apples, Fresh                 ', 'value': '0574000'}, {'key': 'Barley                        ', 'value': '0430000'}, {'key': 'Coffee, Green                 ', 'value': '0711100'}, {'key': 'Corn                          ', 'value': '0440000'}, {'key': 'Cotton                        ', 'value': '2631000'}, {'key': 'Dairy, Butter                 ', 'value': '0230000'}, {'key': 'Dairy, Cheese                 ', 'value': '0240000'}, {'key': 'Dairy, Dry Whole Milk Powder  ', 'value': '0224400'}, {'key': 'Dairy, Milk, Fluid            ', 'value': '0223000'}, {'key': 'Dairy, Milk, Nonfat Dry       ', 'value': '0224200'}, {'key': 'Fresh Cherries,(Sweet&Sour)   ', 'value': '0579305'}, {'key': 'Fresh Peaches & Nectarines    ', 'value': '0579309'}, {'key': 'Grapefruit, Fresh             ', 'value': '0572220'}, {'key': 'Grapes, Fresh                 ', 'value': '0575100'}, {'key': 'Lemons/Limes, Fresh           ', 'value': '0572120'}, {'key': 'Meal, Copra                   ', 'value': '0813700'}, {'key': 'Meal, Cottonseed              ', 'value': '0813300'}, {'key': 'Meal, Fish                    ', 'value': '0814200'}, {'key': 'Meal, Palm Kernel             ', 'value': '0813800'}, {'key': 'Meal, Peanut                  ', 'value': '0813200'}, {'key': 'Meal, Rapeseed                ', 'value': '0813600'}, {'key': 'Meal, Soybean                 ', 'value': '0813100'}, {'key': 'Meal, Soybean (Local)         ', 'value': '0813101'}, {'key': 'Meal, Sunflowerseed           ', 'value': '0813500'}, {'key': 'Meat, Beef and Veal           ', 'value': '0111000'}, {'key': 'Meat, Swine                   ', 'value': '0113000'}, {'key': 'Millet                        ', 'value': '0459100'}, {'key': 'Mixed Grain                   ', 'value': '0459900'}, {'key': 'Oats                          ', 'value': '0452000'}, {'key': 'Oil, Coconut                  ', 'value': '4242000'}, {'key': 'Oil, Cottonseed               ', 'value': '4233000'}, {'key': 'Oil, Olive                    ', 'value': '4235000'}, {'key': 'Oil, Palm                     ', 'value': '4243000'}, {'key': 'Oil, Palm Kernel              ', 'value': '4244000'}, {'key': 'Oil, Peanut                   ', 'value': '4234000'}, {'key': 'Oil, Rapeseed                 ', 'value': '4239100'}, {'key': 'Oil, Soybean                  ', 'value': '4232000'}, {'key': 'Oil, Soybean (Local)          ', 'value': '4232001'}, {'key': 'Oil, Sunflowerseed            ', 'value': '4236000'}, {'key': 'Oilseed, Copra                ', 'value': '2231000'}, {'key': 'Oilseed, Cottonseed           ', 'value': '2223000'}, {'key': 'Oilseed, Palm Kernel          ', 'value': '2232000'}, {'key': 'Oilseed, Peanut               ', 'value': '2221000'}, {'key': 'Oilseed, Rapeseed             ', 'value': '2226000'}, {'key': 'Oilseed, Soybean              ', 'value': '2222000'}, {'key': 'Oilseed, Soybean (Local)      ', 'value': '2222001'}, {'key': 'Oilseed, Sunflowerseed        ', 'value': '2224000'}, {'key': 'Orange Juice                  ', 'value': '0585100'}, {'key': 'Oranges, Fresh                ', 'value': '0571120'}, {'key': 'Pears, Fresh                  ', 'value': '0579220'}, {'key': 'Pistachios, Inshell Basis     ', 'value': '0577907'}, {'key': 'Poultry, Meat, Broiler        ', 'value': '0114200'}, {'key': 'Poultry, Meat, Turkey         ', 'value': '0114300'}, {'key': 'Raisins                       ', 'value': '0575200'}, {'key': 'Rice, Milled                  ', 'value': '0422110'}, {'key': 'Rye                           ', 'value': '0451000'}, {'key': 'Sorghum                       ', 'value': '0459200'}, {'key': 'Sugar, Centrifugal            ', 'value': '0612000'}, {'key': 'Tangerines/Mandarins, Fresh   ', 'value': '0571220'}, {'key': 'Walnuts, Inshell Basis        ', 'value': '0577901'}, {'key': 'Wheat                         ', 'value': '0410000'}]
        self.country=[{'key': 'WORLD TOTAL', 'value': '99'}, {'key': 'ALL COUNTRIES', 'value': '**'}, {'key': 'Afghanistan                   ', 'value': 'AF'}, {'key': 'Africa, NEC                   ', 'value': 'T3'}, {'key': 'Albania                       ', 'value': 'AL'}, {'key': 'Algeria                       ', 'value': 'AG'}, {'key': 'Angola                        ', 'value': 'AO'}, {'key': 'Anguilla                      ', 'value': 'AV'}, {'key': 'Antigua and Barbuda           ', 'value': 'AC'}, {'key': 'Argentina                     ', 'value': 'AR'}, {'key': 'Armenia                       ', 'value': 'AM'}, {'key': 'Aruba                         ', 'value': 'AA'}, {'key': 'Australia                     ', 'value': 'AS'}, {'key': 'Austria                       ', 'value': 'AU'}, {'key': 'Azerbaijan                    ', 'value': 'AJ'}, {'key': 'Azores                        ', 'value': 'Y3'}, {'key': 'Bahamas, The                  ', 'value': 'BF'}, {'key': 'Bahrain                       ', 'value': 'BA'}, {'key': 'Bangladesh                    ', 'value': 'BG'}, {'key': 'Barbados                      ', 'value': 'BB'}, {'key': 'Belarus                       ', 'value': 'BO'}, {'key': 'Belgium (without Luxembourg)  ', 'value': 'S8'}, {'key': 'Belgium-Luxembourg            ', 'value': 'BE'}, {'key': 'Belize                        ', 'value': 'BH'}, {'key': 'Benin                         ', 'value': 'DM'}, {'key': 'Bermuda                       ', 'value': 'BD'}, {'key': 'Bhutan                        ', 'value': 'BT'}, {'key': 'Bolivia                       ', 'value': 'BL'}, {'key': 'Bosnia and Herzegovina        ', 'value': 'BK'}, {'key': 'Botswana                      ', 'value': 'BC'}, {'key': 'Brazil                        ', 'value': 'BR'}, {'key': 'British Ind. Ocean Territory  ', 'value': 'IO'}, {'key': 'British Virgin Islands        ', 'value': 'VI'}, {'key': 'British West Pacific Islands  ', 'value': 'W7'}, {'key': 'Brunei                        ', 'value': 'BX'}, {'key': 'Bulgaria                      ', 'value': 'BU'}, {'key': 'Burkina                       ', 'value': 'UV'}, {'key': 'Burma                         ', 'value': 'BM'}, {'key': 'Burundi                       ', 'value': 'BY'}, {'key': 'Cambodia                      ', 'value': 'CB'}, {'key': 'Cameroon                      ', 'value': 'CM'}, {'key': 'Canada                        ', 'value': 'CA'}, {'key': 'Canary Islands                ', 'value': 'Y7'}, {'key': 'Canton and Enderbury Islands  ', 'value': 'X3'}, {'key': 'Cape Verde                    ', 'value': 'CV'}, {'key': 'Caribbean Basin               ', 'value': 'C1'}, {'key': 'Cayman Islands                ', 'value': 'CJ'}, {'key': 'Central African Republic      ', 'value': 'CT'}, {'key': 'Chad                          ', 'value': 'CD'}, {'key': 'Chile                         ', 'value': 'CI'}, {'key': 'China                         ', 'value': 'CH'}, {'key': 'Colombia                      ', 'value': 'CO'}, {'key': 'Comoros                       ', 'value': 'CN'}, {'key': 'Congo (Brazzaville)           ', 'value': 'CF'}, {'key': 'Congo (Kinshasa)              ', 'value': 'CG'}, {'key': 'Costa Rica                    ', 'value': 'CS'}, {'key': "Cote d'Ivoire                 ", 'value': 'IV'}, {'key': 'Croatia                       ', 'value': 'HR'}, {'key': 'Cuba                          ', 'value': 'CU'}, {'key': 'Cyprus                        ', 'value': 'CY'}, {'key': 'Czech Republic                ', 'value': 'EZ'}, {'key': 'Denmark                       ', 'value': 'DA'}, {'key': 'Djibouti                      ', 'value': 'DJ'}, {'key': 'Dominica                      ', 'value': 'DO'}, {'key': 'Dominican Republic            ', 'value': 'DR'}, {'key': 'Ecuador                       ', 'value': 'EC'}, {'key': 'Egypt                         ', 'value': 'EG'}, {'key': 'El Salvador                   ', 'value': 'ES'}, {'key': 'Equatorial Guinea             ', 'value': 'EK'}, {'key': 'Eritrea                       ', 'value': 'ER'}, {'key': 'Estonia                       ', 'value': 'EN'}, {'key': 'Ethiopia                      ', 'value': 'ET'}, {'key': 'EU-15                         ', 'value': 'E2'}, {'key': 'EU-25                         ', 'value': 'E3'}, {'key': 'European Union                ', 'value': 'E4'}, {'key': 'Falkland Islands (Islas Malvin', 'value': 'FA'}, {'key': 'Faroe Islands                 ', 'value': 'FO'}, {'key': 'Fernando Po                   ', 'value': 'T8'}, {'key': 'Fiji                          ', 'value': 'FJ'}, {'key': 'Finland                       ', 'value': 'FI'}, {'key': 'Former Czechoslovakia         ', 'value': 'CZ'}, {'key': 'Former Yugoslavia             ', 'value': 'YO'}, {'key': 'Fr.Ter.Africa-Issas           ', 'value': 'FT'}, {'key': 'France                        ', 'value': 'FR'}, {'key': 'French Equatorial Africa      ', 'value': 'T4'}, {'key': 'French Guiana                 ', 'value': 'FG'}, {'key': 'French Ind. Ocean Territory   ', 'value': 'X6'}, {'key': 'French Polynesia              ', 'value': 'FP'}, {'key': 'French West Indies            ', 'value': 'Y2'}, {'key': 'Gabon                         ', 'value': 'GB'}, {'key': 'Gambia, The                   ', 'value': 'GA'}, {'key': 'Gaza Strip                    ', 'value': 'GZ'}, {'key': 'Georgia                       ', 'value': 'GG'}, {'key': 'German Democratic Republic    ', 'value': 'GC'}, {'key': 'Germany                       ', 'value': 'GM'}, {'key': 'Germany, Federal Republic of  ', 'value': 'GE'}, {'key': 'Ghana                         ', 'value': 'GH'}, {'key': 'Gibraltar                     ', 'value': 'GI'}, {'key': 'Gilbert and Ellice Islands    ', 'value': 'GN'}, {'key': 'Greece                        ', 'value': 'GR'}, {'key': 'Greenland                     ', 'value': 'GL'}, {'key': 'Grenada                       ', 'value': 'GJ'}, {'key': 'Guadeloupe                    ', 'value': 'GP'}, {'key': 'Guam                          ', 'value': 'GQ'}, {'key': 'Guatemala                     ', 'value': 'GT'}, {'key': 'Guinea                        ', 'value': 'GU'}, {'key': 'Guinea-Bissau                 ', 'value': 'PU'}, {'key': 'Guyana                        ', 'value': 'GY'}, {'key': 'Haiti                         ', 'value': 'HA'}, {'key': 'Honduras                      ', 'value': 'HO'}, {'key': 'Hong Kong                     ', 'value': 'HK'}, {'key': 'Hungary                       ', 'value': 'HU'}, {'key': 'Iceland                       ', 'value': 'IC'}, {'key': 'India                         ', 'value': 'IN'}, {'key': 'Indonesia                     ', 'value': 'ID'}, {'key': 'Iran                          ', 'value': 'IR'}, {'key': 'Iraq                          ', 'value': 'IZ'}, {'key': 'Ireland                       ', 'value': 'EI'}, {'key': 'Israel                        ', 'value': 'IS'}, {'key': 'Italy                         ', 'value': 'IT'}, {'key': 'Jamaica                       ', 'value': 'JM'}, {'key': 'Japan                         ', 'value': 'JA'}, {'key': 'Jordan                        ', 'value': 'JO'}, {'key': 'Kazakhstan                    ', 'value': 'KZ'}, {'key': 'Kenya                         ', 'value': 'KE'}, {'key': 'Korea, North                  ', 'value': 'KN'}, {'key': 'Korea, South                  ', 'value': 'KS'}, {'key': 'Kosovo                        ', 'value': 'KV'}, {'key': 'Kuwait                        ', 'value': 'KU'}, {'key': 'Kyrgyzstan                    ', 'value': 'KG'}, {'key': 'Laos                          ', 'value': 'LA'}, {'key': 'Latvia                        ', 'value': 'LG'}, {'key': 'Lebanon                       ', 'value': 'LE'}, {'key': 'Leeward-Windward Islands      ', 'value': 'Y1'}, {'key': 'Lesotho                       ', 'value': 'LT'}, {'key': 'Liberia                       ', 'value': 'LI'}, {'key': 'Libya                         ', 'value': 'LY'}, {'key': 'Lithuania                     ', 'value': 'LH'}, {'key': 'Luxembourg                    ', 'value': 'LU'}, {'key': 'Macau                         ', 'value': 'MC'}, {'key': 'Macedonia                     ', 'value': 'MK'}, {'key': 'Madagascar                    ', 'value': 'MA'}, {'key': 'Madeira Islands               ', 'value': 'Y9'}, {'key': 'Malawi                        ', 'value': 'MI'}, {'key': 'Malaysia                      ', 'value': 'MY'}, {'key': 'Maldives                      ', 'value': 'MV'}, {'key': 'Mali                          ', 'value': 'ML'}, {'key': 'Malta                         ', 'value': 'MT'}, {'key': 'Martinique                    ', 'value': 'MB'}, {'key': 'Mauritania                    ', 'value': 'MR'}, {'key': 'Mauritius                     ', 'value': 'MP'}, {'key': 'Mexico                        ', 'value': 'MX'}, {'key': 'Midway Islands                ', 'value': 'MQ'}, {'key': 'Moldova                       ', 'value': 'MD'}, {'key': 'Mongolia                      ', 'value': 'MG'}, {'key': 'Montenegro                    ', 'value': 'MJ'}, {'key': 'Montserrat                    ', 'value': 'MH'}, {'key': 'Morocco                       ', 'value': 'MO'}, {'key': 'Mozambique                    ', 'value': 'MZ'}, {'key': 'Namibia                       ', 'value': 'WA'}, {'key': 'Nauru                         ', 'value': 'NR'}, {'key': 'Nepal                         ', 'value': 'NP'}, {'key': 'Netherlands                   ', 'value': 'NL'}, {'key': 'Netherlands Antilles          ', 'value': 'NA'}, {'key': 'New Caledonia                 ', 'value': 'NC'}, {'key': 'New Zealand                   ', 'value': 'NZ'}, {'key': 'Nicaragua                     ', 'value': 'NU'}, {'key': 'Niger                         ', 'value': 'NG'}, {'key': 'Nigeria                       ', 'value': 'NI'}, {'key': 'Norway                        ', 'value': 'NO'}, {'key': 'Oman                          ', 'value': 'MU'}, {'key': 'Other                         ', 'value': '--'}, {'key': 'Other Pacific Islands, NEC    ', 'value': 'Z7'}, {'key': 'Pakistan                      ', 'value': 'PK'}, {'key': 'Panama                        ', 'value': 'PN'}, {'key': 'Papua New Guinea              ', 'value': 'PP'}, {'key': 'Paraguay                      ', 'value': 'PA'}, {'key': 'Peru                          ', 'value': 'PE'}, {'key': 'Philippines                   ', 'value': 'RP'}, {'key': 'Poland                        ', 'value': 'PL'}, {'key': 'Portugal                      ', 'value': 'PO'}, {'key': 'Puerto Rico                   ', 'value': 'RQ'}, {'key': 'Qatar                         ', 'value': 'QA'}, {'key': 'Reunion                       ', 'value': 'RE'}, {'key': 'Romania                       ', 'value': 'RO'}, {'key': 'Russia                        ', 'value': 'RS'}, {'key': 'Rwanda                        ', 'value': 'RW'}, {'key': 'Ryukyu Is - Nansei Is         ', 'value': 'Z5'}, {'key': 'Samoa                         ', 'value': 'WS'}, {'key': 'Sao Tome and Principe         ', 'value': 'TP'}, {'key': 'Saudi Arabia                  ', 'value': 'SA'}, {'key': 'Senegal                       ', 'value': 'SG'}, {'key': 'Serbia                        ', 'value': 'RB'}, {'key': 'Serbia and Montenegro         ', 'value': 'SR'}, {'key': 'Seychelles                    ', 'value': 'SE'}, {'key': 'Sierra Leone                  ', 'value': 'SL'}, {'key': 'Singapore                     ', 'value': 'SN'}, {'key': 'Slovakia                      ', 'value': 'LO'}, {'key': 'Slovenia                      ', 'value': 'SI'}, {'key': 'Solomon Islands               ', 'value': 'BP'}, {'key': 'Somalia                       ', 'value': 'SO'}, {'key': 'South Africa                  ', 'value': 'SF'}, {'key': 'South Sudan                   ', 'value': 'OD'}, {'key': 'Southern Asia NEC             ', 'value': 'X8'}, {'key': 'Spain                         ', 'value': 'SP'}, {'key': 'Sri Lanka                     ', 'value': 'CE'}, {'key': 'St. Helena (Br W Afr)         ', 'value': 'SH'}, {'key': 'St. Kitts and Nevis           ', 'value': 'SC'}, {'key': 'St. Lucia                     ', 'value': 'ST'}, {'key': 'St. Pierre and Miquelon       ', 'value': 'SB'}, {'key': 'St. Vincent and the Grenadines', 'value': 'VC'}, {'key': 'Sudan                         ', 'value': 'SU'}, {'key': 'Suriname                      ', 'value': 'NS'}, {'key': 'Swaziland                     ', 'value': 'WZ'}, {'key': 'Sweden                        ', 'value': 'SW'}, {'key': 'Switzerland                   ', 'value': 'SZ'}, {'key': 'Syria                         ', 'value': 'SY'}, {'key': 'Taiwan                        ', 'value': 'TW'}, {'key': 'Tajikistan                    ', 'value': 'TI'}, {'key': 'Tanzania                      ', 'value': 'TZ'}, {'key': 'Thailand                      ', 'value': 'TH'}, {'key': 'Togo                          ', 'value': 'TO'}, {'key': 'Tonga                         ', 'value': 'TN'}, {'key': 'Trinidad and Tobago           ', 'value': 'TD'}, {'key': 'Trust Territory of the Pacific', 'value': 'NQ'}, {'key': 'Tunisia                       ', 'value': 'TS'}, {'key': 'Turkey                        ', 'value': 'TU'}, {'key': 'Turkmenistan                  ', 'value': 'TX'}, {'key': 'Turks and Caicos Islands      ', 'value': 'TK'}, {'key': 'Uganda                        ', 'value': 'UG'}, {'key': 'Ukraine                       ', 'value': 'UP'}, {'key': 'Union of Soviet Socialist Repu', 'value': 'UR'}, {'key': 'United Arab Emirates          ', 'value': 'TC'}, {'key': 'United Kingdom                ', 'value': 'UK'}, {'key': 'United States                 ', 'value': 'US'}, {'key': 'Uruguay                       ', 'value': 'UY'}, {'key': 'Uzbekistan                    ', 'value': 'UZ'}, {'key': 'Vanuatu/New Hebrides          ', 'value': 'NH'}, {'key': 'Venezuela                     ', 'value': 'VE'}, {'key': 'Vietnam                       ', 'value': 'VM'}, {'key': 'Vietnam, Peoples Republic of  ', 'value': 'V1'}, {'key': 'Vietnam, Republic of (South)  ', 'value': 'V2'}, {'key': 'Virgin Islands of the U.S.    ', 'value': 'VO'}, {'key': 'Wake Island                   ', 'value': 'WQ'}, {'key': 'West Bank                     ', 'value': 'WE'}, {'key': 'Western Sahara                ', 'value': 'WI'}, {'key': 'Yemen                         ', 'value': 'YM'}, {'key': 'Yemen (Aden)                  ', 'value': 'YS'}, {'key': 'Yemen (Sanaa)                 ', 'value': 'YE'}, {'key': 'Yugoslavia (>01/2001)         ', 'value': 'YI'}, {'key': 'Yugoslavia (>05/92)           ', 'value': 'YU'}, {'key': 'Zambia                        ', 'value': 'ZA'}, {'key': 'Zimbabwe                      ', 'value': 'RH'}, {'key': 'Caribbean                     ', 'value': '®02'}, {'key': 'Central America               ', 'value': '®03'}, {'key': 'East Asia                     ', 'value': '®18'}, {'key': 'European Union - 28           ', 'value': '®05'}, {'key': 'Former Soviet Union - 12      ', 'value': '®07'}, {'key': 'Middle East                   ', 'value': '®09'}, {'key': 'North Africa                  ', 'value': '®10'}, {'key': 'North America                 ', 'value': '®01'}, {'key': 'Oceania                       ', 'value': '®14'}, {'key': 'Other Europe                  ', 'value': '®16'}, {'key': 'South America                 ', 'value': '®04'}, {'key': 'South Asia                    ', 'value': '®12'}, {'key': 'Southeast Asia                ', 'value': '®17'}, {'key': 'Sub-Saharan Africa            ', 'value': '®11'}]
        self.init()
        try:
            self.loaddata()
        except:
            pass
        self.load_datatype()

    def init(self):
        self.commodity_values={}
        self.country_values={}
        for item in self.commodity:
            self.commodity_comboBox.addItem(item['key'])
            self.commodity_values[item['key']]=item['value']
        for item in self.country:
            self.country_comboBox_3.addItem(item['key'])
            self.country_values[item['key']]=item['value']
        self.action.triggered.connect(self.close)
        year=int(time.strftime("%Y",time.localtime()))+1
        while year>=1960:
            self.year_comboBox_4.addItem(str(year))
            year-=1
        self.del_pushButton_2.clicked.connect(self.delgroup)
        self.add_pushButton.clicked.connect(self.addgroup)
        self.pushButton.clicked.connect(self.getdata)
        self.commodity_comboBox.currentIndexChanged.connect(self.load_datatype)
        self.listWidget_2.currentRowChanged.connect(self.listshow)
        self.addgroup_button.clicked.connect(self.add_grouplist)
        self.delgroup_button.clicked.connect(self.del_grouplist)
        self.save_button.clicked.connect(self.save)


    def add_grouplist(self):
        groupname=time.strftime("%Y%m%d %H%M%S",time.localtime())
        self.grouplist.append({groupname:[]})
        self.grouplist_show()

    def grouplist_show(self):
        self.listWidget_2.clear()
        for item in self.grouplist:
            for key in item:
                self.listWidget_2.addItem(key)
        self.listWidget_2.setCurrentRow(0)

    def save(self):
        f=open('data.json','w',encoding='utf-8')
        data={'grouplist':self.grouplist,'datatype':self.datatype}
        json.dump(data,f)
        f.close()

    def loaddata(self):
        data=open('data.json','r',encoding='utf-8').read()
        data=json.loads(data)
        self.grouplist=data['grouplist']
        self.datatype=data['datatype']
        self.grouplist_show()

    def del_grouplist(self):
        if len(self.grouplist)==0:
            return
        groupindex=self.listWidget_2.currentRow()
        self.grouplist.remove(self.grouplist[groupindex])
        self.grouplist_show()

    def load_datatype(self):
        self.datatype_comboBox_2.clear()
        self.add_pushButton.setEnabled(False)
        commodity=self.commodity_comboBox.currentText()
        commodityvalue=self.commodity_values[commodity]
        try:
            result=get_datatype(commodityvalue)
        except:
            return
        for item in result:
            self.datatype_comboBox_2.addItem(item['key'])
            self.datatype[item['key']]=item['value']
        self.add_pushButton.setEnabled(True)

    def addgroup(self):
        if len(self.grouplist)==0:
            return
        groupindex=self.listWidget_2.currentRow()
        commodity=self.commodity_comboBox.currentText()
        datatype=self.datatype_comboBox_2.currentText()
        country=self.country_comboBox_3.currentText()
        year=self.year_comboBox_4.currentText()
        for key in self.grouplist[groupindex]:
            self.grouplist[groupindex][key].append([commodity,datatype,country,year])
        self.listshow()
        self.listWidget.setCurrentRow(0)

    def delgroup(self):
        if len(self.grouplist)==0:
            return
        if len(self.grouplist)==0:
            return
        groupindex=self.listWidget_2.currentRow()
        index=self.listWidget.currentRow()
        for key in self.grouplist[groupindex]:
            if len(self.grouplist[groupindex][key])==0:
                return
            self.grouplist[groupindex][key].remove(self.grouplist[groupindex][key][index])
            self.listshow()
            self.listWidget.setCurrentRow(0)

    def listshow(self):
        self.listWidget.clear()
        if len(self.grouplist)==0:
            return
        groupindex=self.listWidget_2.currentRow()
        for key in self.grouplist[groupindex]:
            for item in self.grouplist[groupindex][key]:
                text=item[0][:10]+'--'+item[1][:10]+'--'+item[2][:10]+'--'+item[3]
                self.listWidget.addItem(text)

    def getdata(self):
        self.psd=GetPsd(self.grouplist,self.commodity_values,self.datatype,self.country_values)
        self.psd.finishSignal.connect(self.savedata)
        self.psd.start()
        self.pushButton.setText('抓取中')
        self.pushButton.setEnabled(False)
        self.del_pushButton_2.setEnabled(False)
        self.add_pushButton.setEnabled(False)

    def savedata(self,data):
        for group in data:
            for filename in group:
                result=group[filename]
                keys=[]
                for item in result:
                    for key in item:
                        if key not in ['Commodity','Attribute','Country']:
                            keys.append(key)
                keys=list(set(keys))
                keys=sorted(keys,reverse=False)
                lines={}
                for item in result:
                    name=item['Commodity']+'||'+item['Attribute']+'||'+item['Country']
                    if name in lines:
                        for key in item:
                            lines[name][key]=item[key]
                    else:
                        lines[name]={}
                        for key in item:
                            lines[name][key]=item[key]
                lines=sorted(lines.items(),key=lambda x:x[0])
                result=[['Commodity','Attribute','Country']+keys]
                for item in lines:
                    line=item[0].split('||')
                    for key in keys:
                        try:
                            line.append(item[1][key])
                        except:
                            line.append('')
                    result.append(line)
                write_to_excel(result,filename+'.xlsx')
        self.pushButton.setEnabled(True)
        self.del_pushButton_2.setEnabled(True)
        self.add_pushButton.setEnabled(True)
        self.pushButton.setText('开始抓取')

def write_to_excel(result,filename):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in result:
        sheet.append(line)
    excel.save(filename)

def get_datatype(commodity):
    data={
    'visited':"1",
    'lstGroup':"all",
    'lstColumn':"Year",
    'lstOrder':"Commodity/Attribute/Country",
    'hidQuerySaveMode':"0",
    'hidLoadAttributes':"('%s')"%commodity,
    'hidSplitYear':"0577400^1,0011000^0,0013000^0,0574000^1,0430000^1,0711100^2,0440000^1,2631000^1,0230000^0,0240000^0,0224400^0,0223000^0,0224200^0,0579305^1,0579309^1,0572220^1,0575100^1,0572120^1,0813700^1,0813300^1,0814200^1,0813800^1,0813200^1,0813600^1,0813100^1,0813101^1,0813500^1,0111000^0,0113000^0,0459100^1,0459900^1,0452000^1,4242000^1,4233000^1,4235000^1,4243000^1,4244000^1,4234000^1,4239100^1,4232000^1,4232001^1,4236000^1,2231000^1,2223000^1,2232000^1,2221000^1,2226000^1,2222000^1,2222001^1,2224000^1,0585100^1,0571120^1,0579220^1,0577907^1,0114200^0,0114300^0,0575200^1,0422110^1,0451000^1,0459200^1,0612000^2,0571220^1,0577901^1,0410000^1",
    'hidShowFooter':"0",
    'hidShowRiceFooter':"0",
    'hidShowOilSoybeanFooter':"0"
    }
    html=requests.post('http://apps.fas.usda.gov/psdonline/psdQueryFrameProcess.aspx',data=data).text
    items=re.findall('appendSelectList (\(.*?\));',html)
    result=[]
    for item in items:
        item=eval(item)
        result.append({'key':item[1],'value':item[2]})
    return result

def get_psddata(commodity,datatype,country,year):
    data={
    'visited':"1",
    'lstGroup':"all",
    'lstCommodity':"%s"%commodity,
    'lstAttribute':"%s"%datatype,
    'lstCountry':"%s"%country,
    'lstDate':"%s"%year,
    'lstColumn':"Year",
    'lstOrder':"Commodity/Attribute/Country",
    'hidColumnIndex':"0",
    'hidOrderIndex':"0",
    'hidQuerySaveMode':"0",
    'hidSplitYear':"0577400^1,0011000^0,0013000^0,0574000^1,0430000^1,0711100^2,0440000^1,2631000^1,0230000^0,0240000^0,0224400^0,0223000^0,0224200^0,0579305^1,0579309^1,0572220^1,0575100^1,0572120^1,0813700^1,0813300^1,0814200^1,0813800^1,0813200^1,0813600^1,0813100^1,0813101^1,0813500^1,0111000^0,0113000^0,0459100^1,0459900^1,0452000^1,4242000^1,4233000^1,4235000^1,4243000^1,4244000^1,4234000^1,4239100^1,4232000^1,4232001^1,4236000^1,2231000^1,2223000^1,2232000^1,2221000^1,2226000^1,2222000^1,2222001^1,2224000^1,0585100^1,0571120^1,0579220^1,0577907^1,0114200^0,0114300^0,0575200^1,0422110^1,0451000^1,0459200^1,0612000^2,0571220^1,0577901^1,0410000^1",
    'hidShowFooter':"0",
    'hidShowRiceFooter':"0",
    'hidShowOilSoybeanFooter':"0"
    }
    count=0
    while True:
        try:
            html=requests.post('http://apps.fas.usda.gov/psdonline/psdResult.aspx',data=data,timeout=30).text
        except:
            count+=1
            if count==3:
                return []
            continue
        break
    try:
        table=BeautifulSoup(html,'lxml').find('table',id='gridReport').find_all('tr')
    except:
        return []
    keys=[]
    for td in table[0].find_all('th'):
        keys.append(td.get_text())
    result=[]
    for item in table[1:]:
        tds=item.find_all('td')
        if tds[0].get_text()!='\xa0':
            commodity=tds[0].get_text()
        if tds[1].get_text()!='\xa0':
            Attribute=tds[1].get_text()
        line={}
        for i in range(len(keys)):
            if i==0:
                line[keys[i]]=commodity
                continue
            if i==1:
                line[keys[i]]=Attribute
                continue
            line[keys[i]]=tds[i].get_text()
        result.append(line)
    return result

class GetPsd(QtCore.QThread):
    finishSignal=QtCore.pyqtSignal(list)
    def __init__(self,grouplist,commodity_values,datatype,country_values,parent=None):
        super(GetPsd, self).__init__(parent)
        self.commodity_values=commodity_values
        self.datatype=datatype
        self.country_values=country_values
        self.grouplist=grouplist

    def run(self):
        data=[]
        for line in self.grouplist:
            for key in line:
                result=[]
                for item in line[key]:
                    result+=get_psddata(self.commodity_values[item[0]],self.datatype[item[1]],self.country_values[item[2]],item[3])
                data.append({key:result})
            print(key,'ok')
        self.finishSignal.emit(data)

if __name__ == '__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    management=Psddata()
    management.show()
    sys.exit(app.exec_())
