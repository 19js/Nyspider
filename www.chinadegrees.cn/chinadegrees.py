from util import *
import time
from bs4 import BeautifulSoup


projects={
    '人文社科类':'xkpmGXZJ2016.jsp?xkdm=01,02,03,04,05,06',
    '理学':'xkpmGXZJ2016.jsp?xkdm=07',
    '工学':'xkpmGXZJ2016.jsp?xkdm=08',
    '农学':'xkpmGXZJ2016.jsp?xkdm=09',
    '医学':'xkpmGXZJ2016.jsp?xkdm=10',
    '管理学':'xkpmGXZJ2016.jsp?xkdm=12',
    '艺术学':'xkpmGXZJ2016.jsp?xkdm=13'
}

def get_major_info(url):
    page_url='http://www.chinadegrees.cn/webrms/pages/Ranking/'+url
    res=build_request(page_url)
    res_text=res.text
    table=BeautifulSoup(res_text,'lxml').find('div',id='leftgundong').find_all('p')
    result=[]
    for item in table:
        link=item.find('a').get('href')
        major=item.find('a').get_text()
        result.append([major,link])
    return result

def get_majors():
    major_list=[]
    for project in projects:
        url=projects[project]
        result=get_major_info(url)
        for major in result:
            major_list.append([project]+major)
    return major_list

def get_major_rank(url):
    page_url='http://www.chinadegrees.cn/webrms/pages/Ranking/'+url
    res=build_request(page_url)
    res_text=res.text
    table=BeautifulSoup(res_text,'lxml').find('table',{'width':'610px'}).find_all('tr')
    current_grade=''
    result=[]
    for item in table:
        tds=item.find_all('td')
        if len(tds)==2:
            current_grade=tds[0].get_text()
        college=tds[-1].get_text().replace('\xa0','|').split('|')
        result.append([current_grade,college[0],college[-1]])
    return result

def crawl():
    major_list=get_majors()
    result=[]
    for item in major_list:
        major_result=get_major_rank(item[-1])
        for major_info in major_result:
            result.append(item+major_info)
        print(item,'OK')        
    write_to_excel(result,'result.xlsx',True)

if __name__=='__main__':
    crawl()