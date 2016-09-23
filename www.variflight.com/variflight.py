import requests
from bs4 import BeautifulSoup
import time
import random
import os
from PIL import Image
import math

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
        'X-Requested-With':"XMLHttpRequest",
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
    count=0
    while True:
        try:
            content=session.get(img_url,timeout=30).content
            return content
        except:
            count+=1
            if count==4:
                return False


def parser(url):
    count=0
    session=requests.session()
    while True:
        try:
            html=session.get(url,headers=get_headers(),timeout=30).text
            break
        except:
            count+=1
            if count==4:
                return False
    table=BeautifulSoup(html.replace('\n','').replace('\t',''),'html.parser').find('ul',id='list').find_all('div',{'class':'li_com'})
    result=[]
    for item in table:
        try:
            flight={}
            spans=item.find_all('span')
            flight['name']=spans[0].get_text()
            flight['fly_time']=spans[1].get_text()
            r_fly_time_url='http://www.variflight.com/'+spans[2].find('img').get('src')
            try:
                content=get_image(r_fly_time_url,session)
                flight['r_fly_time_img']=content
            except:
                flight['r_fly_time_img']=False
            flight['from']=spans[3].get_text()
            flight['arrive_time']=spans[4].get_text()
            r_arrive_time_url='http://www.variflight.com/'+spans[5].find('img').get('src')
            try:
                content=get_image(r_arrive_time_url,session)
                flight['r_arrive_time_img']=content
            except:
                flight['r_arrive_time_img']=False
            flight['to']=spans[6].get_text()
            on_time_url='http://www.variflight.com/'+spans[7].find('img').get('src')
            try:
                content=get_image(on_time_url,session)
                flight['on_time_img']=content
            except:
                flight['on_time_img']=False
            try:
                flight['status']=spans[8].get_text()
            except:
                flight['status']=''
            result.append(flight)
        except:
            continue
    return result

def crawler(date):
    #timenow=time.strftime('%Y%m%d_%H%M%S')
    f=open(date+'.txt','w',encoding='utf-8')
    recognise=CaptchaRecognize()
    for line in open('flights.txt','r',encoding='utf-8'):
        line=line.replace('\r','').replace('\n','')
        url=line.split('|')[-1]
        try:
            item=parser(url+date)
            if item==False:
                continue
        except:
            continue
        if item==[]:
            continue
        for flight in item:
            keys=['r_arrive_time_img','r_fly_time_img','on_time_img']
            for key in keys:
                content=flight[key]
                if content==False:
                    flight[key]=''
                    continue
                flight[key]=recognise.recognise(content)
            keys=['name','fly_time','r_fly_time_img','from','arrive_time','r_arrive_time_img','to','on_time_img','status']
            write_line=''
            for key in keys:
                write_line+=flight[key]+'\t'
            f.write(write_line+'\r\n')
        print(line,'ok')
    f.close()

crawler('20160920')
