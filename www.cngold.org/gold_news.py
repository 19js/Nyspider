from util import *
from bs4 import BeautifulSoup
import json


def get_news_list(url):
    """
    获取新闻列表
    """
    req = build_request(url)
    res_text = req.text.encode('iso-8859-1').decode('utf-8')
    ul_list = BeautifulSoup(res_text, 'lxml').find(
        'div', {'class': 'left_info'}).find_all('li')
    result = []
    for item in ul_list:
        try:
            title = item.find('a').get_text()
            news_url = item.find('a').get('href')
            author = item.find_all('span')[-1].get_text()
            date = item.find_all('span')[0].get_text()
        except:
            continue
        result.append([title, news_url, author, date])
    return result


def get_news_info(url):
    """
    获取新闻内容和摘要
    """
    req = build_request(url)
    try:
        res_text = req.text.encode('iso-8859-1').decode('utf-8')
    except:
        res_text = req.text
    soup = BeautifulSoup(res_text, 'lxml').find('div', {'class': 'main'})
    article_des_item = soup.find(
        'dl', {'class': 'aricleDes'})
    if article_des_item is None:
        article_des_item = soup.find(
            'div', {'class': 'abstract'})
    if article_des_item is None:
        article_des_item = soup.find(
            'div', {'class': 'art_zy'})
    if article_des_item is not None:
        article_des = article_des_item.get_text().replace('摘要', '').replace('\n', '')
    else:
        article_des = ''
    content = soup.find('div', {'id': 'zoom'}).get_text()
    list_page = soup.find('div', {'id': 'zoom'}).find(
        'div', {'class': 'listPage'})
    if list_page is None:
        return [article_des, content]
    content = content.replace(list_page.get_text(), '')
    page = 2
    while True:
        try:
            req = build_request(url.replace('.html', '_%s.html' % page))
            if req.status_code == 404:
                break
            res_text = req.text.encode('iso-8859-1').decode('utf-8')
            soup = BeautifulSoup(res_text, 'lxml').find(
                'div', {'id': 'zoom'})
        except:
            break
        text = soup.get_text()
        list_page = soup.find(
            'div', {'class': 'listPage'})
        if list_page is not None:
            text = text.replace(list_page.get_text(), '')
        page += 1
        content += text
    return [article_des, content]


def get_history_news():
    """
    获取日期
    """
    req = build_request('https://www.cngold.org/news/futures/list_11_all.html')
    history_news_content_list = BeautifulSoup(req.text, 'lxml').find_all('div', {
        'class': 'history_news_content'})
    f = open('./files/history_news', 'a')
    for content in history_news_content_list:
        history_news = content.find_all('li')
        for li in history_news:
            title = li.find('a').get_text()
            url = li.find('a').get('href')
            f.write(json.dumps([title, url])+'\n')
    f.close()


def crawl_news():
    get_history_news()
    for line in open('./files/history_news', 'r'):
        history_news = json.loads(line)
        if '2018' in line:
            continue
        try:
            news_list = get_news_list(history_news[-1])
        except Exception as e:
            f = open('./files/history_news_fail', 'a')
            f.write(line)
            f.close()
            print(current_time(), history_news[0], 'fail', e)
            continue
        for news_item in news_list:
            try:
                news_info = get_news_info(news_item[1])
            except:
                f = open('./files/news_fail', 'a')
                f.write(json.dumps(news_item)+'\n')
                f.close()
                print(current_time(), news_item[1], 'fail')
                continue
            f = open('./files/result', 'a')
            f.write(json.dumps(history_news+news_item+news_info)+'\n')
            f.close()
        print(current_time(), history_news[0], 'OK')


crawl_news()
# write_to_excel(load_txt('./files/result'),'news.xlsx')
