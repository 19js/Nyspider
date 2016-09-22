import requests
from bs4 import BeautifulSoup
import time
import urllib

headers = {
        'Host':"vip.stock.finance.sina.com.cn",
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def get_managers(code):
    html=requests.get('http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpManager/stockid/%s.phtml'%code,headers=headers).text.encode('iso-8859-1').decode('gbk')
    table=BeautifulSoup(html,'lxml').find('div',id='con02-6').find_all('tr')
    result=[]
    for item in table:
        if '独立董事' not in str(item):
            continue
        tds=item.find_all('td')
        line=''
        for td in tds:
            line+=td.get_text()+'|'
        line+=item.find('a').get('href')
        line=line.replace('\r','').replace('\n','')
        result.append(line)
    return result

def manager_infor(code,url):
    word=url.split('=')[-1]
    key=word.encode('gbk')
    key=urllib.parse.quote(key)
    html=requests.get(url.replace(word,key),headers=headers).text.encode('iso-8859-1').decode('gbk')
    table=BeautifulSoup(html,'lxml').find('table',id='Table1').find('tbody').find_all('tr')
    line=''
    for item in table:
        for td in item.find_all('td'):
            line+='|'+td.get_text()
    line=line.replace('\r','').replace('\n','')
    return line


def manegers():
    for line in open('./codes.txt','r'):
        code=line.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
        try:
            result=get_managers(code)
        except:
            failed=('failed','a')
            failed.write(line)
            failed.close()
            continue
        f=open('manager.txt','a')
        for item in result:
            f.write(code+'|'+item+'\n')
        f.close()
        print(code,'ok')

def main():
    urls={}
    for line in open('./manager.txt','r',encoding='utf-8'):
        line=line.replace('\n','')
        url='http://vip.stock.finance.sina.com.cn/'+line.split('|')[-1]
        f=open('result.txt','a',encoding='utf-8')
        if url in urls:
            f.write(line+urls[url]+'\n')
            f.close()
            continue
        try:
            item=manager_infor(line.split('|')[0],url)
        except:
            failed=open('failed','a',encoding='utf-8')
            failed.write(line+'\n')
            failed.close()
            continue
        urls[url]=item
        f.write(line+item+'\n')
        f.close()
        print(url,'ok')
    f.close()
main()
