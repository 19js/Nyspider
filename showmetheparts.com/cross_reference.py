import requests
from bs4 import BeautifulSoup

headers = {
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        'Referer':'http://catalog.showmetheparts.com/',
        "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}


def search(compno):
    url='https://www.showmethepartsdb.com/bin/ShowMeConnectdll.dll?lookup=complist&compno={}&id=SMTP2182&page=1&start=0&limit=25'.format(compno)
    html=requests.get(url, headers=headers).text
    table=BeautifulSoup(html,'lxml').find_all('interchangedata')
    result=[]
    for item in table:
        try:
            mfg=item.find('mfg').get_text()
            part_no=item.find("part_no").get_text()
            supplier=item.find('supplier').get_text()
            part_type=item.find('part_type').get_text()
            comp_no=item.find('comp_no').get_text()
            result.append([supplier,mfg,comp_no,part_type,part_no])
        except:
            continue
    return result

def main():
    start=1
    while True:
        try:
            result=search('AW%s'%start)
        except:
            continue
        f=open('result.txt','a')
        for item in result:
            f.write('%s||%s||%s||%s||%s\n'%tuple(item))
        f.close()
        print(start)
        start+=1
        if start==9501:
            break

main()
