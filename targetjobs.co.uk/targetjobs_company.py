import requests
from bs4 import BeautifulSoup
import os
import time
import openpyxl


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
}

facts_class = {
    'location': 'pane-node-field-ad-pro-location',
    'vacancies': 'pane-node-field-ad-pro-vacancies',
    'employer_size': 'pane-node-taxonomy-vocabulary-84'
}

url_class = {
    'facebook': 'pane-node-field-ad-pro-facebook',
    'twitter': 'pane-node-field-ad-pro-twitter',
    'linkedin': 'pane-node-field-ad-link-linkedin',
    'instagram': 'pane-node-field-ad-pro-instagram',
    'careers_url': 'pane-node-field-ad-pro-url-careers',
    'homepage': 'pane-node-field-ad-pro-url-main'
}

class NetworkError(Exception):
    pass

def load_content(url):
    for i in range(5):
        try:
            content = requests.get(url, timeout=30).content
            return content
        except:
            continue
    raise NetworkError

def load_html(url,headers):
    for i in range(5):
        try:
            html = requests.get(url,headers, timeout=20).text
            return html
        except:
            continue
    raise NetworkError

def download_img(img_src, filepath):
    content = load_content(img_src)
    with open(filepath, 'wb') as f:
        f.write(content)


def get_company_info(url):
    html = load_html(url,headers)
    soup = BeautifulSoup(html, 'lxml').find('div', {'id': 'block-system-main'})
    result = {}
    try:
        result['des'] = soup.find(
            'div', {'class': 'read-more-wrapper'}).get_text().replace('\xa0', '')
    except:
        result['des'] = ''
    for fact_key in facts_class:
        try:
            item = soup.find('div', {'class': facts_class[fact_key]})
            value = item.find('div', {'class': 'field-item'}).get_text()
            result[fact_key] = value
        except:
            result[fact_key] = ''
    for url_key in url_class:
        try:
            item = soup.find('div', {'class': url_class[url_key]})
            value = item.find(
                'div', {'class': 'field-item'}).find('a').get('href').split('&url=')[-1]
            result[url_key] = value.replace('%3A', ':')
        except:
            result[url_key] = ''
    return result


def get_companies():
    url = 'https://targetjobs.co.uk/employer-hubs'
    result = []
    html = requests.get(url, headers=headers, timeout=20).text
    table = BeautifulSoup(html, 'lxml').find_all(
        'div', {'class': 'search-results-item'})
    for item in table:
        try:
            company = {}
            company['url'] = 'https://targetjobs.co.uk' + \
                item.find('a').get('href')
            company['name'] = item.find('h2').get_text()
            company['img_url'] = item.find('img').get('src')
            company['sectors'] = item.find(
                'p').get_text().replace('Sectors:', '')
        except:
            continue
        result.append(company)
    return result


def crawl():
    companys=get_companies()
    try:
        os.mkdir('images')
    except:
        pass
    result=[]
    for company in companys:
        img_name = company['img_url'].split('/')[-1].split('?')[0]
        try:
            company_info = get_company_info(company['url'])
        except:
            with open('failed.txt','a',encoding='utf-8') as f:
                f.write(str(company)+'\r\n')
            continue
        for key in company_info:
            company[key] = company_info[key]
        try:
            download_img(company['img_url'], 'images/' + img_name)            
        except:
            with open('failed.txt','a',encoding='utf-8') as f:
                f.write(str(company)+'\r\n')
            continue
        company['img_name'] = img_name        
        try:
            print(company['url'], 'OK')
        except:
            pass            
        result.append(company)
    write_to_excel(result)

def write_to_excel(result):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    keys=['name','url','img_url','img_name','des','sectors','location','vacancies','employer_size','homepage','careers_url','facebook','twitter','linkedin','instagram']
    sheet.append(keys)
    for company in result:
        line=[]
        for key in keys:
            try:
                line.append(company[key])
            except:
                line.append('')
        try:
            sheet.append(line)
        except:
            pass
    excel.save('companies.xlsx')

if __name__ == '__main__':
    crawl()
