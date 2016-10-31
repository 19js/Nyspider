import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import chardet


headers = {
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}

def get_chardet(filename):
    data=open(filename,'rb').read()
    coding=chardet.detect(data)['encoding']
    if coding=='GB2312':
        coding='GBK'
    return coding

def load_keywords():
    encoding=get_chardet('data/negative_keywords.txt')
    negative_keywords=[]
    for line in open('data/negative_keywords.txt','r',encoding=encoding):
        line=line.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
        if line=='':
            continue
        negative_keywords.append(line)
    encoding=get_chardet('data/positive_keywords.txt')
    positive_keywords=[]
    for line in open('data/positive_keywords.txt','r',encoding=encoding):
        line=line.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
        if line=='':
            continue
        positive_keywords.append(line)
    return positive_keywords,negative_keywords

def get_titles(url,num):
    page=1
    count=0
    titles=[]
    while page<=num:
        try:
            html=requests.get(url.replace('.html','_%s.html'%page),headers=headers,timeout=30).text
        except:
            count+=1
            if count==5:
                break
            continue
        try:
            table=BeautifulSoup(html,'lxml').find('div',id='articlelistnew').find_all('div',{'class':'articleh'})
        except:
            break
        for item in table:
            try:
                span=item.find('span',{'class':'l3'})
                if 'em class' in str(span):
                    continue
                title=span.find('a').get('title')
                titles.append(title)
            except:
                continue
        page+=1
    return titles

def load_urls():
    urls=[line.replace('\r','').replace('\n','').split('|') for line in open('data/urls.txt','r',encoding='utf-8')]
    return urls

def write_wo_excel(result,filetype):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for item in result:
        try:
            sheet.append(item)
        except:
            continue
    date=time.strftime('%Y-%m-%d',time.localtime())
    try:
        os.mkdir('result')
    except:
        pass
    excel.save('result/%s_%s.xlsx'%(date,filetype))

def counter(positive_keywords,negative_keywords,name,titles):
    positive=0
    negative=0
    for title in titles:
        up=0
        down=0
        for keyword in positive_keywords:
            if keyword in title:
                up+=1
        for keyword in negative_keywords:
            if keyword in title:
                down+=1
        if up>down:
            positive+=1
        elif down>up:
            negative+=1
    return [name,positive,negative]

def main():
    try:
        positive_keywords,negative_keywords=load_keywords()
    except:
        print("加载关键词失败")
        return
    try:
        urls=load_urls()
    except:
        print('加载股票链接失败')
        return
    try:
        page=int(input("输入抓取页数："))
    except:
        page=2
    result_1=[]
    for item in urls:
        try:
            name=item[0]
            url=item[1]
        except:
            continue
        titles=get_titles(url,page)
        line=counter(positive_keywords,negative_keywords,name,titles)
        result_1.append(line)
        try:
            print(name,'1 ok')
        except:
            pass
    write_wo_excel(result_1,'评论时间')
    result_2=[]
    for item in urls:
        try:
            name=item[0]
            url=item[1]
        except:
            continue
        titles=get_titles(url.replace('.html',',f.html'),page)
        line=counter(positive_keywords,negative_keywords,name,titles)
        result_2.append(line)
        try:
            print(name,'2 ok')
        except:
            pass
    write_wo_excel(result_2,'发表时间')
    print("完成")

main()
time.sleep(360)
