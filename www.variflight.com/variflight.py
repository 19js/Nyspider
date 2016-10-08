import requests
from bs4 import BeautifulSoup
import time
import random
import os
from PIL import Image
import math
import datetime
import threading
import re


def convert_image(image):
    image=image.convert('L')
    image2=Image.new('L',image.size,255)
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix=image.getpixel((x,y))
            if pix<150:
                image2.putpixel((x,y),0)
    return image2

def cut_image(image):
    inletter=False
    foundletter=False
    letters=[]
    start=0
    end=0
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix=image.getpixel((x,y))
            if(pix==0):
                inletter=True
        if foundletter==False and inletter ==True:
            foundletter=True
            start=x
        if foundletter==True and inletter==False:
            end=x
            letters.append((start,end))
            foundletter=False
        inletter=False
    images=[]
    for letter in letters:
        img=image.crop((letter[0],0,letter[1],image.size[1]))
        images.append(img)
    return images

def buildvector(image):
    result={}
    count=0
    for i in image.getdata():
        result[count]=i
        count+=1
    return result


class CaptchaRecognize:
    def __init__(self):
        self.letters=['0','1','2','3','4','5','6','7','8','9','24','44','b','m','s']
        self.loadSet()

    def loadSet(self):
        self.imgset=[]
        for letter in self.letters:
            temp=[]
            for img in os.listdir('./icon/%s'%(letter)):
                temp.append(buildvector(Image.open('./icon/%s/%s'%(letter,img))))
            self.imgset.append({letter:temp})

    #计算矢量大小
    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    #计算矢量之间的 cos 值
    def relation(self,concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

    def recognise(self,content):
        with open('temp.png','wb') as f:
            f.write(content)
        image=Image.open('temp.png')
        image=convert_image(image)
        images=cut_image(image)
        vectors=[]
        for img in images:
            vectors.append(buildvector(img))
        result=[]
        for vector in vectors:
            guess=[]
            for image in self.imgset:
                for letter,temp in image.items():
                    relevance=0
                    num=0
                    for img in temp:
                        relevance+=self.relation(vector,img)
                        num+=1
                    relevance=relevance/num
                    guess.append((relevance,letter))
            guess.sort(reverse=True)
            result.append(guess[0])
        result_str=''
        for item in result:
            result_str+=item[1]
        result_str=result_str.replace('b','%').replace('m',':').replace('s','.')
        return result_str

def get_headers():
    headers = {
        "X-Forwarded-For":'%s.%s.%s.%s'%(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
        'Host':"www.variflight.com",
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    return headers

def flights():
    html=requests.get('http://www.variflight.com/sitemap.html?AE71649A58c77',headers=get_headers()).text
    table=BeautifulSoup(html,'html.parser').find('div',{'class':'list'}).find_all('a')
    f=open('flights.txt','a',encoding='utf-8')
    for item in table:
        try:
            url='http://www.variflight.com/'+item.get('href')+'&fdate='
            if 'flight/fnum/' not in url:
                continue
            name=item.get_text()
            f.write(name+'|'+url+'\n')
        except:
            continue
    f.close()

def get_image(img_url,session):
    headers = {
        "X-Forwarded-For":'%s.%s.%s.%s'%(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Host':"www.variflight.com",
        'Accept':"image/png,image/*;q=0.8,*/*;q=0.5",
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    count=0
    while True:
        try:
            content=session.get(img_url,headers=headers,timeout=30).content
            return content,session
        except:
            count+=1
            if count==4:
                return False,session

def get_flight_infor(url):
    count=0
    while True:
        try:
            html=requests.get(url,headers=get_headers(),timeout=30).text
            break
        except:
            count+=1
            if count==5:
                return False
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'flyProc'})
    item={}
    try:
        item['distance']=soup.find('div',{'class':'p_ti'}).find('span').get_text()
    except:
        item['distance']='-'
    try:
        item['time_length']=soup.find('div',{'class':'p_ti'}).find_all('span')[1].get_text()
    except:
        item['time_length']='-'
    try:
        item['mileage']=soup.find('li',{'class':'mileage'}).get_text().replace('机型：','')
    except:
        item['mileage']='-'
    try:
        item['age']=soup.find('li',{'class':'time'}).get_text().replace('机龄：','')
    except:
        item['age']='-'
    try:
        item['pre_time']=soup.find('li',{'class':'age'}).get_text()
        if '提前' in item['pre_time']:
            item['add_sub']='-'
        elif '晚点' in item['pre_time']:
            item['add_sub']='+'
        else:
            item['add_sub']=0
    except:
        item['pre_time']='-'
        item['add_sub']=0
    try:
        item['minutes']=int(re.findall('(\d+)分钟',item['pre_time'])[0])
    except:
        item['minutes']=0
    try:
        item['hour']=int(re.findall('(\d+)小时',item['pre_time'])[0])
    except:
        item['hour']=0
    return item

class Crawler(threading.Thread):
    def __init__(self,url,num):
        super(Crawler,self).__init__()
        self.url=url
        self.num=num

    def run(self):
        self.status=True
        try:
            self.result=parser(self.url)
        except:
            self.status=False

def parser(url):
    count=0
    session=requests.session()
    while True:
        try:
            html=session.get(url,headers=get_headers(),cookies={"orderRole":"1"},timeout=30).text
            break
        except:
            count+=1
            if count==4:
                return False
    table=BeautifulSoup(html.replace('\n','').replace('\t',''),'lxml').find('ul',id='list').find_all('li')
    result=[]
    for item in table:
        try:
            flight={}
            url='http://www.variflight.com/'+item.find('a').get('href')
            infor=get_flight_infor(url)
            for key in infor:
                flight[key]=infor[key]
            spans=item.find_all('span')
            try:
                flight['share']=item.find('a',{'class':'list_share'}).get_text()
            except:
                flight['share']='-'
            flight['name']=spans[0].find('a').get_text()
            flight['flight']=spans[0].get_text().replace(flight['name'],'')
            flight['fly_time']=spans[1].get_text()
            r_fly_time_url='http://www.variflight.com/'+spans[2].find('img').get('src')
            try:
                content,session=get_image(r_fly_time_url,session)
                flight['r_fly_time_img']=content
            except:
                flight['r_fly_time_img']=False
            try:
                flight['r_fly_time_str']=spans[2].find('em').get_text()
            except:
                flight['r_fly_time_str']=''
            flight['from']=spans[3].get_text()
            flight['arrive_time']=spans[4].get_text()
            r_arrive_time_url='http://www.variflight.com/'+spans[5].find('img').get('src')
            try:
                content,session=get_image(r_arrive_time_url,session)
                flight['r_arrive_time_img']=content
            except:
                flight['r_arrive_time_img']=False
            try:
                flight['r_arrive_time_str']=spans[5].find('em').get_text()
            except:
                flight['r_arrive_time_str']=''
            flight['to']=spans[6].get_text()
            on_time_url='http://www.variflight.com/'+spans[7].find('img').get('src')
            try:
                content,session=get_image(on_time_url,session)
                flight['on_time_img']=content
            except:
                flight['on_time_img']=False
            try:
                flight['status']=spans[8].get_text()
            except:
                flight['status']='-'
            result.append(flight)
        except:
            continue
    return result

def change(flight):
    if flight['add_sub']==0:
        if flight['arrive_time']!=flight['r_arrive_time_img']:
            flight['r_arrive_time_img'],flight['r_fly_time_img']=flight['r_fly_time_img'],flight['r_arrive_time_img']
    elif flight['add_sub']=='+':
        ar_hour=int(flight['arrive_time'].split(':')[0])
        ar_minutes=int(flight['arrive_time'].split('当地')[0].split(':')[1])
        ar_hour=ar_hour+flight['hour']
        ar_minutes+=flight['minutes']
        if ar_minutes>=60:
            ar_minutes=ar_minutes-60
            ar_hour+=1
        if ar_hour>23:
            ar_hour=ar_hour-24
        num=ar_hour*100+ar_minutes
        num1=int(flight['r_arrive_time_img'].split('当地')[0].replace(':',''))
        if num!=num1:
            flight['r_arrive_time_img'],flight['r_fly_time_img']=flight['r_fly_time_img'],flight['r_arrive_time_img']
    else:
        ar_hour=int(flight['arrive_time'].split(':')[0])
        ar_minutes=int(flight['arrive_time'].split('当地')[0].split(':')[1])
        ar_hour=ar_hour-flight['hour']
        ar_minutes-=flight['minutes']
        if ar_minutes<0:
            ar_hour-=1
            ar_minutes+=60
        if ar_hour<0:
            ar_hour+=24
        num=ar_hour*100+ar_minutes
        num1=int(flight['r_arrive_time_img'].split('当地')[0].replace(':',''))
        if num!=num1:
            flight['r_arrive_time_img'],flight['r_fly_time_img']=flight['r_fly_time_img'],flight['r_arrive_time_img']
    return flight

def flights(date):
    recognise=CaptchaRecognize()
    lines=[line.replace('\r','').replace('\n','') for line in open('flights_num.txt','r',encoding='utf-8')]
    while len(lines):
        threadings=[]
        count=0
        while count<20:
            try:
                line=lines.pop()
                url='http://www.variflight.com//flight/fnum/%s.html?AE71649A58c77=&fdate='%line
                crawler=Crawler(url+date,line)
                crawler.setDaemon(True)
                threadings.append(crawler)
                count+=1
            except:
                break
        for crawler in threadings:
            crawler.start()
        for crawler in threadings:
            crawler.join()
        f=open(date+'.txt','a',encoding='utf-8')
        for crawler in threadings:
            if crawler.status==False or crawler.result==False or crawler.result==[]:
                f.write(crawler.num+'\tFalse\n')
                continue
            for flight in crawler.result:
                keys=['r_arrive_time_img','r_fly_time_img','on_time_img']
                for key in keys:
                    content=flight[key]
                    if content==False:
                        flight[key]='-'
                        continue
                    str_time=recognise.recognise(content)
                    try:
                        flight[key]=str_time+flight[key.replace('img','str')]
                    except:
                        flight[key]=str_time
                try:
                    flight=change(flight)
                except:
                    pass
                keys=['name','share','flight','fly_time','r_fly_time_img','from','arrive_time','r_arrive_time_img','to','on_time_img','status','distance','time_length','mileage','age','pre_time']
                write_line=crawler.num+'\tTrue\t'+date+'\t'
                for key in keys:
                    write_line+=flight[key].replace('\t','')+'\t'
                write_line=write_line.replace('\r','').replace('\n','')
                f.write(write_line+'\r\n')
                print(flight['name'],flight['flight'],'ok')
        f.close()
        threadings.clear()

def day_get(d):
    oneday = datetime.timedelta(days=1)
    day = d+oneday
    day=str(day).split(' ')[0].replace('-','')
    print(day)
    return day


date_from=input("起始日期（如20160921）：")
date_to=input("结束日期:")
while True:
    try:
        flights(date_from)
    except:
        print(date_from,'failed')
    if date_from==date_to:
        break
    date_now=datetime.datetime.strptime(date_from, "%Y%m%d")
    date_from=day_get(date_now)

print('完成')
time.sleep(60)
