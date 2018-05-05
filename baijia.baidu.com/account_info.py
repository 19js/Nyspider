from util import *
from bs4 import BeautifulSoup
import json
import time
import re



def get_user_info(app_id):
    info_url = 'https://author.baidu.com/profile?context={{%22from%22:0,%22app_id%22:%22{app_id}%22}}&cmdType=&pagelets[]=root&reqID=0&ispeed=1'.format(
        app_id=app_id)
    session = requests.session()
    for i in range(3):
        session.get('https://baijiahao.baidu.com/u?app_id={}'.format(app_id),headers=get_headers(),timeout=20)
        res_text = session.get(info_url,headers=get_headers(),timeout=20).text
        res_text = re.findall('onPageletArrive\((.*)\);', res_text)[0]
        data = json.loads(res_text)
        soup = BeautifulSoup(data['html'], 'lxml')
        fans = soup.find('div', {'class': 'fans'}).get_text()
        sign = soup.find('div', {'class': 'sign'}).get_text()
        name = soup.find('div', {'class': 'name'}).get_text()
        if '-' in fans:
            continue
        article_url='https://author.baidu.com/pipe?context={{%22from%22:0,%22app_id%22:%22{}%22}}&pagelets[]=article&reqID=1&ispeed=1'.format(app_id)
        res_text=session.get(article_url,headers=get_headers(),timeout=20).text
        res_text = re.findall('onPageletArrive\((.*)\);', res_text)[0]
        data = json.loads(res_text)
        update_time=BeautifulSoup(data['html'],'lxml').find('div',{'class':'time'}).get_text()
        break
    return {
        'fans': fans,
        'app_id':app_id,
        'sign': sign,
        'name': name,
        'update_time':update_time,
        'url':'https://baijiahao.baidu.com/u?app_id={}&fr=bjharticle'.format(app_id)
    }



def load_exists(filename='./files/app_id'):
    exists = {}
    for line in open(filename, 'r'):
        user = json.loads(line)
        exists[user['app_id']] = 1
    return exists


def load_words():
    # text=open('./files/words.txt','r').read()
    # words=[word for word in text]
    # f=open('./files/words.json','w')
    # json.dump(words,f)
    # f.close()
    f=open('./files/words.json','r')
    words=json.load(f)
    return words


def search():
    url = 'https://mbd.baidu.com/webpage?action=searchresource3&type=subscribe&format=json&word={}'
    words = load_words()
    exists = load_exists()
    num = 0
    headers = get_headers()
    headers['Cookie'] = ''
    for word in words:
        try:
            req = build_request(url.format(word), headers=headers)
            data = req.json()['data']['items']['user']['item']
        except Exception as e:
            print(word, 'fail')
            time.sleep(1)
            continue
        f = open('./files/app_id', 'a')
        for item in data:
            try:
                app_id = item['third_id']
            except:
                continue
            if len(app_id) < 10:
                continue
            if app_id in exists:
                continue
            exists[app_id] = 1
            f.write(json.dumps({'app_id': app_id})+'\n')
            num += 1
        f.close()
        print(current_time(), word, num)
        time.sleep(1)


def crawl_user_info():
    success=0
    fail=0
    for line in open('./files/app_id','r'):
        user=json.loads(line)
        if len(user['app_id']) < 10:
            continue
        try:
            result=get_user_info(user['app_id'])
        except Exception as e:
            f = open('./files/fail', 'a')
            f.write(json.dumps(user)+'\n')
            f.close()
            fail+=1
            print(current_time(),success,fail)
            continue
        success+=1
        f = open('./files/result', 'a')
        f.write(json.dumps(result)+'\n')
        f.close()
        print(current_time(),success,fail)

search()
crawl_user_info()