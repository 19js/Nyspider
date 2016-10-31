#coding:utf-8

import requests
import os
import sqlite3

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_html(url):
    html=requests.get(url,headers=headers).text
    return html


def get_image(image_url,image_name):
    content=requests.get(image_url,headers=headers).content
    with open(image_name,'wb') as f:
        f.write(content)
        f.close
