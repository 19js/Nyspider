#coding:utf-8

import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate'}


def getdata(target,viewid):
    html=requests.get('https://www.tripadvisor.com/ExpandedUserReviews-g294212-d325811?target=%s&context=1&reviews=%s&servlet=Attraction_Review&expand=1'%(target,viewid),headers=headers).text
    table=BeautifulSoup(html,'lxml').find_all('div',attrs={'class':'innerBubble'})
    result=[]
    for item in table:
        text=item.find('div',attrs={'class':'entry'}).get_text().replace('\r','').replace('\n','')+'||'
        try:
            text+=item.find('div',attrs={'class':'recommend'}).get_text().replace('\r','').replace('\n','')
        except:
            text+='--'
        result.append(text)
    return result

def main():
    f=open('result.txt','a')
    viewids=[]
    lines=[]
    count=0
    for line in open('data.txt','r'):
        line=line.replace('\n','')
        lines.append(line)
        viewid=line.split('||')[1].split('-')[-1].replace('SRC_','')
        viewids.append(viewid)
        if(len(viewids)<20):
            continue
        text=''
        for id in viewids:
            text+=id+','
        result=getdata(viewids[0],text[:-1])
        print(len(result))
        for num in range(len(lines)):
            f.write(lines[num]+'||'+result[num]+'\n')
        viewids.clear()
        lines.clear()
        count+=1
        print(count,'--ok')
    text=''
    for id in viewids:
        text+=id+','
    result=getdata(viewids[0],text[:-1])
    for num in range(lines):
        f.write(lines[num]+'||'+result[num]+'\n')
    viewids.clear()
    lines.clear()
    f.close()

main()
