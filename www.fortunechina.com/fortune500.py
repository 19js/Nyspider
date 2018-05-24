from util import *
from bs4 import BeautifulSoup
import json


years = [
    ['2017', 'http://www.fortunechina.com/fortune500/c/2017-07/20/content_286785.htm'],
    ['2016', 'http://www.fortunechina.com/fortune500/c/2016-07/20/content_266955.htm'],
    ['2015', 'http://www.fortunechina.com/fortune500/c/2015-07/22/content_244435.htm'],
    ['2014', 'http://www.fortunechina.com/fortune500/c/2014-07/07/content_212535.htm'],
]


def crawl_companys():
    f = open('./files/companys', 'w')
    for year_item in years:
        req = build_request(year_item[-1])
        res_text = req.text.encode("iso-8859-1").decode('utf-8')
        table = BeautifulSoup(res_text, 'lxml').find(
            'table', {'id': 'yytable'}).find_all('tr')
        for tr in table[1:]:
            td_list = tr.find_all('td')
            line = [year_item[0]]
            for td in td_list:
                line.append(td.get_text())
            url = tr.find('a').get('href')
            line.append(url)
            f.write(json.dumps(line, ensure_ascii=False)+'\n')
    f.close()


def crawl_2013_companys():
    page = 1
    f = open('./files/companys', 'a')
    while page < 6:
        if page != 1:
            url = 'http://www.fortunechina.com/fortune500/c/2013-07/08/content_164375_{}.htm'.format(
                page)
        else:
            url = 'http://www.fortunechina.com/fortune500/c/2013-07/08/content_164375.htm'
        req = build_request(url)
        res_text = req.text.encode("iso-8859-1").decode('utf-8')
        table = BeautifulSoup(res_text, 'lxml').find(
            'table', {'class': 'rankingtable'}).find_all('tr')
        for tr in table[1:]:
            td_list = tr.find_all('td')
            line = ['2013']
            for td in td_list:
                line.append(td.get_text())
            url = tr.find('a').get('href')
            line.append(url)
            f.write(json.dumps(line, ensure_ascii=False)+'\n')
        page+=1
    f.close()

def get_company_info(url):
    req=build_request(url)
    thisyeardata=BeautifulSoup(req.text,'lxml').find('div',{'class':'thisyeardata'}).find_all('tr')
    result={}
    for tr in thisyeardata:
        if '<table' in str(tr):
            continue
        if '国家' in str(tr):
            value=tr.find('td').get_text().replace('国家','').replace('：','').replace(':','').replace('\r','').replace('\n','').replace('  ','')
            result['国家']=value
        if '员工数' in str(tr):
            value=tr.find_all('td')[-1].get_text().replace('员工数','').replace('：','').replace(':','').replace('\r','').replace('\n','').replace('  ','')
            result['员工数']=value
        if '营业收入' in str(tr):
            value=tr.find_all('td')[1].get_text()
            result['营业收入']=value
            value=tr.find_all('td')[2].get_text()
            result['营业收入增减']=value
        if '利润' in str(tr) and '利润占比' not in str(tr):
            value=tr.find_all('td')[1].get_text()
            result['利润']=value
            value=tr.find_all('td')[2].get_text()
            result['利润增减']=value
        if '资产' in str(tr) and '资产收益' not in str(tr) and '资产控股' not in str(tr):
            value=tr.find_all('td')[1].get_text()
            result['资产']=value
            value=tr.find_all('td')[2].get_text()
            result['资产增减']=value
        if '股东权益' in str(tr):
            value=tr.find_all('td')[1].get_text()
            result['股东权益']=value
            value=tr.find_all('td')[2].get_text()
            result['股东权益增减']=value
        if '净利率' in str(tr):
            value=tr.find_all('td')[1].get_text()
            result['净利率']=value
        if '资产收益率' in str(tr):
            value=tr.find_all('td')[1].get_text()
            result['资产收益率']=value
    return result

def crawl_info():
    for line in open('./files/companys','r'):
        company=json.loads(line)
        try:
            info=get_company_info(company[-1])
        except:
            f=open('./files/companys_fail','a')
            f.write(json.dumps(company, ensure_ascii=False)+'\n')
            f.close()
            continue
        info['base']=company
        f=open('./files/companys_info','a')
        f.write(json.dumps(info, ensure_ascii=False)+'\n')
        f.close()
        print(company)

def load_companys():
    headers=['name','国家']
    year_list=['2013','2014','2015','2016','2017']
    year_list.reverse()
    for info_key in ['排名','员工数','营业收入','营业收入增减','利润','利润增减','净利率','资产','资产增减','资产收益率','股东权益','股东权益增减']:
        for year in year_list:
            headers.append(year+' '+info_key)
    yield headers
    result={}
    for line in open('./files/companys_info','r'):
        company=json.loads(line)
        key=company['base'][3]
        key=sub_str(key,append=[' '])
        year=company['base'][0]
        if key in result:
            result[key][year]=company
        else:
            result[key]={}
            result[key][year]=company
    for company_key in result:
        line=['','']
        for year in year_list:
            if year not in result[company_key]:
                line.append('')
                continue
            line[0]=result[company_key][year]['base'][3]
            line[1]=result[company_key][year]['base'][-2]
            #当年排名
            line.append(result[company_key][year]['base'][1])
        for info_key in ['员工数','营业收入','营业收入增减','利润','利润增减','净利率','资产','资产增减','资产收益率','股东权益','股东权益增减']:
            for year in year_list:
                if year not in result[company_key]:
                    line.append('')
                    continue
                line.append(sub_str(result[company_key][year][info_key]))
        yield line

#crawl_info()
write_to_excel(load_companys(),'世界500强.xlsx')
    
        
        
        
        
            
                


        



        