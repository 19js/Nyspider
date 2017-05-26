import requests
import openpyxl
from bs4 import BeautifulSoup
import time

def get_claim_files(page):
    data={
        "cmd":"claim_index",
        "curpage":page,
        "stock_way":0,
        "pagelines":20
    }
    html=requests.post('http://www.xmzfcg.gov.cn/claim/claimAction.do',data=data,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('table',{'width':'95%'}).find_all('tr')
    result=[]
    for item in table:
        try:
            if 'claimAction.do?cmd=claim_view' not in str(item):
                continue
            tds=item.find_all('td')
            company=tds[1].get_text()
            url='http://www.xmzfcg.gov.cn/claim/'+item.find('a').get('href').replace("javascript:ShowView('",'').replace("')",'')
            name=tds[3].get_text().replace('\r','').replace('\n','').replace(' ','')
            result.append([company,name,url])
        except Exception as e:
            print(e)
            pass
    return result

def get_claim_info(url):
    html=requests.get(url,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('table',{'width':'90%'}).find_all('tr')
    result=[]
    for item in table:
        try:
            key=item.find('td',{'align':'right'}).get_text()
            if '来源:' in key or '采购方式:' in key:
                value=item.find_all('td')[1].get_text().replace('\r','').replace('\n','').replace(' ','')
            else:
                value=item.find('td',{'align':'left'}).get_text().replace('\r','').replace('\n','').replace(' ','')
        except:
            continue
        result.append(value)
    return result

def write_to_excel(result):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in result:
        try:
            sheet.append(line)
        except:
            print(line)
            pass
    excel.save('result.xlsx')

def crawl():
    try:
        max_page=int(input("需要采集的页数:"))
    except:
        max_page=5
    page=1
    result=[]
    while page<=max_page:
        try:
            items=get_claim_files(page)
        except Exception as e:
            print('[Error]',e,page)
            continue
        index=0
        while index<len(items):
            try:
                line=get_claim_info(items[index][-1])
            except Exception as e:
                print('[Error]',e)
                continue
            result.append(items[index]+line)
            index+=1
        print('Page ',page,'OK')
        page+=1
    write_to_excel(result)
    print('采集完成')

crawl()
time.sleep(50)
