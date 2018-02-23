from util import *
from bs4 import BeautifulSoup
import json

cookie = 'PHPSESSID=kpks57t94k32q5g8q7gdl5pjl7; __jsluid=3c97a105e1e5e31c3203dfcb9c236dcd; Hm_lvt_de72ed30dc21da8d5dcf608850a7aaac=1519364738; gr_user_id=38f84b24-abf6-40ef-8f4e-c249c576ffa7; gr_session_id_b9a32bc6f5df5804=6a0da6b7-b5b6-4896-afbe-6dffbf6bd4ac; yd_username=18502793163; uv_flag=C7E29E49-6940-0001-6532-181E8EA01EA8; UM_distinctid=161c136f2e33cf-013d8779ecffca-32667b04-1fa400-161c136f2e479f; CNZZDATA1260321659=886797634-1519362400-https%253A%252F%252Fwww.yindou.com%252F%7C1519362400; _b_rz=rongzhitanchuang; ydurl=https://www.yindou.com/myaccount/; ydreferrer=https://www.yindou.com/; _dg_f2=ok; ydrecord=46075_1519365354; _kela_guide=ok; get_str=%7B%22%5C%2Findex_php5%22%3A%22%22%2C%22zhaiquangoumai%5C%2F%22%3A%22%22%2C%22page%22%3A%228%22%2C%22total%22%3A%220%22%2C%22rate%22%3A%22%22%2C%22leftday%22%3A%22%22%2C%22backday%22%3A%22%22%2C%22category%22%3A%22%22%7D; Hm_lpvt_de72ed30dc21da8d5dcf608850a7aaac=1519366102'


def get_urls():
    page = 1
    while True:
        url = 'https://www.yindou.com/zhaiquangoumai/?page={}&total=0&rate=&leftday=&backday=&category='.format(
            1)
        req = build_request(url)
        table = BeautifulSoup(req.text, 'lxml').find(
            'div', {'class': 'iv-body'}).find_all("div", {'class': 'iv-block'})
        f = open('urls.txt', 'a')
        for item in table:
            spans = item.find_all('span')
            link = item.find('a').get('href')
            line = []
            for span in spans:
                value = span.get_text().replace('\n', '').replace(' ', '')
                line.append(value)
            line.append(link)
            f.write(str(line)+'\n')
        f.close()
        if page == 1152:
            break
        print(page, 'OK')
        page += 1


def get_detail(url):
    headers = get_headers()
    headers['Cookie'] = cookie
    req = build_request(url, headers)
    soup = BeautifulSoup(req.text, 'lxml').find(
        'div', {'class': 'iv_prj_dtl_cont-block'})
    table = soup.find('div', {'class': 'iv_cont_intro-block'}
                      ).find_all('p', {'class': 'd_ele'})
    result = {}
    keys = []
    for item in table:
        name = item.find('span').get_text().replace('\n', '')
        value = item.get_text().replace('\n', '')
        result[name] = value
        keys.append(name)
    info_soup = soup.find('div', {'class': 'iv_cont_info-block'})
    table = info_soup.find_all('p', {'class': 'in_option'})
    for item in table:
        name = item.find('span').get_text().replace('\n', '')
        value = item.get_text().replace('\n', '')
        result[name] = value
        keys.append(name)
    table = info_soup.find_all('div', {'class': 'in_option_div'})
    for item in table:
        name = item.find('span').get_text().replace('\n', '')
        value = item.get_text().replace('\n', '')
        result[name] = value
        keys.append(name)
    return result


def crawl():
    for line in open('urls.txt', 'r'):
        item = eval(line)
        try:
            result = get_detail('https://www.yindou.com'+item[-1])
        except:
            with open('failed.txt', 'a') as f:
                f.write(line)
            print(item[-1], 'Failed')
            continue
        values = {}
        values['base_info'] = item
        values['detail'] = result
        with open('result.txt', 'a') as f:
            f.write(json.dumps(values)+'\n')
        print(item[-1], 'OK')


def load_txt():
    keys = ['项目名称：', '计息天数：', '借款金额：', '加入条件：', '起息时间：', '还款日期：', '提现到账：', '还款方式：', '站内转让：', '产品类别：', '相关费用：', '合同范本：', '借款人姓名：', '借款人证件号：', '借款人性别：',
            '借款人手机号：', '借款人年龄：', '借款人婚姻状况：', '借款人现居住地：', '借款人户口所在地：', '风险提示：', '借款用途：', '还款来源：', '本平台逾期次数：', '本平台逾期总金额：', '身份证信息：', '征信情况：', '收入情况：', '综合评估：']
    yield ['']*10+keys
    for line in open('./result.txt', 'r'):
        line = json.loads(line)
        item = line['base_info']
        for key in keys:
            try:
                value = line['detail'][key].replace(key, '').replace('  ','')
                item.append(value)
            except:
                item.append('')
        yield item


write_to_excel(load_txt(),'result.xlsx')
