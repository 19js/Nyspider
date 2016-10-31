import requests
from bs4 import BeautifulSoup
import re
import time

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def getHospitalUrl(pageurl):
    html=requests.get(pageurl,headers=headers).text
    soup=BeautifulSoup(html,'html.parser').find('div',{'class':'g-hospital-items to-margin'}).find_all('li')
    result=[]
    for li in soup:
        result.append(li.find('a').get('href'))
    return result

def getHospitalInfor(url):
    html=requests.get(url,headers=headers).text.replace('\r','').replace('\n','').replace('\t','')
    soup=BeautifulSoup(html,'html.parser').find('div',{'class':'grid-group'})
    info=soup.find('div',{'class':'info'})
    result={'url':url}
    try:
        markcount=info.find('span',{'class':'mark-count'}).get_text()
        result['mark-count']=markcount
    except:
        result['mark-count']=''
    try:
        title=info.find('h1').find('a').get_text()
        result['title']=title
    except:
        result['title']=''
    try:
        Level=info.find('h1').find('span').get_text()
        result['level']=Level
    except:
        result['level']=''
    labels=['address','tel','website','about']
    for label in labels:
        try:
            text=info.find('div',{'class':label}).find('span').get_text()
        except:
            text=''
        result[label]=text
    re_label='预约量(.*?)导医服务(.*?)患者评价(.*?)候诊时间(.*)'
    statue_text=soup.find('div',{'class':'status'}).find('div',{'class':'data'}).get_text().replace(' ','')
    status=re.findall(re_label,statue_text)[0]
    statue_labels=['Appointment_num','Service','Evaluation','Time']
    for index in range(len(status)):
        result[statue_labels[index]]=status[index]
    for key in result:
        result[key]=result[key].replace(' ','').replace('\xa0','')
    return result

def writeToText(hospitals):
    f=open('hospitals.txt','a',encoding='utf-8')
    for hos in hospitals:
        line='||'.join(hos)
        f.write(line+'\r\n')
    f.close()

def main():
    f=open('failed.txt','a')
    lables=['title','url','level','address','tel','website','about','Appointment_num','Service','Evaluation','Time']
    pagestart=1
    while pagestart<721:
        try:
            hospitalurls=getHospitalUrl('http://www.guahao.com/hospital/areahospitals?pageNo=%s'%pagestart)
        except:
            continue
        hospitals=[]
        for url in hospitalurls:
            try:
                hospital=getHospitalInfor(url)
            except:
                f.write(url+'\n')
                continue
            hos=[]
            for label in lables:
                hos.append(hospital[label])
            hospitals.append(hos)
            time.sleep(6)
        writeToText(hospitals)
        print('page ',pagestart,' ok')
        pagestart+=1
    f.close()

main()
