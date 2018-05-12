from util import *
import time
from bs4 import BeautifulSoup
import json


def get_movie_list():
    offset = 0
    base_url = 'http://v.qq.com/x/list/movie?sort=19&offset={}'
    while True:
        try:
            req = build_request(base_url.format(offset))
            figures_list = BeautifulSoup(req.text, 'lxml').find(
                'ul', {'class': 'figures_list'}).find_all('li', {'class': 'list_item'})
        except Exception as e:
            print('offset', offset, 'fail', e)
            continue
        f = open('./files/movie_list', 'a')
        for item in figures_list:
            movie = {}
            movie['url'] = item.find('a').get('href')
            movie['cid'] = item.find('a').get('data-float')
            movie['title'] = item.find(
                'div', {'class': 'figure_title_score'}).find('a').get_text()
            try:
                movie['figure_score'] = item.find(
                    'div', {'class': 'figure_score'}).get_text().replace('\n', '')
            except:
                movie['figure_score'] = ''
            try:
                movie['mark_v'] = item.find(
                    'i', {'class': 'mark_v'}).find('img').get('alt')
            except:
                movie['mark_v'] = ''
            f.write(json.dumps(movie)+'\n')
        f.close()
        if offset == 4980:
            break
        print(current_time(), offset, 'OK')
        offset += 30
        time.sleep(1)


def get_float_info():
    url = 'http://node.video.qq.com/x/api/float_vinfo2?cid=3ou2gtkskly3a99'


def get_movie_info(url):
    req = build_request(url)
    try:
        res_text = req.text.encode('iso-8859-1').decode('utf-8')
    except:
        res_text = req.text
    soup = BeautifulSoup(res_text, 'lxml').find('body')
    info = {}
    current_item = soup.find('ul', {'class': 'figure_list'}).find(
        'li', {'class': 'list_item'})
    info['play_time'] = current_item.find(
        'div', {'class': 'figure_count'}).find('span').get_text()
    info['figure_num'] = current_item.find(
        'div', {'class': 'figure_num'}).find('span').get_text()
    info['mod_cover_playnum'] = soup.find(
        'em', {'id': 'mod_cover_playnum'}).get_text()
    try:
        douban_score = soup.find('span', {'class': 'douban_score'})
        info['douban_score'] = douban_score.get_text().replace('\n', '')
    except:
        info['douban_score'] = ''
    video_tags = soup.find('div', {'class': 'video_tags'})
    if '豆瓣高分' in str(video_tags):
        info['douban_high_score'] = '是'
    else:
        info['douban_high_score'] = '否'
    info['院线'] = '否'
    info['tags'] = ''
    video_tag_list = video_tags.find_all('a')
    for tag in video_tag_list:
        try:
            href = tag.get('href')
        except:
            href = ''
        if 'area=' in href:
            info['area'] = tag.get_text()
        elif 'year=' in href:
            info['year'] = tag.get_text()
        else:
            tag_value = tag.get_text()
            if '院线' in tag_value:
                info['院线'] = '是'
            else:
                info['tags'] += tag_value+' '
    director = soup.find('div', {'class': 'director'})
    if director is None:
        return info
    director_text = director.get_text().replace('\xa0', '').replace('\n', '')
    if '演员' in director_text:
        info['actor_list'] = director_text.split('演员')[-1].replace(':', '')
        info['director'] = director_text.split('演员')[0].replace('导演:', '')
    else:
        info['director'] = director_text
        info['actor_list'] = ''
    return info


def crawl_movie_info():
    for line in open('./files/movie_list', 'r'):
        try:
            item = json.loads(line)
            info = get_movie_info(item['url'])
        except Exception as e:
            print(current_time(), 'fail', e)
            f = open('./files/fail', 'a')
            f.write(line)
            f.close()
            continue
        for key in item:
            info[key] = item[key]
        f = open('./files/result', 'a')
        f.write(json.dumps(info)+'\n')
        f.close()
        print(current_time(), info['title'], 'OK')
        time.sleep(0.2)

def load_result():
    keys = ['title', 'year', 'play_time', 'tags', 'figure_score', 'douban_score', 'figure_num',
            'mod_cover_playnum', 'mark_v', '院线', 'director', 'actor_list', 'douban_high_score', 'area','url']
    num = 1
    for line in open('./files/result', 'r'):
        movie = json.loads(line)
        item = [num]
        if 'area' not in movie:
            movie['area']=movie['tags'].split(' ')[0]
            movie['tags']=movie['tags'].replace(movie['area']+' ','')
        for key in keys:
            if key == 'mark_v':
                values = ['否', '否', '否']
                if 'VIP' in movie[key]:
                    values[1] = '是'
                elif '用券' in movie[key]:
                    values[0] = '是'
                elif '独播' in movie[key]:
                    values[2] = '是'
                item += values
                continue
            try:
                item.append(movie[key])
            except:
                item.append('')
        yield item
        num+=1

write_to_excel(load_result(),'腾讯电影.xlsx')
