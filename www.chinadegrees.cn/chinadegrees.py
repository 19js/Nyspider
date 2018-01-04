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
    for project in projects:
        url=projects[project]
        result=get_major_info(url)
        with open('majors.txt','a') as f:
            for major in result:
                f.write(str([project]+major)+'\n')

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

def main():
    # for line in open('./majors.txt','r'):
    #     item=eval(line)
    #     major_result=get_major_rank(item[-1])
    #     f=open('result.txt','a')
    #     for major in major_result:
    #         f.write(str(item+major)+'\n')
    #     f.close()
    result=[]
    for line in open('./result.txt','r'):
        result.append(eval(line))
    write_to_excel(result,'result.xlsx',True)

if __name__=='__main__':
    main()