import requests
from bs4 import BeautifulSoup
import json
import os
import time
import threading
import re

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def search(code):
    result=[]
    for s_type in ['']:
        data={
        'stockcode':code,
        'type':s_type
        }
        html=requests.post('http://ircs.p5w.net/ircs/rsc/queryBroadcastList.do',data=data,headers=headers,timeout=30).text
        try:
            soup=BeautifulSoup(html,'html.parser').find('div',{'class':'new_box'}).find_all('p',{'class':'xwt_wz2'})
        except:
            continue
        for item in soup:
            try:
                title=item.find('a').get('title')
            except:
                continue
            url=item.find('a').get('href')
            if '说明会' in title:
                try:
                    year=re.findall('(\d+)年',title)[0]
                except:
                    year='0000'
                try:
                    date=re.findall('(\d+-\d+-\d+)',item.get_text())[0]
                except:
                    date='-'
                result.append([0,code,title,url,year,date])
                continue
            elif '网上路演' in title and '新股' in title and '视频' not in title:
                result.append([1,code,title,url])
    return result

def topic_interaction(item):
    rid=re.findall('rid=(\d+)',item[3])[0]
    page=1
    filename=item[1]+'_'+item[4]+'.txt'
    pre_table=''
    try_count=0
    while True:
        data={
        'pageNo':page,
        'rid':rid
        }
        try:
            html=requests.post('http://ircs.p5w.net/ircs/topicInteraction/questionPage.do',data=data,headers=headers,timeout=30).text
            try_count=0
        except:
            try:
                print(item[2],page,'failed')
            except:
                pass
            try_count+=1
            if try_count==5:
                break
            continue
        try:
            value=json.loads(html)['value']
            table=json.loads(value)['q_all']
        except:
            break
        if len(table)==0:
            break
        if table==pre_table:
            break
        pre_table=table
        f=open('说明会/%s'%filename,'a',encoding='utf-8')
        for ques in table:
            try:
                reply=ques['reply'][0]
            except:
                continue
            q_content=ques['q_content'].replace('\r','').replace('\n','')
            r_content=reply['r_content'].replace('\r','').replace('\n','')
            r_officename=reply['r_officename'].split(':')[0]
            f.write('***%s\r\n$$$%s:%s\r\n'%(q_content,r_officename,r_content))
        f.close()
        try:
            print(item[2],page,'ok')
        except:
            pass
        page+=1
    f=open('说明会.txt','a',encoding='utf-8')
    f.write('%s_%s|%s\r\n'%(item[1],item[4],item[-1]))
    f.close()

def topic_by_boardid(item):
    boardid=re.findall('boardid=(\d+)',item[3])[0]
    page=1
    filename=item[1]+'_'+item[4]+'.txt'
    pre_table=[]
    try_count=0
    while True:
        url='http://newzspt.p5w.net/bbs/question_page.asp?boardid=%s&bbs=1&pageNo=%s'%(boardid,page)
        try:
            html=requests.get(url,headers=headers,timeout=20).text.encode('iso-8859-1').decode('gbk','ignore')
            try_count=0
        except:
            try:
                print(item[2],page,'failed')
            except:
                pass
            try_count+=1
            if try_count==5:
                break
            continue
        table=BeautifulSoup(html,'html.parser').find_all('q_and_r')
        if len(table)==0:
            break
        if table==pre_table:
            break
        pre_table=table
        f=open('说明会/%s'%filename,'a',encoding='utf-8')
        for ques in table:
            reply=ques.find('replay')
            if reply is None:
                continue
            ques=ques.find('question')
            q_name=ques.find('q_name').get_text()
            if '主持人' in q_name:
                continue
            q_content=ques.find('q_content').get_text().replace('\r','').replace('\n','')
            r_content=reply.find('r_content').get_text()
            r_officename=reply.find('r_officename').get_text().split(':')[0]
            f.write('***%s\r\n$$$%s:%s\r\n'%(q_content,r_officename,r_content))
        f.close()
        try:
            print(item[2],page,'ok')
        except:
            pass
        page+=1
    f=open('说明会.txt','a',encoding='utf-8')
    f.write('%s_%s|%s\r\n'%(item[1],item[4],item[-1]))
    f.close()

