import requests
from bs4 import BeautifulSoup
import time
import openpyxl

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}

def get_company_urls(province,cate):
    base_url='http://m.51sole.com/company/bm/p{}/?cate={}&province={}'
    page=1
    result=[]
    pre=[]
    while True:
        try:
            html=requests.get(base_url.format(page,cate,province),headers=headers,timeout=30).text
            table=BeautifulSoup(html,'lxml').find('div',{'class':'companybox'}).find_all('li')
        except Exception as e:
            print(province,page,e)
            continue
        if table==pre:
            break
        pre=table
        for item in table:
            title=item.find('a').get_text()
            url=item.find('a').get('href')
            result.append([title,url])
        print(province,cate,page,'OK')
        page+=1
    return result

def search(keyword):
    base_url='http://m.51sole.com/s/p{}/?q={}'
    page=1
    result=[]
    pre=[]
    while True:
        try:
            html=requests.get(base_url.format(page,keyword),headers=headers,timeout=30).text
            table=BeautifulSoup(html,'lxml').find_all('div',{'class':'intro'})
        except Exception as e:
            print(page,e)
            continue
        if table==pre:
            break
        pre=table
        f=open('urls.txt','a')
        for item in table:
            try:
                title=item.find('dd').find('a').get_text()
                url=item.find('dd').find('a').get('href')
            except Exception as e:
                print(e)
                continue
            f.write(str(['','',title,url])+'\n')
            #result.append([title,url])
        f.close()
        print(keyword,page,'OK')
        page+=1
    return result


def get_company_info(url):
    html=requests.get(url,headers=headers,timeout=30).text
    soup=BeautifulSoup(html,'lxml').find_all('div',{'class':'callus'})
    item=soup[0]
    table=[]
    info=['']*3
    for item in soup:
        table+=item.find_all('li')
    for item in table:
        if '联系人：' in str(item):
            text=item.get_text().replace('联系人：','')
            info[0]=text
        if '手机：' in str(item):
            text=item.get_text().replace('手机：','')
            info[1]=text
        if '电话：' in str(item):
            text=item.get_text().replace('电话：','')
            info[2]=text
    return info

def get_provinces():
    html=requests.get('http://m.51sole.com/company/bm/p2/?cate=qiangdimiantuliao',headers=headers).text
    table=BeautifulSoup(html,'lxml').find('ul',{'class':'common-city bg-white'}).find_all('li')
    f=open('province.txt','a')
    for item in table:
        province_id=item.get('o-id')
        province_name=item.find('a').get_text()
        f.write(str([province_name,province_id])+'\n')
    f.close()

def parser():
    lines=[]
    for line in open('urls.txt','r'):
        if line not in lines:
            lines.append(line)
    f=open('urls.txt','w')
    for line in lines:
        f.write(line)
    f.close()

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in open('./contact.txt','r'):
        line=eval(line)
        sheet.append(line)
    excel.save('result.xlsx')


if __name__=='__main__':
    '''
    search("涂料")
    cates=['jianzhuzhuangxiushigong','tuliaozhuji']
    for line in open('./province.txt','r'):
        line=eval(line)
        for cate in cates:
            f=open('urls.txt','a')
            result=get_company_urls(line[1], cate)
            for item in result:
                f.write(str(['','']+item)+'\n')
            f.close()
    parser()
    for line in open('./urls.txt','r'):
        try:
            line=eval(line)
        except:
            continue
        try:
            info=get_company_info('http://m.51sole.com/'+line[-1])
        except Exception as e:
            print(line,e)
            failed=open('failed.txt','a')
            failed.write(str(line)+'\n')
            failed.close()
            time.sleep(2)
            continue
        f=open('contact.txt','a')
        f.write(str(line+info)+'\n')
        f.close()
        print(line,'OK')
    '''
    write_to_excel()
