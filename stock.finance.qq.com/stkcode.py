import requests
from bs4 import BeautifulSoup


def get_stkcode():
    f=open('stkcode.txt','w')
    page=1
    while True:
        html=requests.get('http://hq.gucheng.com/List.asp?Type=A&Sort=&Page=%s'%page).text.encode('ISO-8859-1').decode('GBK','ignore')
        table=BeautifulSoup(html,'lxml').find('div',{'class':'hq_big_bk md_6'}).find_all('tr')
        for tr in table[1:-1]:
            tds=tr.find_all('td')
            line=tds[1].get_text()+'---'+tds[0].get_text()
            print(line)
            f.write(line+'\r\n')
        page+=1
        if page==139:
            break
    f.close()

get_stkcode()
