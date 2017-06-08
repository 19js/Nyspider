import requests
import base64
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_encoded_urls():
    html=requests.get('http://dir.scmor.com/google/',headers=headers).text.replace('\r','').replace('\n','').replace(' ','')
    encoded_urls=re.findall('autourl\[\d+\]="(.*?)";',html)
    return encoded_urls

def from_char_code(a, *b):
    try:
        return unichr(a%65536) + ''.join([unichr(i%65536) for i in b])
    except:
        return chr(a%65536) + ''.join([chr(i%65536) for i in b])

def decode(string):
    string=base64.b64decode(string).decode('utf-8')
    key='link@scmor.com'
    length=len(key)
    code=''
    for i in range(len(string)):
        k=i%length
        code+=from_char_code(ord(string[i])^ord(key[k]))
    result=base64.b64decode(code).decode('utf-8')
    return result

def write_to_txt(urls):
    f=open('result.txt','w')
    for url in urls:
        f.write(url+'\n')
    f.close()

def crawl():
    encoded_urls=get_encoded_urls()
    urls=[]
    for string in encoded_urls:
        url=decode(string)
        urls.append(url)
    write_to_txt(urls)

while True:
    try:
        crawl()
    except Exception as e:
        print(e)
        continue
    print(time.strftime('%Y-%m-%d %X',time.localtime()),'OK')
    time.sleep(3600)
