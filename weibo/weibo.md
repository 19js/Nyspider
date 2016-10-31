###Python网络爬虫之新浪微博
####1.模拟登录
这里我是利用selenium登录，然后获取登录后的cookies,方便快捷，也免去了编写代码模拟登录的麻烦。requests直接可以利用这个cookies实现登录抓取。

```python
from selenium import webdriver

def login(username,password):
    browser=webdriver.PhantomJS('./phantomjs')
    browser.get('https://passport.weibo.cn/signin/login?entry=mweibo&amp;res=wel&amp;wm=3349&amp;r=http%3A%2F%2Fm.weibo.cn%2F')#打开登录界面
    browser.set_page_load_timeout(10)
    time.sleep(5)#延时等待网页加载完成
    browser.find_element_by_id('loginName').send_keys(username)#填入用户名
    browser.find_element_by_id('loginPassword').send_keys(password)#填入密码
    browser.find_element_by_id('loginAction').click()#点击登录
    time.sleep(5)
    cookies=browser.get_cookies()#获取登录后的cookies
    result={}
    for item in cookies:
        try:
            result[item['name']]=item['value']
        except:
            continue
    return result#返回dict类型cookies

```
requests不能保持手动构建的cookie，因此需要将dict类型的cookie转成cookiejar类型

```python
import requests
import os

def weibo():
    if os.path.isfile('cookies'):
        cookies=eval(open('cookies','r').read())
    else:
        cookies=login('username','password')#获取登录后的cookie
    session=requests.session()
    session.cookies=requests.utils.cookiejar_from_dict(cookies)#将字典转为CookieJar,并传入session中
    return session

```

####2.获取首页微博
```python
import json

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}

session=weibo()
html=session.get('http://m.weibo.cn/index/feed?format=cards&page=1',headers=headers).text
data=json.loads(html)[0]['card_group']
result=[]
for item in data:
    user=item['mblog']['user']['screen_name']
    text=item['mblog']['text']
    weiboid=item['mblog']['idstr']
    result.append({'user':user,'text':text})
print(result)
```

####3.获取微博评论

```python

def get_comments(session,weiboid):
    page=1
    html=session.get('http://m.weibo.cn/single/rcList?format=cards&id={weiboid}&type=comment&hot=0&page={page}'.format(weiboid=weiweiboid,page=page),headers=headers).text
    data=json.loads(html)[1]['card_group']
    comments=[]
    for item in data:
        comment={}
        comment['user']=item['user']['screen_name']
        comment['date']=item['created_at']
        comment['text']=item['text']
        comments.append(comment)
    return comments
```
