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


def get_data(url,session):
    html=session.get(url,headers=headers).text.encode('ISO-8859-1').decode('gbk','ignore')
    soup=BeautifulSoup(html,'html.parser')
    table=soup.find('table',{'align':'center','width':'98%'}).find_all('tr')
    title=soup.find('td',{'height':'22'}).get_text()
    result=[title]
    for item in table:
        result.append(item.find_all('td')[-1].get_text().replace('\r','').replace('\n','').replace('\t',''))
    return result

def get_AQI(url,session):
    html=session.get(url,headers=headers).text.encode('ISO-8859-1').decode('gbk','ignore')
    aqi=BeautifulSoup(html,'html.parser').find('td',{'align':'center'}).find('table',{'width':'60'}).find('td').get_text()
    return aqi

def main(date):
    urls=['http://www.tyshbj.com.cn/hbj/shishi/chengqushuju.asp?dwcode=1&dwname=%C9%CF%C0%BC&xiabiao=1',
    'http://www.tyshbj.com.cn/hbj/shishi/chengqushuju.asp?dwcode=54&dwname=%BD%F0%CA%A4&xiabiao=4',
    'http://www.tyshbj.com.cn/hbj/shishi/chengqushuju.asp?dwcode=56&dwname=%C4%CF%D5%AF&xiabiao=5',
    'http://www.tyshbj.com.cn/hbj/shishi/chengqushuju.asp?dwcode=53&dwname=%BC%E2%B2%DD%C6%BA&xiabiao=3',
    'http://www.tyshbj.com.cn/hbj/shishi/chengqushuju.asp?dwcode=57&dwname=%CC%D2%D4%B0&xiabiao=6',
    'http://www.tyshbj.com.cn/hbj/shishi/chengqushuju.asp?dwcode=62&dwname=%D0%A1%B5%EA&xiabiao=8',
    'http://www.tyshbj.com.cn/hbj/shishi/chengqushuju.asp?dwcode=59&dwname=%CE%EB%B3%C7&xiabiao=7',
    'http://www.tyshbj.com.cn/hbj/shishi/chengqushuju.asp?dwcode=63&dwname=%BD%FA%D4%B4&xiabiao=9']
    aqi_url='http://www.tyshbj.com.cn/hbj/shishi/chengqulist.asp'
    keys=['时间','检测点','SO2最近1小时均值：', 'NO2最近1小时均值：', 'PM10最近1小时均值：', 'PM10最近24小时均值：','CO最近1小时均值：', 'O3最近1小时均值：', 'O3最近8小时均值：', 'PM2.5最近1小时均值：', 'PM2.5最近24小时均值：']
    try:
        session=requests.session()
        session.get('http://www.tyshbj.com.cn/hbj/shishi/',headers=headers)
        lines=[]
        for url in urls:
            result=get_data(url,session)
            lines.append(date+'\t'+'\t'.join(result)+'\r\n')
        aqi=get_AQI(aqi_url,session)
        lines.append(date+'\tAQI\t'+aqi+'\r\n\r\n')
    except:
        return False
    f=open('result.txt','a',encoding='utf-8')
    for line in lines:
        f.write(line)
    f.close()
    try:
        write_to_excel()
    except:
        return False
    return True

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in open('result.txt','r',encoding='utf-8'):
        line=line.replace('\r\n','')
        sheet.append(line.split('\t'))
    excel.save('result.xlsx')


while True:
    timenow=time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
    if ':30:' in timenow:
        while True:
            status=main(timenow)
            if(status):
                break
        print(timenow,'ok')
        time.sleep(2500)
    time.sleep(15)
