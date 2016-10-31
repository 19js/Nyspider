import requests
from bs4 import BeautifulSoup
import time
import re
import os

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def login(username,passwd):
    data={
    'username':username,
    'password':passwd,
    'btnSubmit':""
    }
    session=requests.session()
    html=session.get('http://58.213.159.173/Login.aspx',headers=headers).text
    soup=BeautifulSoup(html,'lxml')
    data['__VIEWSTATEGENERATOR']=soup.find('input',id='__VIEWSTATEGENERATOR').get('value')
    data['__EVENTVALIDATION']=soup.find('input',id='__EVENTVALIDATION').get('value')
    data['__VIEWSTATE']=soup.find('input',id='__VIEWSTATE').get('value')
    session.post('http://58.213.159.173/Login.aspx',data=data,headers=headers)
    return session

def get_data(session,filedir,site,sites):
    html=session.get('http://58.213.159.173/Atmosphere/view/HistoryDataList.aspx',cookies={'amdb_Js_station_id':sites[site]},headers=headers).text
    soup=BeautifulSoup(html,'lxml')
    inputs=soup.find_all('input')
    data={}
    for item in inputs:
        try:
            data[item.get('id')]=item.get('value')
        except:
            continue
    data['btnCancel']=''
    data['hid_Ctrl']=''
    data['btn_Ctrl']=''
    data['hidPageSize']=15
    data['ScriptManager1']="UpdatePanel1|btnSubmit"
    data['AspNetPager1$DropDownList1']="20"
    data['AspNetPager1$AspNetPager1_input']="1"
    data['__ASYNCPOST']="true"
    keys=['__LASTFOCUS','btnSubmit','AspNetPager1$AspNetPager1_input', 'start_time', '__VIEWSTATEGENERATOR', '__ASYNCPOST', '__EVENTARGUMENT', 'AspNetPager1$DropDownList1', '__EVENTTARGET', 'end_time', 'hidPageSize', '__EVENTVALIDATION', 'ScriptManager1', 'hid_Ctrl', '__VIEWSTATE']
    postdata={}
    for key in data:
        if key in keys:
            postdata[key]=data[key]
        if 'cblChannelList' in key:
            postdata[key.replace('_','$')]=data[key]
    html=session.post('http://58.213.159.173/Atmosphere/view/HistoryDataList.aspx',data=postdata,cookies={'amdb_Js_station_id':sites[site]},headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'tbodyContainer'}).find('div',id='div_print').find_all('tr')
    f=open(filedir+'/'+site+'.txt','a',encoding='utf-8')
    for tr in table[1:16]:
        line=''
        for td in tr.find_all('td'):
            line+=td.get_text()+'\t'
        f.write(line+'\n')
    f.close()

def crawl(session,filedir):
    try:
        os.mkdir(filedir)
    except:
        pass
    html=session.get('http://58.213.159.173/Atmosphere/left.aspx',headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',id='TreeView1n0Nodes').find_all('td',{'class':'TreeView1_3'})
    sites={}
    for item in table:
        try:
            name=item.find('a').get_text()
            amdb_Js_station_id=re.findall("doGet\('','(\d+)'\)",str(item))[0]
        except:
            continue
        sites[name]=amdb_Js_station_id
    for site in sites:
        count=0
        while True:
            try:
                get_data(session,filedir,site,sites)
                break
            except:
                count+=1
                if count==3:
                    break

def main():
    users=['nj-nj',
    'sz-sz',
    'wx-wx',
    'cz-cz',
    'yz-yz',
    'zj-zj',
    'nt-nt',
    'xz-xz',
    'tz-tz',
    'yc-yc',
    'ha-ha',
    'lyg-lyg',
    'sq-sq']
    for item in users:
        user=item.split('-')
        try:
            session=login(user[0],user[1])
            crawl(session,user[0])
        except:
            timenow=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            print(timenow,user[0],'failed')
main()
