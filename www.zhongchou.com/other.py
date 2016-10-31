#coding:utf-8

import requests
from bs4 import BeautifulSoup

def get_infor(text):
    headers = {
            'Host':"www.zhongchou.com",
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
    id=text.split('|')[1]
    try:
        html=requests.get('http://www.zhongchou.com/deal-show/id-'+id,headers=headers).text.encode('ISO-8859-1').decode('utf-8','ignore')
    except:
        return None
    table=BeautifulSoup(html,'html.parser').find('div',attrs={'class':'mainIn02Box'})
    title=table.find('div',attrs={'class':'jlxqTitleText siteIlB_box'}).find_all('div')
    text+='|'+title[0].get_text().replace('\n','')
    text+='|'+title[1].get_text()
    right_table=table.find('div',attrs={'class':'xqDetailRight'})
    su_table=right_table.find('div',attrs={'class':"xqDetailDataBox"}).find_all('div')
    text+='|'+su_table[0].find('p').get_text()
    text+='|'+su_table[1].find('p').get_text()
    su_table=right_table.find('div',attrs={'class':'xqRatioOuterBox'})
    text+='|'+su_table.find('p').get_text()+'|'+su_table.find('b').get_text()
    su_table=right_table.find('div',attrs={'class':'xqDetailBtnBox'}).find('a',id='deal_detail_like')
    text+='|'+su_table.find('b').get_text()
    return text

def main():
    file_d=open('data.txt','r')
    data_f=open('other.txt','a')
    num=0
    for line in file_d.readlines():
        try:
            text=get_infor(line.replace('\n',''))
        except:
            continue
        if text==None:
            continue
        data_f.write(text+'\n')
        num+=1
        print(num)
    data_f.close()

main()
