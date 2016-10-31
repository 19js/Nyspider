import requests
from bs4 import BeautifulSoup
import re
import time

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    'Cookie':'_sid_=146354779185506519562612; Hm_lvt_66fcb71a7f1d7ae4ae082580ac03c957=1465826549,1465827615,1466651466,1466826044; _ipgeo=province%3A%E6%B9%96%E5%8C%97%7Ccity%3A%E6%AD%A6%E6%B1%89; searchHistory=%E3%80%82%2C%7C%C3%97%2C%7Cyi%2C%7C%E5%86%85%E7%A7%91%2C%7C%2Cclear; _area_=%7B%22provinceId%22%3A%22all%22%2C%22provinceName%22%3A%22%E5%85%A8%E5%9B%BD%22%2C%22cityId%22%3A%22all%22%2C%22cityName%22%3A%22%E4%B8%8D%E9%99%90%22%7D; _e_m=1466826043505; __rf__="4Deq6iq4P8ozUbZC0pilG2+JSpt9LfZSf3HIUJHZ0+X+UwZoIf6gqOyTHwLcc7nIuZ4AghGgupiFMOOrutJSxg=="; Hm_lpvt_66fcb71a7f1d7ae4ae082580ac03c957=1466855715; _sh_ssid_=1466854599212',
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def getDocUrl(pageurl):
    html=requests.get(pageurl,headers=headers).text
    table=BeautifulSoup(html,'html.parser').find('div',{'class':'g-doctor-items to-margin'}).find_all('li')
    result=[]
    for li in table:
        doctor={}
        doctor['url']=li.find('a').get('href')
        numinfor=li.find('div',{'class':'num-info g-clear'})
        doctor['Rate']=numinfor.find('div',{'class':'stars'}).find('em').get_text()
        count=numinfor.find('div',{'class':'count'}).find_all('em')
        try:
            doctor['Inquiry']=count[0].get_text()
        except:
            doctor['Inquiry']='-'
        try:
            doctor['Appointment']=count[1].get_text()
        except:
            doctor['Appointment']='-'
        try:
            expert_team=li.find('a',{'class':'expert-team'})
            if expert_team==None:
                doctor['expert_team']='No'
            else:
                doctor['expert_team']='Yes'
        except:
            doctor['expert_team']='No'
        result.append(doctor)
    return result

def doctorInfor(doc):
    html=requests.get(doc['url'],headers=headers).text
    soup=BeautifulSoup(html,'html.parser').find('div',id='g-cfg')
    info=soup.find('div',{'class':'info'})
    try:
        doc['like']=info.find('span',{'class':'mark-count'}).get_text()
    except:
        doc['like']='-'
    name=info.find('h1').find('strong').get_text()
    try:
        title=info.find('h1').get_text().replace(name,'')
    except:
        title='-'
    doc['name']=name
    doc['title']=title
    card_hospital=info.find('div',id='card-hospital').find_all('a')
    try:
        doc['hospital']=card_hospital[0].get_text()
    except:
        doc['hospital']='-'
    try:
        doc['department']=card_hospital[1].get_text()
    except:
        doc['department']='-'
    try:
        doc['keywords']=info.find('div',{'class':'keys'}).get_text()
    except:
        doc['keywords']='-'
    try:
        doc['Preference']=info.find('div',{'class':'goodat'}).find('span').get_text()
    except:
        doc['Preference']='-'
    try:
        doc['about']=info.find('div',{'class':'about'}).get_text()
    except:
        doc['about']='-'
    wrap=soup.find('div',{'class':'wrap'})
    try:
        grid_right=wrap.find('aside',{'class':'grid-right'}).find('section',{'class':['aside-honor']}).find('div',{'class':'grid-content'}).find_all('span')
        prize=''
        for honor in grid_right:
            prize+=' '+honor.get('title')
        doc['prize']=prize
    except:
        doc['prize']='-'
    section=wrap.find('section',{'class':['expert-consult']})
    items=section.find_all('div',{'class':'item'})
    try:
        doc['Price_photo']=items[0].get_text().replace('图文问诊','')
    except:
        doc['Price_photo']='-'
    try:
        doc['Price_phone']=items[1].get_text().replace('电话问诊','')
    except:
        doc['Price_phone']='-'
    try:
        doc['Price_video']=items[2].get_text().replace('视频问诊','')
    except:
        doc['Price_video']='-'
    try:
        doc['Photo_inquiry_num']=section.find('div',{'class':'grid-content'}).find('h4').find('strong').get_text()
    except:
        doc['Photo_inquiry_num']='-'
    section=wrap.find('section',{'class':['expert-comment']})
    try:
        doc['sharing']=section.find('div',{'class':'tip'}).get_text()
    except:
        doc['sharing']='-'
    return doc

def writeToTxt(doc):
    keys=['name', 'url','expert_team','title', 'hospital', 'department', 'about','Preference', 'keywords', 'like', 'Inquiry', 'Rate', 'Appointment','Price_photo','Photo_inquiry_num',  'Price_phone', 'Price_video', 'prize',  'sharing']
    line=''
    f=open('doctors.txt','a',encoding='utf-8')
    for key in keys:
        line+=doc[key].replace('\r','').replace('\n','').replace('\t','').replace('   ','').replace('元/次立即问诊元/次设置开诊提醒','')+'||'
    f.write(line+'\r\n')
    f.close()

def main():
    need=['内科','外科','妇产科','皮肤性病科','骨科','耳鼻咽喉科','抑郁症']
    for label in need:
        startpage=1
        endpage=100
        while startpage<endpage:
            url='http://www.guahao.com/search/expert?iSq=&fhc=&fg=&q=%E5%86%85%E7%A7%91&pi=all&p={}&ci=all&c=%E4%B8%8D%E9%99%90&o=all&es=all&hl=all&ht=all&hk=&dt=&dty=&hdi=&mf=true&fg=0&ipIsShanghai=false&searchAll=Y&hospitalId=&standardDepartmentId=&consult=&volunteerDoctor=&imagetext=&phone=&diagnosis=&sort=general&hydate=&activityId=&pageNo={}'.format(label,startpage)
            docs=getDocUrl(url)
            for doc in docs:
                try:
                    doctor=doctorInfor(doc)
                except:
                    f=open('failed_doc.txt','a',encoding='utf-8')
                    f.write(str(doc)+'\r\n')
                    f.close()
                    time.sleep(5)
                    continue
                writeToTxt(doctor)
                time.sleep(5)
            print(startpage,' ok')
            startpage+=1

main()
