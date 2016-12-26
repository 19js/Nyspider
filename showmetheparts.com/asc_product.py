import requests
from bs4 import BeautifulSoup
import time

headers = {
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}

def search(keyword):
    url='https://www.showmethepartsdb.com/bin/ShowMeConnectdll.dll?lookup=complist&compno=%s&id=ASC2182&storeid=&userid=&_dc=1475926588068&page=1&start=0&limit=25&callback='
    html=requests.get(url%keyword,headers=headers).text
    table=BeautifulSoup(html,'lxml').find_all('interchangedata')
    result=[]
    for item in table:
        try:
            Manufacturer=item.find('mfg').get_text()
            Mfg_Part_Number=item.find('comp_no').get_text()
            part_type=item.find('part_type').get_text()
            part_no=item.find('part_no').get_text()
            result.append([Manufacturer,Mfg_Part_Number,part_type,part_no])
        except:
            continue
    return result

def main():
    for key in open('words.txt','r'):
        key=key.replace('\n','').replace(' ','')
        items=search(key)
        try:
            items=search(items[0][-1])
        except:
            failed=open('failed.txt','a')
            failed.write(key+'\n')
            failed.close()
            continue
        f=open('result.txt','a')
        for item in items:
            line=key
            for i in item:
                line+='| '+i
            f.write(line+'\n')
        f.close()
        print(key)
        time.sleep(0.5)

main()
