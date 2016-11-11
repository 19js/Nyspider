from selenium import webdriver
from bs4 import BeautifulSoup
import time

browser=webdriver.Chrome("./chromedriver")
browser.get('http://hotels.ctrip.com/hotel/zhuhai31')
browser.implicitly_wait(10)
hotels=[eval(line) for line in open('hotels.txt','r')]
flag=True
for hotel in hotels:
    hotel_id=hotel[2].split('.')[0].split('/')[-1]
    if hotel_id!='437289' and flag:
        continue
    flag=False
    f=open('result.txt','a')
    f.write(str(hotel+[''])+'\n')
    f.close()
    page=1
    '''
    if hotel_id=='371212':
        page=148
    '''
    endpage=1000
    while page<=endpage:
        try:
            browser.get('http://hotels.ctrip.com/hotel/dianping/%s_p%st0.html'%(hotel_id,page))
            html=browser.page_source
        except:
            continue
        time.sleep(2)
        try:
            comments=BeautifulSoup(html,'lxml').find_all('div',{'class':'comment_block'})
            if comments==None:
                break
        except:
            break
        if '以下为酒店3年前历史点评' in str(comments):
            break
        f=open('result.txt','a')
        print(len(comments))
        for line in comments:
            f.write(str(hotel+[str(line)])+'\n')
        f.close()
        print(page,hotel[0])
        if endpage==1000:
            try:
                endpage=BeautifulSoup(html,'lxml').find('div',{'class':'c_page_list'}).find_all('a')[-1].get('value')
                endpage=int(endpage)
            except:
                break
        page+=1
