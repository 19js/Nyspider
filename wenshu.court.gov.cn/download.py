import requests
from bs4 import BeautifulSoup
import json

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

def doclist(page,Param="",Order="裁判日期"):
    data={
    'Param':Param,
    'Index':page,
    'Page':"20",
    'Order':Order,
    'Direction':"desc"
    }
    html=requests.post('http://wenshu.court.gov.cn/List/ListContent',data=data,headers=headers).text
    data=json.loads(html)
    data=eval(data)
    result=[]
    for item in data:
        if 'Count' in item:
            continue
        result.append(item)
    return result

def download(docid,title):
    data={
    'conditions':'',
    'docIds':docid+'|'+title+'|',
    'keyCode':""
    }
    content=requests.post('http://wenshu.court.gov.cn/CreateContentJS/CreateListDocZip.aspx?action=1',data=data,headers=headers).content
    with open('result/%s.doc'%docid,'wb') as f:
        f.write(content)

if __name__ == '__main__':
    docs=doclist(1)
    try:
        import os
        os.mkdir('result')
    except:
        pass
    for item in docs:
        download(item['文书ID'],item['案件名称'])
        print(item['案件名称'])
