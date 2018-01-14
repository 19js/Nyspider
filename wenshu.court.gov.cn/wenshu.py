import requests
from urllib import parse
import execjs
import json
import random
import re
from bs4 import BeautifulSoup
from proxy.abuyun import get_proxies_abuyun
import openpyxl


def get_headers():
    pc_headers = {
        #"X-Forwarded-For": '%s.%s.%s.%s' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Host": "wenshu.court.gov.cn",
        #"Origin": "http://wenshu.court.gov.cn",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }
    return pc_headers


def create_guid():
    # 获取guid参数
    js1 = '''
		function getGuid() {
	        var guid = createGuid() + createGuid() + "-" + createGuid() + "-" + createGuid() + createGuid() + "-" + createGuid() + createGuid() + createGuid(); //CreateGuid();
	       	return guid;
	    }
	    var createGuid = function () {
	        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
	    }
	'''
    ctx1 = execjs.compile(js1)
    guid = (ctx1.call("getGuid"))
    return guid


def get_number(guid):
    # 获取number
    code_url = "http://wenshu.court.gov.cn/ValiCode/GetCode"
    data = {
        'guid': guid
    }
    req = requests.post(code_url, data=data, headers=get_headers())
    number = req.text
    return number


def get_vjkl5(session, param, guid, number):
    # 获取cookie中的vjkl5
    url = "http://wenshu.court.gov.cn/list/list/?sorttype=1&number=" + number + \
        "&guid=" + guid + "&conditions=searchWord+QWJS+++" + parse.quote(param)
    req = session.get(url=url, headers=get_headers())
    vjkl5 = req.cookies["vjkl5"]
    return vjkl5


def get_vl5x(vjkl5):
    # 根据vjkl5获取参数vl5x
    js = ""
    fp1 = open('./js/sha1.js')
    js += fp1.read()
    fp1.close()
    fp2 = open('./js/md5.js')
    js += fp2.read()
    fp2.close()
    fp3 = open('./js/base64.js')
    js += fp3.read()
    fp3.close()
    fp4 = open('./js/vl5x.js')
    js += fp4.read()
    fp4.close()
    ctx2 = execjs.compile(js)
    vl5x = (ctx2.call('vl5x', vjkl5))
    return vl5x


def get_doclist(param, Index, Page, Order, Direction):
    guid = create_guid()
    number = get_number(guid)
    session = requests.session()
    vjkl5 = get_vjkl5(session, param, guid, number)
    vl5x = get_vl5x(vjkl5)

    # 获取数据
    content_url = "http://wenshu.court.gov.cn/List/ListContent"
    data = {
        "Param": param,
        "Index": Index,
        "Page": Page,
        "Order": Order,
        "Direction": Direction,
        "vl5x": vl5x,
        "number": number,
        "guid": guid
    }
    req = session.post(url=content_url, headers=get_headers(), data=data)
    data = json.loads(req.text)
    doc_list = json.loads(data)
    return doc_list


def wenshu(keyword):
    # 搜索条件
    param = "全文检索:" + keyword  # 搜索关键字
    Index = 1  # 第几页
    Page = 20  # 每页几条
    Order = "法院层级"  # 排序标准
    Direction = "asc"  # asc正序 desc倒序
    while True:
        doc_list = get_doclist(param, Index, Page, Order, Direction)
        if len(doc_list) == 1:
            break
        with open('./files/%s.txt' % keyword, 'a') as f:
            for item in doc_list:
                if 'Count' in item:
                    continue
                item['裁判要旨段原文'] = ''
                item['keyword'] = keyword
                f.write(json.dumps(item) + '\n')
        print(Index, 'OK', len(doc_list))
        Index += 1


def parser_wenshu_content(res_text):
    html_data = re.findall('jsonHtmlData = ("{.*?}");', res_text)[0]
    data = json.loads(html_data)
    data = json.loads(data)
    content = BeautifulSoup(data['Html'], 'lxml').get_text()
    try:
        view_num = re.findall('浏览：(\d+)次', res_text)[0]
    except Exception as e:
        view_num = 0
    result = {
        'title': data['Title'],
        'pubdate': data['PubDate'],
        'view_num': view_num,
        'content': content
    }
    return result


def parser_wenshu_content_by_re(res_text):
    html_data = re.findall('jsonHtmlData = ("{.*?}");', res_text)[0]
    try:
        view_num = re.findall('浏览：(\d+)次', res_text)[0]
    except Exception as e:
        view_num = 0
    res_text=res_text.replace('\\"','"')
    title = re.findall('"Title":"(.*?)"', res_text)[0]
    pubdate = re.findall('"PubDate":"(.*?)"', res_text)[0]
    html = re.findall('"Html":"(.*?)"', res_text)[0]
    content=BeautifulSoup(html, 'lxml').get_text()
    result = {
        'title': title,
        'pubdate': pubdate,
        'view_num': view_num,
        'content': content
    }
    return result


def get_wenshu_content(doc_id):
    url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID='
    for i in range(3):
        try:
            # res_text = requests.get(
            #     url + doc_id, headers=get_headers(), proxies=get_proxies_abuyun(), timeout=10).text
            res_text = requests.get(
                url + doc_id, headers=get_headers(), timeout=10).text
            break
        except Exception as e:
            print(e)
            continue
    try:
        result = parser_wenshu_content(res_text)
    except:
        result = parser_wenshu_content_by_re(res_text)
    return result


def load_result(filename):
    keys = ['案件名称', '法院名称', '案号', '审判程序', '文书ID', '裁判日期',
            'title', 'pubdate', 'view_num', 'content']
    yield keys
    for line in open(filename, 'r'):
        try:
            item = json.loads(line.replace('\n',''))
        except:
            print([line])
            continue
        row = []
        for key in keys:
            try:
                row.append(item[key])
            except:
                row.append('')
        yield row

def write_to_excel(lines,filename):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in lines:
        sheet.append(line)
    excel.save(filename)

if __name__ == '__main__':
    need_keys = ['案件名称', '法院名称', '案号', '审判程序', '文书ID', '裁判日期']
    for word in ['汶川地震', '玉树地震', '芦山地震']:
        # for line in open('./files/%s.txt' % word, 'r'):
        #     item = json.loads(line)
        #     try:
        #         article = get_wenshu_content(item['文书ID'])
        #     except Exception as e:
        #         import logging
        #         logging.exception(e)
        #         with open('./files/%s_failed.txt' % word, 'a') as f:
        #             f.write(line)
        #         print(item['文书ID'], 'Failed')
        #         continue
        #     for key in need_keys:
        #         try:
        #             article[key] = item[key]
        #         except:
        #             article[key] = ''
        #     with open('./files/%s_result.txt' % word, 'a') as f:
        #         f.write(json.dumps(article) + '\n')
        #     print(item['文书ID'], 'OK')
        write_to_excel(load_result('./files/%s_result.txt'%word),word+'.xlsx')
