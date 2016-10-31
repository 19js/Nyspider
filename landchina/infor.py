import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_infor(item):
    html=requests.get('http://www.landchina.com/'+item[0],headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('table',id='mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1')
    tr_ids=['mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r17', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r12','mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r23', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21','mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10', 'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14']
    line=''
    for trid in tr_ids:
        if trid=='mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r12':
            try:
                trs=table.find('tr',id=trid).find('table',id='mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3').find_all('tr')
                text='|分期支付约定:'
                for tr in trs:
                    if 'r2_tmp' in str(tr) or 'p1_f3_r1' in str(tr):
                        continue
                    for td in tr.find_all('td'):
                        text+=td.get_text()+' '
            except:
                continue
        elif trid=='mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21':
            try:
                tr=table.find('tr',id=trid)
            except:
                continue
            try:
                down=tr.find('td',id='mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c2').get_text()
            except:
                down=''
            try:
                up=tr.find('td',id='mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c4').get_text()
            except:
                up=''
            try:
                date=tr.find('td',id='mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21_c4').get_text()
            except:
                date=''
            text='|约定容积率下限:'+down+'|约定容积率上限:'+up+'|约定交地时间:'+date
        else:
            try:
                tds=table.find('tr',id=trid).find_all('td')
            except:
                continue
            text=''
            for td in tds:
                text+='| '+td.get_text()
        line+=text
    line=line.replace('\r','').replace('\n','').replace('\t','').replace('||','|').replace('||','|').replace('：',':').replace(':|',':')
    item={}
    keys=[]
    for key_value in line.split('|'):
        key=key_value.split(':')[0]
        if key.replace(' ','').replace('\xa0','')=='':
            continue
        keys.append(key)
        try:
            item[key]=key_value.split(':')[1]
        except:
            item[key]=''
    if item[' 面积(公顷)']==item[' 土地来源']:
        item[' 土地来源']='现有建设用地'
    elif float(item[' 土地来源'])==0:
        item[' 土地来源']='新增建设用地'
    else:
        item[' 土地来源']='新增建设用地(来自存量库)'
    return item

def main():
    keys=[' 行政区', ' 电子监管号', ' 项目名称', ' 项目位置', ' 面积(公顷)', ' 土地来源', ' 土地用途', ' 供地方式', ' 土地使用年限', ' 行业分类', ' 土地级别', ' 成交价格(万元)', '分期支付约定', ' 土地使用权人', '约定容积率下限', '约定容积率上限', '约定交地时间', ' 约定开工时间', ' 约定竣工时间', ' 实际开工时间', ' 实际竣工时间', ' 批准单位', ' 合同签订日期']
    try:
        os.mkdir('result')
    except:
        pass
    for filename in os.listdir('province'):
        f=open('result/'+filename,'a')
        count=0
        for line in open('province/'+filename,'r'):
            try:
                line=eval(line)
            except:
                continue
            try:
                item=get_infor(line)
            except:
                failed=open('failed_'+filename,'a')
                failed.write(str(line)+'\n')
                failed.close()
                continue
            f.write(str(item)+'\n')
            count+=1
            print(filename,count)
        f.close()

main()