def topic_by_selcode(item):
    try:
        selcode=re.findall('selcode=(\d+)',item[3])[0]
    except:
        html=requests.get(item[3],headers=headers,timeout=20).text
        selcode=re.findall('boardid=(\d+)"',html)[0]
    page=1
    filename=item[1]+'_'+item[4]+'.txt'
    pre_table=[]
    try_count=0
    while True:
        url='http://zsptbs.p5w.net/bbs/chatbbs/left.asp?boardid=%s&pageNo=%s'%(selcode,page)
        try:
            html=requests.get(url,headers=headers,timeout=20).text.encode('iso-8859-1').decode('gbk','ignore')
            try_count=0
        except:
            try:
                print(item[2],page,'failed')
            except:
                pass
            try_count+=1
            if try_count==5:
                break
            continue
        table=BeautifulSoup(html,'html.parser').find_all('tr')
        if len(table)==0:
            break
        lines=[]
        for tr in table:
            tds=tr.find_all('td')
            if len(tds)!=4:
                continue
            if 'images_bbs/hold.gif' in str(tr) or '发言人' in str(tr):
                continue
            q_name=tds[2].get_text().replace('\r','').replace('\n','').replace(' ','')
            if '主持人' in q_name:
                continue
            content=tds[-1].get_text().replace('\r','').replace('\n','')
            r_name=tds[0].get_text().replace('\r','').replace('\n','').replace(' ','').replace('\t','').replace('\xa0','')
            if r_name=='':
                lines.append('$$$%s:%s\r\n'%(q_name,content))
            else:
                lines.append('***%s\r\n'%(content))
        if pre_table==lines:
            break
        pre_table=lines
        f=open('说明会/%s'%filename,'a',encoding='utf-8')
        for line in lines:
            f.write(line)
        f.close()
        try:
            print(item[2],page,'ok')
        except:
            pass
        page+=1
    f=open('说明会.txt','a',encoding='utf-8')
    f.write('%s_%s|%s\r\n'%(item[1],item[4],item[-1]))
    f.close()


def roadshow_question_page(item):
    page=1
    pre_table=[]
    if '.' in item[-1].split('/')[-1]:
        baseurl=item[-1].replace(item[-1].split('/')[-1],'')
    else:
        baseurl=item[-1]
    try_count=0
    while True:
        url=baseurl+'/bbs/question_page.asp?pageNo='+str(page)
        try:
            html=requests.get(url,headers=headers,timeout=20).text.encode('iso-8859-1').decode('gbk','ignore')
            try_count=0
        except:
            try:
                print(item[2],page,'failed')
            except:
                pass
            try_count+=1
            if try_count==5:
                break
            continue
        table=BeautifulSoup(html,'html.parser').find_all('q_and_r')
        if len(table)==0:
            break
        if table==pre_table:
            break
        pre_table=table
        f=open('路演/%s.txt'%item[1],'a',encoding='utf-8')
        for ques in table:
            ques=ques.find('question')
            q_name=ques.find('q_ofname').get_text()
            if '主持人' in q_name:
                continue
            reply=ques.find('replay')
            if reply is None:
                if page!=1:
                    try:
                        content=ques.find('q_content').get_text().replace('\r','').replace('\n','')
                        f.write('@@@%s:%s\r\n'%(q_name.split(':')[0],content))
                    except:
                        pass
                continue
            q_content=ques.find('q_content').get_text().replace('\r','').replace('\n','')
            r_content=reply.find('r_content').get_text()
            r_officename=reply.find('r_officename').get_text().split(':')[0]
            f.write('***%s\r\n$$$%s:%s\r\n'%(q_content,r_officename,r_content))
        f.close()
        try:
            print(item[2],page,'ok')
        except:
            pass
        page+=1

def roadshow_rs(item):
    page=1
    pre_table=[]
    if '.' in item[-1].split('/')[-1]:
        baseurl=item[-1].replace(item[-1].split('/')[-1],'')
    else:
        baseurl=item[-1]
    try_count=0
    while True:
        url=baseurl+'/left.asp?pageNo='+str(page)
        try:
            html=requests.get(url,headers=headers,timeout=20).text.encode('iso-8859-1').decode('gbk','ignore')
            try_count=0
        except:
            try:
                print(item[2],page,'failed')
            except:
                pass
            try_count+=1
            if try_count==5:
                break
            continue
        table=BeautifulSoup(html,'html.parser').find_all('tr')
        if len(table)==0:
            break
        if table==pre_table:
            break
        pre_table=table
        f=open('路演/%s.txt'%item[1],'a',encoding='utf-8')
        for tr in table:
            tds=tr.find_all('td')
            if len(tds)!=4:
                continue
            if '发言人' in str(tr):
                continue
            q_name=tds[2].get_text().replace('\r','').replace('\n','').replace(' ','')
            if '主持人' in q_name:
                continue
            if 'images_bbs/hold.gif' in str(tr):
                if page!=1:
                    content=tds[-1].get_text().replace('\r','').replace('\n','')
                    f.write('@@@%s:%s\r\n'%(q_name,content))
                    continue
            content=tds[-1].get_text().replace('\r','').replace('\n','')
            r_name=tds[0].get_text().replace('\r','').replace('\n','').replace(' ','').replace('\t','').replace('\xa0','')
            if r_name=='':
                f.write('$$$%s:%s\r\n'%(q_name,content))
            else:
                f.write('***%s\r\n'%(content))
        f.close()
        try:
            print(item[2],page,'ok')
        except:
            pass
        page+=1

