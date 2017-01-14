import requests
from bs4 import BeautifulSoup
import threading
import time

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


lock=threading.Lock()
lock_failed=threading.Lock()

class Query(threading.Thread):
    def __init__(self,line):
        super(Query,self).__init__()
        self.line=line
        self.url='http://222.35.47.118/web/shopcart/ProductsSetting_Virus_Detail.aspx?id=%s'%line[1]

    def run(self):
        try:
            result=parser(self.url)
            with lock:
                f=open('data/10_1.txt','a',encoding='utf-8')
                f.write(str(self.line+result)+'\n')
                f.close()
        except:
            with lock_failed:
                failed_f=open('data/10_1_failed.txt','a',encoding='utf-8')
                failed_f.write(str(self.line)+'\n')
                failed_f.close()

def parser(url):
    html=requests.get(url,headers=headers,timeout=30).text
    table=BeautifulSoup(html,'lxml').find('table',{'class':'Detail'}).find_all('tr')
    data={}
    keys=['平台资源号', '中文名称', '菌种保藏编号', '特征特性', '属名', '种名加词', '资源归类编码', '其他藏中心编号', '模式菌株', '来源历史', '主要用途', '收藏时间', '生物危害程度', '原始编号', '培养基编号', '原产国', '培养温度', '具体用途', '机构名称', '寄主名称', '隶属单位名称', '致病对象', '资源保藏类型', '致病名称', '保存方法', '传播途径', '实物状态', '分离基物', '共享方式', '采集地', '提供形式', '基因元器件', '获取途径', '记录地址', '图像', '价格', '机构名称编写', '其它', '联系方式', '是否有货', '序列信息']
    for item in table:
        names=item.find_all('td',{'align':'right'})
        values=item.find_all('td',{'align':'left'})
        for i in range(len(names)):
            data[names[i].get_text().replace('\n','')]=values[i].get_text().replace('\xa0','').replace('\r','').replace('\n','')
    result=[]
    for key in keys:
        try:
            result.append(data[key])
        except:
            result.append('')
    return result

def main():
    html=requests.get('http://222.35.47.118/web/shopcart/ProduceList.aspx',headers=headers).text
    page=1
    while True:
        soup=BeautifulSoup(html,'html.parser')
        table=soup.find('table',id='ctl00_ContentPlaceHolder1_GridView1')
        lines=[]
        for item in table:
            try:
                tds=item.find_all('td')
                if len(tds)==0:
                    continue
                line=[]
                for td in tds:
                    try:
                        line.append(td.get_text().replace('\r','').replace('\n','').replace('\t',''))
                    except:
                        line.append('')
                lines.append(line)
            except:
                continue
        for line in lines:
            work=Query(line)
            work.start()
            work.join()
        print(page,'ok')
        page+=1
        data={}
        for item in soup.find_all('input'):
            name=item.get('name')
            if name in ['__VIEWSTATE','__EVENTVALIDATION']:
                data[name]=item.get('value')
        data['ctl00$ContentPlaceHolder1$AspNetPager1_input']=1
        data['__EVENTARGUMENT']=page
        data['__VIEWSTATEGENERATOR']='2709E55C'
        data['__EVENTTARGET']='ctl00$ContentPlaceHolder1$AspNetPager1'
        html=requests.post('http://222.35.47.118/web/shopcart/ProduceList.aspx',data=data,headers=headers).text
main()
