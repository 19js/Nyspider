from util import *
import json
import time


def search_user(keyword):
    url = 'https://www.toutiao.com/search_content/?offset={}&format=json&keyword={}&autoload=true&count=20&cur_tab=4&from=media'
    headers = get_headers()
    offset = 0
    result = []
    keys = ['name', 'screen_name', 'user_id', 'media_id',
            'follow_count', 'source_url', 'description', 'verify_content']
    while True:
        try:
            req = build_request(url.format(offset, keyword), headers=headers)
            data = req.json()['data']
        except:
            break
        if len(data) == 0:
            break
        for user in data:
            item = {}
            flag = True
            for key in keys:
                try:
                    item[key] = user[key]
                except:
                    flag = False
                    break
            if not flag:
                continue
            result.append(item)
        offset += 20
        # time.sleep(1)
        print(keyword,'offset', offset)
    return result


def get_last_pub_time(media_id):
    url = 'https://www.toutiao.com/api/pc/media_hot/?media_id={}'.format(media_id)
    req=build_proxy_request(url)
    data=req.json()['data']['hot_articles']
    pub_time_list=[item['publish_time'] for item in data]
    pub_time_list=sorted(pub_time_list,reverse=True)
    return pub_time_list[0]
    


def load_words():
    f = open('./files/words.json', 'r')
    words = json.load(f)
    return words


def load_exists(filename='./files/user_list'):
    exists = {}
    for line in open(filename, 'r'):
        user = json.loads(line)
        exists[user['user_id']] = 1
    return exists


def crawl_user():
    words = load_words()
    exists = load_exists()
    num = 1
    is_ok = True
    for word in words:
        if word != '叭' and is_ok:
            continue
        is_ok = False
        try:
            result = search_user(word)
        except Exception as e:
            print(current_time(), word, 'fail', e)
            continue
        f = open('./files/user_list', 'a')
        for item in result:
            user_id = item['user_id']
            if user_id in exists:
                continue
            if item['follow_count'] < 100 or item['follow_count'] > 90000:
                continue
            exists[user_id] = 1
            f.write(json.dumps(item)+'\n')
            num += 1
        f.close()
        print(current_time(), word, num)

def crawl_active_user():
    num=0
    for line in open('./files/user_list','r'):
        try:
            user=json.loads(line)
            pub_date=get_last_pub_time(user['media_id'])
        except:
            f = open('./files/user_list_fail', 'a')
            f.write(line)
            f.close()
            continue
        user['pub_time']=pub_date
        f = open('./files/result', 'a')
        f.write(json.dumps(user)+'\n')
        f.close()
        num+=1
        print(current_time(),num)


crawl_active_user()
