from bs4 import BeautifulSoup
import os

def parser():
    files=[]
    for filename in os.listdir('html'):
        files.append(filename)
    files.sort(key=lambda x:int(x.replace('.html','')))
    f=open('result.txt','a')
    for filename in files:
        html=open('html/'+filename,'r').read()
        try:
            table=BeautifulSoup(html,'lxml').find('div',{'class':'rprt_all'}).find_all('div',{'class':"rprt abstract"})
        except:
            continue
        for item in table:
            cit=item.find('div',{'class':'cit'})
            try:
                periodical=cit.find('a').get_text()
            except:
                periodical='-'
            try:
                date=cit.get_text().replace(periodical,'')
            except:
                date='-'
            try:
                title=item.find('h1').get_text()
            except:
                continue
            try:
                auths=item.find('div',{'class':'auths'}).find_all('a')
            except:
                auths=[]
            auth_num=len(auths)
            auth_name=''
            for a in auths:
                auth_name+=a.get_text()+';'
            try:
                afflist=item.find('div',{'class':'afflist'}).find_all('li')
            except:
                afflist=''
            auth_infor=''
            for li in afflist:
                auth_infor+=li.get_text()+'||'
            try:
                abstract=item.find('div',{'class':'abstr'}).get_text()
            except:
                abstract=''
            try:
                pmid=item.find('div',{'class':'aux'}).find('a',{'ref':'aid_type=pmid'}).get_text()
            except:
                pmid='-'
            f.write(str([pmid,periodical,date,title,auth_num,auth_name,auth_infor,abstract])+'\r\n')
        print(filename,'-ok')
    f.close()
parser()
