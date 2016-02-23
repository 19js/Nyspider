#coding:utf-8

import requests
from bs4 import BeautifulSoup
from ctypes import *
import xlwt3
import sys

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}


def login(username,passwd):
    session=requests.session()
    data={
    'username':username,
    'password':passwd
    }
    session.post('http://www.chuanlaoda.cn/good/login.html',headers=headers,data=data)
    return session

def get_urls(session,page):
    header = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With':"XMLHttpRequest",
            'Content-Type':"application/x-www-form-urlencoded; charset=UTF-8",
            'Host':"www.chuanlaoda.cn",
            'Referer':"http://www.chuanlaoda.cn/good/shiplist.html",
            'Connection': 'keep-alive'}
    data={
    'page':page,
    'srcname':"",
    'src':"",
    'destname':"",
    'dest':"",
    'min':"",
    'max':"",
    'atime':""
    }
    html=session.post('http://www.chuanlaoda.cn/good/shiplist.html',data=data,headers=header).text#.encode('ISO-8859-1').decode('utf-8','ignore')
    table=BeautifulSoup(html).find('div',attrs={'class':"listbox"}).find_all('dl')
    lists=[]
    for item in table[1:]:
        ship={}
        d3=item.find('dd',attrs={'class':'d3'})
        number=d3.get('n')
        ship['num']=number
        ship['title']=d3.find('span',attrs={'class':'info'}).get('title')
        ship['weight']=item.find('dd',attrs={'class':'d4'}).get_text()
        lists.append(ship)
    return lists

def infor(session,ship):
    num=ship['num']
    html=session.get('http://www.chuanlaoda.cn/good/ship/%s.html'%num,headers=headers).text
    soup=BeautifulSoup(html).find('div',attrs={'class':'shipinfo'})
    line=soup.find('div',attrs={'class':'linebox'}).find_all('div',attrs={'class':'line'})[1].find_all('div')
    ship['date']=line[0].get_text()
    ship['from']=line[1].get_text().replace('\n','').replace('\t','')
    ship['to']=line[-1].get_text()
    try:
        img_url=soup.find('dd',attrs={'class':'uinfo'}).find('div',id='umobile').find('img').get('src')
    except:
        img_url='http://www.chuanlaoda.cn/mobile/%s.png'%num
    try:
        img=session.get(img_url,headers=headers,timeout=40).content
    except:
        img=False
    ship['img']=img
    return ship

def img_ocr(imgname):
    ocrpasswd = "868197D30CC624FD3C2E2EE66494DA5F"
    #VcodeInit 初始换引擎函数 只有一个参数 为引擎初始化密码 失败返回-1 此函数只需调用一次 切勿多次调用 。
    dll = windll.LoadLibrary('CaptchaOCR.dll')
    load_ocr = dll.VcodeInit
    load_ocr.argtypes = [c_char_p]
    load_ocr.restypes = c_int
    index = load_ocr(ocrpasswd.encode('utf-8'))
    img_string = open(imgname, "rb").read()
    img_buffer = create_string_buffer(img_string)
    #申请接收识别结果的缓冲区  一定要申请
    ret_buffer = create_string_buffer(15)
    #调用此函数之前，如果已经初始化成功过识别引擎函数 那么无需再调用初始化函数
    #GetVcode 识别函数 参数1为 VcodeInit 返回值 index 参数2为图片数据 参数3为图片大小 参数4为接收识别结果 需要给变量申请内存 如 ret_buffer = create_string_buffer(10)
    get_code_from_buffer = dll.GetVcode
    get_code_from_buffer(index, byref(img_buffer), len(img_buffer), byref(ret_buffer))
    return ret_buffer.value.decode('utf-8')

def main(username,passwd,page):
    excel=xlwt3.Workbook()
    count=0
    sheet=excel.add_sheet('sheet')
    session=login(username,passwd)
    for pagenum in range(int(page)):
        ships=get_urls(session, pagenum+1)
        for ship in ships:
            try:
                ship=infor(session, ship)
            except:
                continue
            if ship['img']==False:
                ship['phone']=''
                continue
            with open('temp.png','wb') as img:
                img.write(ship['img'])
            phonenum=img_ocr('temp.png')
            ship['phone']=phonenum
        for ship in ships:
            try:
                sheet.write(count,0,ship['title'])
                sheet.write(count,1,ship['weight'])
                sheet.write(count,2,ship['date'])
                sheet.write(count,3,ship['from'])
                sheet.write(count,4,ship['to'])
                sheet.write(count,5,ship['phone'])
                count+=1
            except:
                continue
        print(pagenum+1,'---ok')
        excel.save('data.xls')

if __name__=='__main__':
    username='13291481459'
    passwd='111111'
    page=2
    if len(sys.argv) == 4:
        username=sys.argv[1]
        passwd=sys.argv[2]
        page=sys.argv[3]
    main(username,passwd,page)
