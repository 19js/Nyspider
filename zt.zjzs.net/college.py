from util import *
from bs4 import BeautifulSoup

def get_college_list():
    url='http://zt.zjzs.net/xuanke2018/allcollege.html'
    req=build_request(url)
    res_text=req.text.encode('iso-8859-1').decode('utf-8','ignore')
    table=BeautifulSoup(res_text,'lxml').find_all('tr',{'bgcolor':'#FFFFFF'})
    result=[]
    for item in table:
        tds=item.find_all('td')
        line=[]
        for td in tds[:-1]:
            line.append(td.get_text())
        line.append('http://zt.zjzs.net/xuanke2018/'+tds[-1].find('a').get('href'))
        result.append(line)
    return result
            

def get_info(url):
    req=build_request(url)
    res_text=req.text.encode('iso-8859-1').decode('utf-8','ignore')
    res_text=res_text.replace('<br/>','  ')
    table=BeautifulSoup(res_text,'lxml').find('div',{'class':'search'}).find_all('tr',{'bgcolor':'#FFFFFF'})
    result=[]
    for item in table:
        tds=item.find_all('td')
        line=[]
        for td in tds:
            value=td.get_text()
            if value=='':
                value='无'
            line.append(value)
        result.append(line)
    return result

def crawl():
    college_list=get_college_list()
    for college in college_list:
        result=get_info(college[-1])
        print(college)
        f=open('result.txt','a')
        for line in result:
            f.write(str(college+line)+'\n')
        f.close()

def load_txt(filename):
    for line in open(filename,'r'):
        yield eval(line)

write_to_excel(load_txt('./result.txt'),'result.xlsx')