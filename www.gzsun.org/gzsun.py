from util import *
from bs4 import BeautifulSoup
import re
import json


def parser_notice(html):
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'xinwen1'})
    re_exp={
        '拍卖标的':'拍卖标的\|(.*?)\|',
        '评估价值':'标的评估价值（元）\|(.*?)\|',
        '起拍价':'起拍价（元）\|(.*?)\|',
        '保证金':'保证金（元）\|(.*?)\|',
        '年':'\|\[(\d+)\]第',
        '期数':'\|\[\d+\]第(\d+)期',
        '简介':'拍卖标的简介\|(.*?)\|'
    }
    content=soup.get_text().replace(' ','').replace('\r','').replace('\t','').replace('\n','|').replace('\xa0','').replace('\u3000','')
    for i in range(5):
        content=content.replace('||','|')
    result={}
    for key in re_exp:
        try:
            value=re.findall(re_exp[key],content)[0]
        except:
            value=''
        result[key]=value
    sen_list=re.sub('。|，','|',result['简介']).split('|')
    struct_value=''
    area_value=''
    floor_value=''
    for text in sen_list:
        if '结构' in text:
            struct_value+=text+' '
        if '层' in text:
            floor_value+=text+' '
        if '面积' in text:
            area_value+=text+' '
    result['结构']=struct_value
    result['层']=floor_value
    result['面积']=area_value
    return result

def parser_result(html):
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'xinwen1'})
    re_exp={
        '拍卖标的':'\|拍卖标的：(.*?)\|',
        '拍卖底价':'\|委托拍卖底价：(.*?)\|',
        '成交价':'\|成交价：(.*?)\|',
        '年':'\|\[(\d+)\]第',
        '期数':'\|\[\d+\]第(\d+)期',
    }
    content=soup.get_text().replace(' ','').replace('\r','').replace('\t','').replace('\n','|').replace('\xa0','').replace('\u3000','')
    result={}
    for key in re_exp:
        try:
            value=re.findall(re_exp[key],content)[0]
        except:
            value=''
        result[key]=value
    return result
    
def get_info(url):
    try:
        req=build_request(url)
    except:
        with open('failed.txt','a') as f:
            f.write(url+'\n')
        return
    counter=0
    res_text=req.text
    notice_result=parser_notice(res_text)
    notice_result['url']=url
    if notice_result['拍卖标的']!='':
        f=open('notice.txt','a')
        f.write(json.dumps(notice_result)+'\n')
        f.close()
        counter+=1
    result=parser_result(res_text)
    result['url']=url
    if result['拍卖标的']!='':
        f=open('auction_result.txt','a')
        f.write(json.dumps(result)+'\n')
        f.close()
        counter+=1
    if counter==0:
        f=open('other.txt','a')
        f.write(url+'\n')
        f.close()


def main():
    base_url='http://www.gzsun.org/common/zhengwenye.jsp?ggType=BIAODIXX&zhengwenId={}&lmId=3'
    ID=10000
    while True:
        url=base_url.format(ID)
        get_info(url)
        print(ID,'OK')
        if ID==30964:
            break
        ID+=1

main()
        
