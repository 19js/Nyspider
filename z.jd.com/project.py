import requests
from bs4 import BeautifulSoup
import time
import json
import openpyxl

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}


def get_project_list(page,category_id):
    data={
        'status':8,
        'sort':'zhtj',
        'categoryId':category_id,
        'page':page
    }
    html=requests.post('https://z.jd.com/bigger/search.html',data=data,headers=headers,timeout=30).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'l-result'}).find_all('li',{'class':'info'})
    result=[]
    for item in soup:
        try:
            name=item.find('h4',{'class':'link-tit'}).get_text()
            url=item.find('a').get('href')
            result.append([name,url])
        except Exception as e:
            print(e)
            continue
    return result

def get_project_count(project_id):
    url='https://sq.jr.jd.com/cm/getCount?key=1000&systemId={}'
    html=requests.get(url.format(project_id),headers={'Referer':'https://z.jd.com/project/details/{}.html'.format(project_id)},timeout=30).text
    data=json.loads(html.replace('(','').replace(')',''))['data']
    create_time=data['createTime']
    focus_num=data['focus']
    praise_num=data['praise']
    return (focus_num,praise_num,create_time)

def get_topic_num(project_id):
    url='https://sq.jr.jd.com/topic/count?key=1000&systemId={}'
    html=requests.get(url.format(project_id),headers={'Referer':'https://z.jd.com/project/details/{}.html'.format(project_id)},timeout=30).text
    count=json.loads(html.replace('(','').replace(')',''))['count']
    return count

def get_project_base_info(project_id):
    html=requests.get('https://z.jd.com/project/details/{}.html'.format(project_id),headers=headers,timeout=30).text
    soup=BeautifulSoup(html,'lxml').find('div',{'class':'main'})
    project_soup=soup.find('div',{'class':'project-introduce'})
    wrap_details=soup.find('div',{'class':'wrap-details'})
    try:
        amount=project_soup.find('p',{'class':'p-num'}).get_text()
    except:
        amount='-'
    try:
        percent=project_soup.find('p',{'class':'p-progress'}).find('span',{'class':'fl percent'}).get_text()
    except:
        percent='-'
    try:
        surport_num=project_soup.find('p',{'class':'p-progress'}).find_all('span')[1].get_text()
    except:
        surport_num='-'
    try:
        f_red_list=project_soup.find('p',{'class':'p-target'}).find_all('span',{'class':'f_red'})
    except:
        f_red_list=[]
    try:
        dead_line=f_red_list[0].get_text().replace('\r\n','').replace(' ','')
    except:
        dead_line='-'
    try:
        target_amount=f_red_list[1].get_text().replace('\r\n','').replace(' ','')
    except:
        target_amount='-'
    try:
        focus_num,praise_num,create_time=get_project_count(project_id)
    except:
        focus_num='-'
        praise_num='-'
        create_time='-'
    try:
        topic_num=get_topic_num(project_id)
    except:
        topic_num='-'
    try:
        process_num=wrap_details.find('div',id='qaBtn').find('span').get_text()
    except:
        process_num='-'
    result=[amount,percent,surport_num,dead_line,target_amount,focus_num,praise_num,create_time,topic_num,process_num]

    details_r=wrap_details.find('div',{'class':'details-r'})
    icon_v='0'
    icon_crown='0'
    try:
        promoters_name=details_r.find('div',{'class':'promoters-name'})
        name=promoters_name.find('a').get('title')
        if 'icon-crown' in str(promoters_name):
            icon_crown='1'
        if 'icon-v' in str(promoters_name):
            icon_v='1'
    except:
        name='-'
    try:
        promoters_num=details_r.find('div',{'class':'promoters-num'}).find_all('div',{'class':'fl'})
        start_num=promoters_num[0].get_text()
        s_num=promoters_num[1].get_text()
    except:
        start_num='0'
        s_num='0'

    try:
        contact_box=details_r.find('ul',{'class':'contact-box'}).find_all('li')
    except Exception as e:
        contact_box=[]
    company_name='-'
    company_address='-'
    company_phone='-'
    company_work_time='-'
    for item in contact_box:
        if '公司名称' in str(item):
            company_name=item.find('div',{'class':'val'}).get_text()
        if '联系地址' in str(item):
            company_address=item.find('div',{'class':'val'}).get_text().replace('\xa0','')
        if '官方电话' in str(item):
            company_phone=item.find('div',{'class':'val'}).get_text()
        if '工作时间' in str(item):
            company_work_time=item.find('div',{'class':'val'}).get_text()
    result+=[name,icon_v,icon_crown,start_num,s_num,company_name,company_address,company_phone,company_work_time]

    boxs=details_r.find_all('div',{'class':'box-grade'})
    for box in boxs:
        try:
            price=box.find('div',{'class':'t-price'}).get_text().replace('\r','').replace('\n','').replace('\t','').replace(' ','')
            people=box.find('div',{'class':'t-people'}).get_text().replace('\r','').replace('\n','').replace('\t','').replace(' ','')
        except:
            continue
        box_items=box.find_all('p',{'class':'box-item'})
        date='-'
        for box_item in box_items:
            if '预计回报发送时间' in str(box_item):
                date=box_item.find('span').get_text()
        result+=[price,people,date]
    return result

def crawl_project_list():
    keys={
        '科技':10,
        '美食':36,
        '家电':37,
        '设计':12,
        '娱乐':11,
        '出版':38,
        '公益':13,
        '其他':14
    }
    for key in keys:
        page=1
        pre_list=[]
        while True:
            try:
                result=get_project_list(page,keys[key])
            except Exception as e:
                print(e,key)
                continue
            if pre_list==result:
                break
            pre_list=result
            f=open('projects.txt','a')
            for item in result:
                f.write(str([key]+item)+'\n')
            f.close()
            print(key,page,'OK')
            page+=1

def crawl():
    for line in open('projects.txt','r'):
        item=eval(line)
        try:
            result=get_project_base_info(item[-1].split('/')[-1].split('.')[0])
        except:
            failed_f=open('failed.txt','a')
            failed_f.write(line)
            failed_f.close()
            continue
        f=open('result.txt','a')
        f.write(str(item+result)+'\n')
        f.close()
        print(item,'OK')

crawl()
