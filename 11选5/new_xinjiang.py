#coding:utf-8

import requests
from bs4 import BeautifulSoup
import os
import time
import datetime

def xinjiang():
	html=requests.get('http://pub.icaile.com/xj11x5kjjg.php?action=chart&date=yesterday&random=0.01876128008245137&id=525&async=true').text
	data=eval(html)['data']
	f=open('data/新疆.txt','a')
	counts=[]
	for item in data:
		text=''
		text+=item['dateNumber']+' '
		counts.append(item['dateNumber'][-2:])
		for i in item['list']:
			text+=i+' '
		f.write(text[:-1]+'\n')
	try:
		html=requests.get('http://pub.icaile.com/xj11x5kjjg.php').text
		table=BeautifulSoup(html,'html.parser').find('table',attrs={'class':'today'}).find_all('tr')
	except:
		print('something wrong!')
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
	f=open('data/新疆.txt_failed.txt','a')
	for num in range(97):
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
			xinjiang()
			print('ok')
			time.sleep(80)
