from selenium import webdriver
from bs4 import BeautifulSoup
import time


def parser(soup):
    parser_line=[]
    try:
        name=soup.find('p',{'class':'name'}).get_text()
        parser_line.append(name)
    except:
        parser_line.append('-')
    try:
        score=soup.find('span',{'class':'score'}).get_text()
        parser_line.append(score)
    except:
        parser_line.append('-')
    try:
        room=soup.find('a',{'class':'room'}).get_text()
        parser_line.append(room)
    except:
        parser_line.append('-')
    try:
        date=soup.find('span',{'class':'date'}).get_text()
        parser_line.append(date)
    except:
        parser_line.append('-')
    try:
        p_type=soup.find('span',{'class':'type'}).get_text()
        parser_line.append(p_type)
    except:
        parser_line.append('-')
    try:
        text=soup.find('div',{'class':'J_commentDetail'}).get_text()
        parser_line.append(text)
    except:
        try:
            text=soup.find('p',{'class':'J_commentDetail'}).get_text()
            parser_line.append(text)
        except:
            parser_line.append('-')
    try:
        reply_date=soup.find('span',{'class':'time'}).get_text()
        parser_line.append(reply_date)
    except:
        parser_line.append('-')
    try:
        reply=soup.find('div',{'class':'htl_reply'}).find('p',{'class':'text'}).get_text()
        parser_line.append(reply)
    except:
        parser_line.append('-')
    return parser_line

browser=webdriver.Chrome("./chromedriver")
browser.get('http://hotels.ctrip.com/hotel/zhuhai31')
browser.implicitly_wait(10)
hotels=[line.split('\t') for line in open('hotels.txt','r')]
s=True
for hotel in hotels:
    hotel_id=hotel[1].split('.html')[0].split('/')[-1]
    if hotel_id!='2030855' and s:
        continue
    s=False
    browser.get('http://hotels.ctrip.com/hotel/dianping/%s_p%st0.html'%(hotel_id,1))
    time.sleep(2)
    m=browser.find_element_by_class_name('select_sort')
    m.find_element_by_xpath("//option[@value='1']").click()
    time.sleep(2)
    flag=True
    while flag:
        html=browser.page_source
        try:
            browser.find_element_by_class_name('comment_tab_main')
            comments=BeautifulSoup(html,'lxml').find('div',{'class':'comment_tab_main'}).find_all('div',{'class':'comment_block'})
        except:
            continue
        f=open('result.txt','a')
        for soup in comments:
            line=parser(soup)
            if '-11-' not in line[-2]:
                flag=False
                break
            f.write(str(hotel+line)+'\n')
        f.close()
        if flag!=True:
            break
        try:
            m=browser.find_element_by_class_name('c_page_box')
            m.find_element_by_class_name('c_down').click()
            time.sleep(2)
        except:
            pass
