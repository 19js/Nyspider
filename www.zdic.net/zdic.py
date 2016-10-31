import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import re


headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}


def get_words():
    html=open("./1.htm",'r').read()
    tables=BeautifulSoup(html,'lxml').find_all('div',{'class':'bs_index3'})
    f=open('words.txt','a')
    for table in tables:
        for li in table.find_all('li'):
            word=li.get_text()
            url='http://www.zdic.net'+li.find('a').get('href')
            f.write(str([word,url])+'\n')
    f.close()

def loads_words():
    words=[eval(line) for line in open('words.txt','r')]
    return words

def word_infor(wordurl):
    html=requests.get(wordurl,headers=headers).text.encode('iso-8859-1').decode('utf-8','ignore')
    soup=BeautifulSoup(html,'lxml').find('div',id='content')
    infor=soup.find('div',id='ziif')
    baseinfor=[]
    try:
        imgs=infor.find('div',id='ziip').find_all('img')
        text=''
        for img in imgs:
            url=img.get('src')
            if url=='/images/bwlico.gif':
                continue
            if url=='/images/cc1.gif':
                text='常用字'
                break
            if url=='/images/cc2.gif':
                text='次常用字'
                break
            if url=='/images/ty.gif':
                text='通用字'
                break
        baseinfor.append(text)
    except:
        baseinfor.append('')
    table=infor.find('table',id='z_info').find_all('tr')[1].find_all('td')
    try:
        spans=table[0].find_all('span')
        text=''
        for span in spans:
            try:
                text+=span.find('a').get_text()+','
            except:
                continue
        if text[0]=='/':
            text=text[1:]
        baseinfor.append(text)
    except:
        baseinfor.append('')
    try:
        text=table[2].find('div',{'class':'z_it2_jbs'}).get_text()
        baseinfor.append(text)
    except:
        baseinfor.append('')
    try:
        text=table[2].find('div',{'class':'z_it2_jzbh'}).get_text()
        baseinfor.append(text)
    except:
        baseinfor.append('')
    try:
        text=table[2].find('div',{'class':'z_it2_jbh'}).get_text()
        baseinfor.append(text)
    except:
        baseinfor.append('')
    for td in table:
        if '结构' not in str(td):
            continue
        try:
            struct=td.find('a').get_text()
            baseinfor.append(struct)
        except:
            baseinfor.append('')
        try:
            text=td.get_text().replace(baseinfor[-1],'')
            line=[]
            line.append(text.split('；')[0])
            try:
                text=re.findall('从(.*?)、(.*?)声',text)[0]
                line+=[text[0],text[1]]
            except:
                line+=['','']
            baseinfor+=line
        except:
            baseinfor+=['','']
        break
    table=infor.find('table',id='z_info2').find_all('tr')[1].find_all('td')
    try:
        text=table[5].get_text()
        baseinfor.append(text)
    except:
        baseinfor.append('')
    try:
        text=table[0].get_text().replace('  U+','')
        baseinfor.append(text)
    except:
        baseinfor.append('')
    tabpage=str(soup.find('div',{'class':'tab-page'})).split('<hr class="dichr"/>')
    words=[]
    word=''
    for item in tabpage:
        if '●' not in item:
            continue
        des=BeautifulSoup(item,'lxml').find_all('p')
        try:
            word=des[0].find('strong').get_text()
        except:
            pass
        index=1
        for p in des:
            if 'dicpy' not in str(p):
                index+=1
                continue
            try:
                pronunciation=re.findall('dicpy">(.*?)<script',str(p))[0]
                pronunciation_num=re.findall('spz\("(.*?)"\);',str(p))[0]
            except:
                pronunciation=p.get_text().split(' ')[0]
                pronunciation_num=''
            break
        try:
            line=[word,pronunciation_num[0].upper(),pronunciation,pronunciation_num,[]]
        except:
            line=[word,'',pronunciation,pronunciation_num,[]]
        try:
            p_class=des[index].get('class')
        except:
            continue
        for p in des[index:]:
            if p.get('class')!=p_class:
                break
            if 'strong' in str(p):
                break
            line[-1].append(str(p).replace('\u3000',''))
        words.append(line)
    return {'baseinfor':baseinfor,'words':words,'url':wordurl}

def main():
    flag=True
    for line in open('words.txt','r'):
        item=eval(line)
        result=word_infor(item[-1])
        f=open('result.txt','a')
        f.write(str(result)+'\n')
        f.close()
        print(item)

main()
