import requests
from bs4 import BeautifulSoup
import json


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def search(key):
    offset=0
    while offset<100:
        data=requests.get('https://www.zhihu.com/r/search?q={}&type=content&offset={}'.format(key,offset),headers=headers).text
        items=parser(data)
        print(items)
        return

def parser(data):
    htmls=json.loads(data)['htmls']
    result=[]
    for html in htmls:
        item={}
        soup=BeautifulSoup(html,'html.parser').find('div',{'class':'content'})
        item['question-id']=soup.find('meta',{'itemprop':'question-id'}).get('content')
        item['question-url-token']=soup.find('meta',{'itemprop':'question-url-token'}).get('content')
        item['title']=soup.find('a').get_text()
        answer=soup.find('div',{'class':['entry','answer']})
        item['answer-id']=answer.find('meta',{'itemprop':'answer-id'}).get('content')
        item['answer-url-token']=answer.find('meta',{'itemprop':'answer-url-token'}).get('content')
        item['votecount']=answer.find('a',{'class':'zm-item-vote-count'}).get_text()
        try:
            item['author']=answer.find('a',{'class':'author'}).get_text()
        except:
            item['author']='匿名用户'
        item['answer-content']=answer.find('script',{'class':'content'}).get_text()
        item['answer-content']=BeautifulSoup(item['answer-content'],'html.parser').get_text()
        item['date']=answer.find('a',{'class':'time text-muted'}).get('data-tooltip')
        item['answer-comment-count']=answer.find('a',{'class':'js-toggleCommentBox'}).find('span').get_text()
        if '添加评论' in item['answer-comment-count']:
            item['answer-comment-count']=0
        item['copyright']=answer.find('a',{'class':'js-copyright'}).get_text()
        result.append(item)
    return result

def question_infor():


search('key')
