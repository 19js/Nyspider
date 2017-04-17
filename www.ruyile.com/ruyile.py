import requests
from bs4 import BeautifulSoup
import time

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_school_urls(school_type,filename):
    page=1
    pre_schools=[]
    while True:
        try:
            html=requests.get('http://www.ruyile.com/xuexiao/?t={}&p={}'.format(school_type,page),headers=headers,timeout=30).text
            schools=BeautifulSoup(html,'lxml').find('div',{'class':'main'}).find_all('div',{'class':'sk'})
        except Exception as e:
            print(school_type,page,e)
            continue
        if pre_schools==schools:
            break
        pre_schools=schools
        f=open(filename,'a')
        for item in schools:
            try:
                title=item.find('h4').get_text().replace('\r','').replace('\n','')
                url='http://www.ruyile.com/'+item.find('a').get('href')
            except:
                continue
            f.write(str([title,url])+'\n')
        f.close()
        print(school_type,page,'OK')
        page+=1

def get_school_info(school):
    html=requests.get(school[-1],headers=headers,timeout=30).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'main'}).find('div',{'class':'xxsx'}).find_all('div')
    result=['']*8
    for item in soup:
        if '所属地区' in item.get_text():
            areas=item.find_all('a')
            try:
                result[0]=areas[0].get_text().replace('\r','').replace('\n','').replace(' ','')
            except:
                result[0]='-'
            if result[0] in '北京 上海 天津 重庆 北京市 上海市 天津市 重庆市':
                result[1]=result[0]
                try:
                    result[2]=areas[1].get_text().replace('\r','').replace('\n','').replace(' ','')
                except:
                    result[2]='-'
            else:
                try:
                    result[1]=areas[1].get_text().replace('\r','').replace('\n','').replace(' ','')
                except:
                    result[1]='-'
                try:
                    result[2]=areas[2].get_text().replace('\r','').replace('\n','').replace(' ','')
                except:
                    result[2]='-'
        if '学校地址' in item.get_text():
            result[-1]=item.get_text().replace('学校地址','').replace('\r','').replace('\n','').replace('：','')
        if '招生电话' in item.get_text():
            result[-2]=item.get_text().replace('招生电话','').replace('\r','').replace('\n','').replace('：','')
    result[3]=school[0]
    result[4]=school[0]
    for key in result[:3]:
        result[4]=result[4].replace(key,'')
    result.append(school[-1])
    return result

if __name__=='__main__':
    get_school_urls(2,'小学.txt')
    get_school_urls(3,'中学.txt')
    for filename in ['小学.txt','中学.txt']:
        for line in open(filename,'r'):
            school=eval(line)
            try:
                info=get_school_info(school)
            except Exception as e:
                failed=open(filename.replace('.txt','_failed.txt'),'a')
                failed.write(line)
                failed.close()
                print(school,e)
                continue
            info[5]=filename.replace('.txt','')
            f=open(filename.replace('.txt','_result.txt'),'a')
            f.write(str(info)+'\n')
            f.close()
            print(filename,school,'OK')