def roadshow_by_rid(item):
    try:
        rid=re.findall('rid=(\d+)',item[3])[0]
    except:
        html=requests.get(item[-1],headers=headers,timeout=20).text
        rid=re.findall('topicInteraction.*?rid=(\d+)',html)[0]
    page=1
    pre_table=''
    try_count=0
    while True:
        data={
        'pageNo':page,
        'rid':rid
        }
        try:
            html=requests.post('http://ircs.p5w.net/ircs/topicInteraction/questionPage.do',data=data,headers=headers,timeout=30).text
            try_count=0
        except:
            try:
                print(item[2],page,'failed')
            except:
                pass
            try_count+=1
            if try_count==5:
                break
            continue
        try:
            value=json.loads(html)['value']
            table=json.loads(value)['q_all']
        except:
            break
        if len(table)==0:
            break
        if table==pre_table:
            break
        pre_table=table
        f=open('路演/%s'%item[1],'a',encoding='utf-8')
        for ques in table:
            try:
                reply=ques['reply'][0]
            except:
                try:
                    if page!=1:
                        q_name=ques['q_name']
                        if '主持人' not in q_name:
                            q_content=ques['q_content'].replace('\r','').replace('\n','')
                            q_name=ques['q_name'].split(':')[0]
                            f.write('@@@%s:%s\r\n'%(q_name,q_content))
                except:
                    pass
                continue
            q_content=ques['q_content'].replace('\r','').replace('\n','')
            r_content=reply['r_content'].replace('\r','').replace('\n','')
            r_officename=reply['r_officename'].split(':')[0]
            f.write('***%s\r\n$$$%s:%s\r\n'%(q_content,r_officename,r_content))
        f.close()
        try:
            print(item[2],page,'ok')
        except:
            pass
        page+=1

def crawl(item):
    if item[0]==0:
        if 'topicInteraction' in item[3]:
            try:
                topic_interaction(item)
            except:
                f=open('0_failed.txt','a',encoding='utf-8')
                f.write(str(item)+'\n')
                f.close()
        elif 'newzspt.p5w.net/bbs/bbs.asp?boardid' in item[3]:
            try:
                topic_by_boardid(item)
            except:
                f=open('0_failed.txt','a',encoding='utf-8')
                f.write(str(item)+'\n')
                f.close()
        elif 'zsptbs.p5w.net/bbs/chatbbs' in item[3]:
            try:
                topic_by_selcode(item)
            except:
                f=open('0_failed.txt','a',encoding='utf-8')
                f.write(str(item)+'\n')
                f.close()
        else:
            f=open('0_failed.txt','a',encoding='utf-8')
            f.write(str(item)+'\n')
            f.close()
    else:
        if 'roadshow2008' in item[-1]:
            try:
                roadshow_question_page(item)
            except:
                f=open('roadshow_failed.txt','a',encoding='utf-8')
                f.write(str(item)+'\n')
                f.close()
        elif '/rs20' in item[-1] or '/bbs/' in item[-1]:
            try:
                roadshow_rs(item)
            except:
                f=open('roadshow_failed.txt','a',encoding='utf-8')
                f.write(str(item)+'\n')
                f.close()
        elif 'video' in item[-1]:
            return
        elif 'irm.p5w.net' in item[-1]:
            try:
                roadshow_by_rid(item)
            except:
                f=open('roadshow_failed.txt','a',encoding='utf-8')
                f.write(str(item)+'\n')
                f.close()
        else:
            f=open('roadshow_failed.txt','a',encoding='utf-8')
            f.write(str(item)+'\n')
            f.close()


if __name__=='__main__':
    try:
        os.mkdir('说明会')
    except:
        pass
    try:
        os.mkdir('路演')
    except:
        pass
    for filename in os.listdir(path='code'):
        if '.txt' not in filename:
            continue
        for line in open('code/%s'%filename,'r',encoding='utf-8'):
            code=line.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
            try:
                result=search(code)
            except:
                f=open('failed_%s'%filename,'a',encoding='utf-8')
                f.write(line)
                f.close()
                continue
            for item in result:
                #crawl(item)
                work=threading.Thread(target=crawl,args=(item,))
                work.setDaemon(True)
                work.start()
                time.sleep(2)
