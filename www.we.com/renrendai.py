# coding=utf-8

import requests
from bs4 import BeautifulSoup
import json
import codecs
import logging
import re


# 用户名
j_username = ""
# 密码
j_password = ''


class Renrendai():
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
        self.count = 1
        self.login()

    def login(self):
        data = {
            'j_username': j_username,
            'j_password': j_password,
            'rememberme': 'on',
            'targetUrl': 'http://www.we.com/',
            'returnUrl': 'https://www.we.com/account/index.action'}
        self.session.post(
            'https://www.we.com/j_spring_security_check', data=data, headers=self.headers)

    def run(self):
        id_from = 2121001
        id_to = 2486529
        for loan_id in range(int(id_from), int(id_to)+1):
            try:
                loan_info = self.get_loan_info(loan_id)
            except Exception as e:
                logging.exception(e)
                failed_f = codecs.open(
                    './files/failed.txt', 'a', encoding='utf-8')
                failed_f.write(str(loan_id)+'\n')
                failed_f.close()
                continue
            f = open('./files/loan_result', 'a')
            f.write(json.dumps(loan_info)+'\n')
            f.close()
            print(loan_id,'OK')

    def build_request(self, url):
        for i in range(3):
            try:
                html = self.session.get(
                    url, headers=self.headers, timeout=20).text
                return html
            except Exception as e:
                continue
        return None

    def get_loan_info(self, loan_id):
        url = 'https://www.renrendai.com/pc/loan/{}.html'.format(loan_id)
        html = self.build_request(url)
        loan_info = self.parser_loan(html)
        return loan_info

    def parser_loan(self, html):
        detail = re.findall("var detail = '(.*?)';", html)[0]
        data = json.loads('"%s"' % detail)
        detail = json.loads(data)
        info = re.findall("var info = '(.*?)';", html)[0]
        data = json.loads('"%s"' % info)
        info = json.loads(data)
        return {
            'detail': detail,
            'info': info
        }


if __name__ == '__main__':
    work = Renrendai()
    work.run()
