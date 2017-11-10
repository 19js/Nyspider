import requests
import json
import time
import hashlib
import base64
import random

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0"}



def get_proxy_from_nyloner(page, num):
    timestamp = int(time.time())
    string = str(page) + str(num) + str(timestamp)
    md5 = hashlib.md5()
    md5.update(string.encode())
    token = md5.hexdigest()
    url = 'https://nyloner.cn/proxy?page={}&num={}&token={}&t={}'.format(
        page, num, token, timestamp)
    res_text = requests.get(url,headers=headers).text
    res_data = json.loads(res_text)
    result = decode_str(res_data['list'])
    result = eval(result)
    return result


def from_char_code(a, *b):
    return chr(a % 65536) + ''.join([chr(i % 65536) for i in b])


def decode_str(string):
    secret_key = 'nyloner'
    key_length = len(secret_key)
    string = base64.b64decode(string).decode('utf-8')
    code = ''
    for i in range(len(string)):
        index = i % key_length
        code += from_char_code(ord(string[i]) ^ ord(secret_key[index]))
    result = base64.b64decode(code).decode('utf-8')
    return result


def gen_proxies():
    while True:
        ip_list = get_proxy_from_nyloner(1, 15)
        ip_list += get_proxy_from_nyloner(2, 15)
        for index in range(len(ip_list)):
            proxies = {
                'http': 'http://%s:%s' % (ip_list[index]['ip'], ip_list[index]['port'])
            }
            yield proxies

if __name__ == '__main__':
    proxy=gen_proxies()
    for i in range(10):
        print(next(proxy))
