import requests
from bs4 import BeautifulSoup
import time
import openpyxl


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def disease_urls():
    page=0
    while True:
        html=requests.get('http://jbk.39.net/bw_t1_p%s'%page,headers=headers).text
        try:
            table=BeautifulSoup(html,'lxml').find('div',{'class':'lbox_art'}).find_all('h3')
        except:
            break
        if len(table)==0:
            break
        f=open('urls.txt','a')
        for item in table:
            name=item.find('a').get('title')
            url=item.find('a').get('href')
            f.write(name+'|'+url+'\n')
        f.close()
        print(page,'ok')
        page+=1

def infor(name,url):
    line=[name]
    try:
        html=requests.get(url+'yfhl/',headers=headers,timeout=30).text.encode('iso-8859-1').decode('gbk','ignore')
        text=BeautifulSoup(html,'lxml').find('div',{'class':'chi-know'}).find('div',{'class':'art-box'}).get_text()
        line.append(text)
    except:
        line.append('')
    try:
        html=requests.get(url+'hl/',headers=headers,timeout=30).text.encode('iso-8859-1').decode('gbk','ignore')
        text=BeautifulSoup(html,'lxml').find('div',{'class':'chi-know'}).find('div',{'class':'art-box'}).get_text()
        line.append(text)
    except:
        line.append('')
    try:
        html=requests.get(url+'ysbj/',headers=headers,timeout=30).text.encode('iso-8859-1').decode('gbk','ignore')
        text=''
        try:
            text=BeautifulSoup(html,'lxml').find('div',{'class':'chi-know'}).find('div',{'class':'yinshi_table'}).get_text()
        except:
            pass
        table=BeautifulSoup(html,'lxml').find('div',{'class':'chi-know'}).find_all('div',{'class':'art-box'})
        for div in table:
            text+='\n'+div.get_text()
        line.append(text)
    except:
        line.append('')
    try:
        html=requests.get(url+'bfbz/',headers=headers,timeout=30).text.encode('iso-8859-1').decode('gbk','ignore')
        try:
            text=BeautifulSoup(html,'lxml').find('div',{'class':'chi-know'}).find('dl',{'class':'links'}).get_text()
        except:
            text=''
        try:
            text+='\n'+BeautifulSoup(html,'lxml').find('div',{'class':'chi-know'}).find('div',{'class':'art-box'}).get_text()
        except:
            pass
        line.append(text)
    except:
        line.append('')
    try:
        html=requests.get(url+'jzzn/',headers=headers,timeout=30).text.encode('iso-8859-1').decode('gbk','ignore')
        table=BeautifulSoup(html,'lxml').find('div',id='contentText').find_all('dl')
        text=['']*4
        for dl in table:
            try:
                title=dl.find('dt').get_text()
                value=dl.get_text().replace(title,'')
            except:
                continue
            if '典型症状' in title:
                text[0]+=value
            if '就诊前准备' in title:
                text[1]+=value
            if '常见问诊内容' in title:
                text[2]+=value
            if '重点检查项目' in title:
                text[3]+=value
        line+=text
    except:
        line+=['']*4
    try:
        html=requests.get(url+'jcjb/',headers=headers,timeout=30).text.encode('iso-8859-1').decode('gbk','ignore')
        table=BeautifulSoup(html,'lxml').find('div',{'class':'chi-know'}).find('div',{'class':'checkbox-data'}).find_all('tr')
        text=[]
        for item in table:
            tds=item.find_all('td')
            try:
                name=item.find('a').get_text()
                url=item.find('a').get('href')
                area=tds[1].get_text()
                check_infor=check(url)
                text+=[name,area]+check_infor
            except:
                continue
    except:
        text=[]
    line+=text
    return line

def check(url):
    html=requests.get(url,headers=headers,timeout=30).text.encode('iso-8859-1').decode('gbk','ignore')
    soup=BeautifulSoup(html,'lxml').find('article')
    try:
        intro=soup.find('div',id='intro').find('span').get_text()
    except:
        intro=''
    try:
        table=soup.find_all('div',{'class':'catalogItem'})
        mention=''
        for item in table:
            try:
                title=item.find('h3').get_text()
            except:
                continue
            if '注意事项' in title:
                mention=item.find('div',{'class':'text'}).get_text()
    except:
        mention=''
    return [intro,mention]

def main():
    urls=[line.replace('\n','').split('|') for line in open('urls.txt','r')]
    count=0
    for item in urls:
        try:
            line=infor(item[0],item[1])
        except:
            failed=open('failed.txt','a')
            failed.write(str(item)+'\n')
            failed.close()
            continue
        f=open('result.txt','a')
        f.write(str(line)+'\n')
        f.close()
        print(item,'ok')
        count+=1
        print(count)
main()
