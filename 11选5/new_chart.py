#coding:utf-8

import requests
from bs4 import BeautifulSoup
import os
import time
import datetime

class Get_infor():
	def __init__(self):
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate',
			'Connection': 'keep-alive'}
		self.urls={'北京11选5': 'http://pub.icaile.com/bj11x5kjjg.php','湖北11选5': 'http://pub.icaile.com/hb11x5kjjg.php', '江西11选5': 'http://pub.icaile.com/jx11x5kjjg.php', '山西11选5': 'http://pub.icaile.com/sx11x5kjjg.php', '宁夏11选5': 'http://pub.icaile.com/nx11x5kjjg.php', '辽宁11选5': 'http://pub.icaile.com/ln11x5kjjg.php', '贵州11选5': 'http://pub.icaile.com/gz11x5kjjg.php', '云南11选5': 'http://pub.icaile.com/yn11x5kjjg.php', '西藏11选5': 'http://pub.icaile.com/xz11x5kjjg.php', '重庆11选5': 'http://pub.icaile.com/cq11x5kjjg.php', '吉林11选5': 'http://pub.icaile.com/jl11x5kjjg.php', '黑龙江11选5': 'http://pub.icaile.com/hlj11x5kjjg.php', '河南11选5': 'http://pub.icaile.com/hn11x5kjjg.php', '上海11选5': 'http://pub.icaile.com/sh11x5kjjg.php', '广东11选5': 'http://pub.icaile.com/gd11x5kjjg.php', '四川11选5': 'http://pub.icaile.com/sc11x5kjjg.php', '山东11选5': 'http://pub.icaile.com/sd11x5kjjg.php', '安徽11选5': 'http://pub.icaile.com/ah11x5kjjg.php', '浙江11选5': 'http://pub.icaile.com/zj11x5kjjg.php', '江苏11选5': 'http://pub.icaile.com/js11x5kjjg.php', '内蒙古11选5': 'http://pub.icaile.com/nmg11x5kjjg.php', '甘肃11选5': 'http://pub.icaile.com/gs11x5kjjg.php', '福建11选5': 'http://pub.icaile.com/fj11x5kjjg.php', '河北11选5': 'http://pub.icaile.com/heb11x5kjjg.php', '广西11选5': 'http://pub.icaile.com/gx11x5kjjg.php', '天津11选5': 'http://pub.icaile.com/tj11x5kjjg.php', '陕西11选5': 'http://pub.icaile.com/shx11x5kjjg.php'}
		self.count={'湖北11选5': 81, '江苏11选5': 82, '四川11选5': 78, '西藏11选5': 0, '内蒙古11选5': 75, '重庆11选5': 0, '福建11选5': 78, '山东11选5': 78, '上海11选5': 90, '北京11选5': 85, '广西11选5': 90, '江西11选5': 84, '宁夏11选5': 0, '安徽11选5': 81, '河南11选5': 72, '广东11选5': 84, '贵州11选5': 80, '陕西11选5': 79, '黑龙江11选5': 79, '辽宁11选5': 83, '河北11选5': 79, '山西11选5': 85, '吉林11选5': 79, '浙江11选5': 80, '云南11选5': 72, '天津11选5': 90, '甘肃11选5': 72}
	def run(self):
		try:
			os.mkdir('data')
		except:
			print('..')
		failed=[]
		for key in self.urls:
			try:
				html=requests.get(self.urls[key],headers=self.headers).text
			except:
				continue
			try:
				table=BeautifulSoup(html,'html.parser').find('table',attrs={'class':'today'}).find_all('tr')
			except:
				failed.append(key)
				continue
			f=open('data/'+key+'.txt','a')
			counts=[]
			date=''
			for item in table:
				try:
					text=''
					infor=item.find_all('td')
					counts.append(infor[0].get_text()[-2:])
					date=infor[0].get_text()[:-2]
					text+=infor[0].get_text()+' '
					for i in infor[2].find_all('em'):
						text+=i.get_text()+' '
					f.write(text[:-1]+'\n')
				except:
					continue
			if counts==['数据']:
				continue
			f.close()
			f=open('data/'+key+'_failed.txt','a')
			for num in range(self.count[key]):
				if num<9:
					num1='0'+str(num+1)
				else:
					num1=str(num+1)
				if num1 not in counts:
					f.write(date+num1+'\n')
			f.close()

		for key in failed:
			try:
				html=requests.get(self.urls[key],headers=self.headers).text
			except:
				continue
			try:
				table=BeautifulSoup(html,'html.parser').find('table',attrs={'class':'today'}).find_all('tr')
			except:
				continue
			f=open('data/'+key+'.txt','a')
			counts=[]
			date=''
			for item in table:
				try:
					text=''
					infor=item.find_all('td')
					counts.append(infor[0].get_text()[-2:])
					date=infor[0].get_text()[:-2]
					text+=infor[0].get_text()+' '
					for i in infor[2].find_all('em'):
						text+=i.get_text()+' '
					f.write(text[:-1]+'\n')
				except:
					continue
			if counts==['数据']:
				continue
			f=open('data/'+key+'_failed.txt','a')
			for num in range(self.count[key]):
				if num<9:
					num1='0'+str(num+1)
				else:
					num1=str(num+1)
				if num1 not in counts:
					f.write(date+num1+'\n')
			f.close()

if __name__=='__main__':
	start_time=input('输入抓取时间(格式如22:30):')
	while True:
		now = datetime.datetime.now().strftime('%H:%M')
		if now==start_time:
			work=Get_infor()
			work.run()
			print('ok')
			time.sleep(80)
