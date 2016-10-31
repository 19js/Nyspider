import requests
from bs4 import BeautifulSoup
import re
import openpyxl


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_url(url,page):
    html=requests.get(url+'/pg%s'%page,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',{'class':'mod_cont'}).find_all('li',{'class':'pictext'})
    result=[]
    for li in table:
        item={}
        item['url']='http://m.lianjia.com/'+li.find('a').get('href')
        item['title']=li.find('div',{'class':'item_main text_cut'}).get_text()
        result.append(item)
    return result

def get_infor(item):
    html=requests.get(item['url'],headers=headers).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'content_area'})
    info_box=soup.find('div',{'class':'info_box'})
    item['house_price']=info_box.find('div',{'class':'house_price'}).get_text()
    item['tags']=info_box.find('div',{'class':'tag_box'}).get_text()
    tits=soup.find('ul',{'class':'lists'}).find_all('div',{'class':'tit'})
    values=soup.find('ul',{'class':'lists'}).find_all('div',{'class':'value box_col'})
    for index in range(len(tits)):
        item[tits[index].get_text().replace('\r','').replace('\n','').replace(' ','').replace('：','')]=values[index].get_text()
    try:
        item['卖点']=soup.find('p',{'class':'text'}).get_text()
    except:
        pass
    try:
        communityurl='http://m.lianjia.com/'+soup.find('ul',{'class':'lists'}).find('a',{'class':'flexbox'}).get('href')
    except:
        return item
    try:
        html=requests.get(communityurl,headers=headers).text
        soup=BeautifulSoup(html,'lxml').find('div',{'class':'content_area'})
        house_detail=soup.find('div',{'class':'house_detail'})
        tits=house_detail.find_all('span',{'class':'tit'})
        values=house_detail.find_all('span',{'class':'value box_col'})
        for index in range(len(tits)):
            item[tits[index].get_text()]=values[index].get_text()
        try:
            item['均价']=soup.find('h3',{'class':'chart_head'}).get_text()
        except:
            pass
    except:
        pass
    return item

def main():
    url=input('Input url:')
    if '/pg' in url:
        url=re.sub('/pg\d+','',url)
    print(url)
    page=1
    pre=[]
    f=open('result.txt','w',encoding='utf-8')
    while True:
        try:
            result=get_url(url,page)
        except:
            print('failed')
            break
        if pre==result:
            break
        pre=result
        for item in result:
            try:
                hourse=get_infor(item)
            except:
                failed=open('failed.txt','a',encoding='utf-8')
                failed.write(str(item)+'\n')
                failed.close()
                continue
            f.write(str(hourse)+'\n')
        print(page,'ok')
        page+=1
        if page==101:
            break
    f.close()

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    keys=['title', 'url','house_price','tags', '面积', '首付', '月供', '朝向', '楼型', '装修','房源编号', '楼层', '户型', '年代', '地铁', '卖点', '小区', '建造年代', '均价','物业费用', '房屋类型', '绿化率', '楼栋数','建造类型', '容积率', '房屋总数']
    sheet.append(keys)
    for line in open('result.txt','r',encoding='utf-8'):
        try:
            item=eval(line)
        except:
            continue
        hourse=[]
        for key in keys:
            try:
                hourse.append(item[key])
            except:
                hourse.append('-')
        sheet.append(hourse)
    excel.save('result.xlsx')

write_to_excel()
