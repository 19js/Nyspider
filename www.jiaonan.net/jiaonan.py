import requests
from bs4 import BeautifulSoup
import threading
import time
import random
import openpyxl

def get_headers():
    pc_headers = {
        "X-Forwarded-For":'%s.%s.%s.%s'%(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),        
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    }
    return pc_headers


class NetWorkError(Exception):
    pass


def load_res_text(url):
    for i in range(3):
        try:
            res_text=requests.get(url,headers=get_headers(),timeout=10).text
            return res_text
        except Exception as e:
            print(e)
            continue
    raise NetWorkError

def get_info(url):
    res_text=load_res_text(url)
    res_text=res_text.encode('iso-8859-1').decode('gbk')
    soup=BeautifulSoup(res_text,'lxml').find('div',id='xx_bcont')
    phone_tags=soup.find_all('span',{'class':'phone_pub'})
    result=[]
    for item in phone_tags:
        try:
            href=item.find('a').get('href')
            info=href.split('=')[-1]
        except:
            continue
        result.append(info)
    return result

def get_items(url):
    res_text=load_res_text(url)
    #res_text=res_text.encode('iso-8859-1').decode('gbk')
    soup=BeautifulSoup(res_text,'lxml').find('div',{'class':'list_left'}).find_all('div',{'id':'listB_cont'})
    result=[]
    for item in soup:
        try:
            a_item=item.find('a')
            title=a_item.get_text()
            url='http://www.jiaonan.net/'+a_item.get('href')
        except:
            continue
        result.append([title,url])
    return result

class PhoneInfo(threading.Thread):
    def __init__(self,item):
        super(PhoneInfo,self).__init__()
        self.item=item
        self.daemon=True

    def run(self):
        self.status=False
        try:
            result=get_info(self.item[-1])
            self.status=True
            self.item+=result
        except Exception as e:
            # import logging
            # logging.exception(e)
            pass

def crawl():
    #base_url='http://www.jiaonan.net/index.php?m=content&c=index&a=lists&catid=1&member_type=0&areaid=0&page={}'
    base_url='http://www.jiaonan.net/index.php?m=content&c=index&a=lists&catid=22&member_type=0&areaid=0&page={}'
    page=1
    counter=0
    while page<79:
        items=get_items(base_url.format(page))
        tasks=[]
        for item in items:
            task=PhoneInfo(item)
            tasks.append(task)
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        f=open('car_result.txt','a')
        failed_f=open('car_failed.txt','a')
        for task in tasks:
            if task.status:
                f.write(str(task.item)+'\n')
                counter+=1
            else:
                failed_f.write(str(task.item)+'\n')
        f.close()
        failed_f.close()
        print(page,counter,'OK')
        page+=1

def write_to_excel(txt_filename):
    excel=openpyxl.Workbook()
    sheet=excel.create_sheet()
    for line in load_txt(txt_filename):
        sheet.append(line)
    excel.save(txt_filename.replace('.txt','.xlsx'))

def load_txt(txt_filename):
    for line in open(txt_filename,'r'):
        try:
            line=eval(line)
        except:
            continue
        yield line

if __name__=='__main__':
    write_to_excel('./car_result.txt')