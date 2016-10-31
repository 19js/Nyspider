from selenium import webdriver
from bs4 import BeautifulSoup
import time

def loadNameAndArea():#加载需要抓取的名单
    lines=open('names.txt','r',encoding='utf-8').readlines()#读入文本
    userlist=[]
    for line in lines:
        userlist.append(line.replace('\r','').replace('\n',''))
    return userlist


def writeToTxt(user):#将结果写入txt
    line='\t'.join(user)
    f=open('result.txt','a',encoding='utf-8')
    f.write(line+'\r\n')
    f.close()

def parser(html):#解析网页，用的是BeautifulSoup库
    soup=BeautifulSoup(html,'html.parser').find('div',id='total')
    result=[]
    labels=['singlebattle','teambattle','totalbattle']
    for label in labels:
        table=soup.find('div',id=label)
        result.append(table.find('span',{'class':'value separate'}).get_text())
        result.append(table.find('span',{'class':'value2'}).get_text())
    return result

def getUserInfor():
    browser=webdriver.Firefox()#调用火狐浏览器
    browser.get('http://rank.kongzhong.com/wows/index.html?name=%E4%BD%BF%E5%BE%92-%E6%B8%94%E9%B6%B8&zone=north')
    browser.implicitly_wait(10)#设置页面加载等待时间
    userlist=loadNameAndArea()#获取名单
    for user in userlist:
        user=user.split('\t')#名单中 名字和区域是以\t分隔
        if '南区' in user[-1]:#判断是那一个区域
            area='south'
        else:
            area='north'
        url='http://rank.kongzhong.com/wows/index.html?name=%s&zone=%s'%(user[0],area)#构造链接
        browser.get(url)#打开链接
        time.sleep(2)#停2s等待页面加载完成
        html=browser.page_source#获取页面源码
        try:
            result=parser(html)#解析页面
        except:
            continue
        result=user+result
        writeToTxt(result)#写入txt
    browser.quit()

getUserInfor()
