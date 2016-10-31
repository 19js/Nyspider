import requests
import json
import time
import os

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    'Authorization':"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjU3ZTNkZjBjNDM1NTdhOWIxYjA5MDhlZSIsInJvbGUiOiJzdHVkZW50IiwiaWF0IjoxNDc0OTUxMTU4LCJleHAiOjE0Nzc1NDMxNTh9.XuLlDWgXGemKdZJqvxpAQ7ruOg9Hbv6SK9ELdz5JE64",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_themes():
    f=open('themes.txt','a')
    for line in open('data','r'):
        data=json.loads(line)
        for item in data:
            name=item['name']
            publisher=item['publisher']
            semester=item['semester']
            for themes in item['themes']:
                for theme in themes:
                    try:
                        tipic=theme['name']
                        theme_id=theme['_id']
                        f.write(str([name,publisher,semester,tipic,theme_id])+'\n')
                    except:
                        continue
    f.close()

def get_video_url(theme_id):
    html=requests.get('https://api-v4-0.yangcong345.com/themes/'+theme_id,headers=headers).text
    data=json.loads(html)['topics']
    videos=[]
    for item in data:
        try:
            name=item['name']
            url=item['hyperVideo']['url']['pc']['hls_middle']
            videos.append([name,url])
        except:
            continue
    return videos

def themes():
    f=open('videos.txt','a')
    for line in open('themes.txt','r'):
        line=eval(line)
        theme_id=line[-1]
        try:
            urls=get_video_url(theme_id)
        except:
            failed=open('failed.txt','a')
            failed.write(str(line)+'\n')
            failed.close()
            continue
        for item in urls:
            f.write(str(line+item)+'\n')
        print(line,'ok')
        #time.sleep(0.5)
    f.close()

def save_video(item):
    html=requests.get('http://pchls.media.yangcong345.com/pcM_571ba4c59fcb86114c61cf33.m3u8').text
    urls=[]
    for line in html.split('\n'):
        if '.ts' in line:
            urls.append('http://pchls.media.yangcong345.com/'+line)
    try:
        os.mkdir(item[1])
    except:
        pass
    try:
        os.mkdir('%s/%s'%(item[1],item[2]))
    except:
        pass
    try:
        os.mkdir("%s/%s/%s"%(item[1],item[2],item[0]))
    except:
        pass
    try:
        os.mkdir("%s/%s/%s/%s"%(item[1],item[2],item[0],item[3]))
    except:
        pass
    filename="%s/%s/%s/%s/%s.mp4"%(item[1],item[2],item[0],item[3],item[5])
    f=open(filename,'ab')
    for url in urls:
        count=0
        state=True
        while True:
            try:
                content=requests.get(url,timeout=30).content
                break
            except:
                count+=1
                if count==5:
                    state=False
                    failed=open('failed','a')
                    failed.write(line)
                    failed.close()
                    f.close()
                    os.remove(filename)
                    return
        if not state:
            continue
        f.write(content)
    f.close()
    print(filename,'ok')
                
def videos():
    for line in open('videos.txt','r'):
        item=eval(line)
        try:
            save_video(item)
        except:
            failed=open('failed','a')
            failed.write(line)
            failed.close()
            continue

videos()