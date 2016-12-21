import requests
import json

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    'Host':'sysjk.ivdc.org.cn:8081',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def company_page(page):
    data={
    'start':page*20,
    'limit':20,
    'condList':'',
    'isGjcx':0
    }
    html=requests.post('http://sysjk.ivdc.org.cn:8081/cx/query_syscqysj/querysyscqyinfo.do', data=data,headers=headers).text
    data=json.loads(html)['rows']
    result=[]
    for item in data:
        line=[]
        for key in ['qymc','xkzh','gmpZsh','cym','itemid']:
            try:
                line.append(item[key])
            except:
                line.append('')
        result.append(line)
    return result

def detail(itemidlist):
    data={
    'itemidList':str(itemidlist)
    }
    keys=['bgqk', 'byx', 'comid', 'cym', 'fddbr', 'fddbrzz', 'fzrq', 'gmpBgqk', 'gmpByx', 'gmpGgh', 'gmpGgrq', 'gmpItemid', 'gmpQydm', 'gmpQymc', 'gmpQyxz', 'gmpScdz', 'gmpSf', 'gmpShr', 'gmpShrq', 'gmpSxrq', 'gmpYsfw', 'gmpYszt', 'gmpZsh', 'gmpZszt', 'itemid', 'qydm', 'qyfzr', 'qymc', 'scdz', 'scfw', 'shr', 'shrq', 'xkzh', 'yxqz', 'zcdz', 'zhnd', 'zszt']
    html=requests.post('http://sysjk.ivdc.org.cn:8081/cx/query_syscqysj/querysyscqydetail.do', data=data,headers=headers).text
    data=json.loads(html)['rows']
    result={}
    for item in data:
        itemid=item['itemid']
        line=[]
        for key in keys:
            try:
                line.append(item[key])
            except:
                line.append('')
        try:
            result[itemid].append(line)
        except:
            result[itemid]=[line]
    return result

def main():
    page=0
    while True:
        companys=company_page(page)
        if companys==[]:
            break
        itemidlist=[]
        for company in companys:
            itemidlist.append(company[-1])
        result=detail(itemidlist)
        f=open('data/company.txt','a',encoding='utf-8')
        for company in companys:
            itemid=company[-1]
            for line in result[itemid]:
                f.write(str(company+line)+'\n')
        f.close()
        print(page,'ok')
        page+=1

main()
