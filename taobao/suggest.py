import requests
import json
import time
import os
import chardet

headers = {
        ':authority':'suggest.taobao.com',
        'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
        'Accept':"*/*",
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}


def suggest(keyword):
    html=requests.get('https://suggest.taobao.com/sug?q={}&code=utf-8&area=c2c&nick=&sid=null'.format(keyword),headers=headers).text
    data=json.loads(html)['result']
    result=[]
    for item in data:
        result.append(item[0].replace('</b>','').replace('<b>',''))
    return result

def get_chardet(filename):
    data=open(filename,'rb').read()
    coding=chardet.detect(data)
    return coding['encoding']

def loadkeywords():
    keywords={}
    for filename in os.listdir('keywords'):
        if '.txt' not in filename:
            continue
        encoding=get_chardet('keywords/'+filename)
        if encoding=='GB2312':
            encoding='GBK'
        keywords[filename]=[]
        for line in open('keywords/'+filename,'r',encoding=encoding):
            word=line.replace('\r','').replace('\n','')
            keywords[filename].append(word)
    return keywords

def save_to_txt(filename,deep,words):
    f=open('result/'+filename.replace('.txt','_%s.txt'%deep),'w',encoding='utf-8')
    writed=[]
    for word in words:
        if word in writed:
            continue
        writed.append(word)
        f.write(word+'\r\n')
    f.close()

def main():
    keywords=loadkeywords()
    while True:
        try:
            deep=input("输入采集深度:")
            deep=int(deep)
            break
        except:
            pass
    for filename in keywords:
        result=[]
        for word in keywords[filename]:
            words=[word]
            count=0
            for num in range(deep):
                suggest_words=[]
                for need_word in words:
                    try:
                        suggest_words+=suggest(need_word)
                    except:
                        continue
                suggest_words=list(set(suggest_words))
                words=suggest_words
                count+=len(suggest_words)
                result+=suggest_words
                print(word,'deep',num+1)
            print(word,'get',count,'ok')
        save_to_txt(filename,deep,result)

main()
