import requests
from bs4 import BeautifulSoup
import openpyxl
import time
from selenium import webdriver

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}


def get_term(journal=None,date_from=None,date_to=None):
    term=''
    if date_from!=None and date_to==None:
        term='("%s"[Date - Publication] : "3000"[Date - Publication])'%(date_from)
    elif date_from!=None and date_to!=None:
        term='("%s"[Date - Publication] : "%s"[Date - Publication])'%(date_from,date_to)
    elif date_from==None and date_to==None:
        term=''
    else:
        return False
    if journal!=None:
        if term!='':
            term='(%s) AND "%s"[Journal]'%(term,journal)
        else:
            term='"%s"[Journal]'%journal
    return term

def get_urls(term):
    url='http://www.ncbi.nlm.nih.gov/pubmed/?term='+term
    browser=webdriver.Firefox()
    browser.get(url)
    browser.implicitly_wait(10)
    items=[]
    page=1
    while True:
        html=browser.page_source
        result=page_parser(html)
        if result==[]:
            break
        items+=result
        print(page,'ok')
        page+=1
        try:
            browser.find_element_by_xpath("//a[@id='EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Entrez_Pager.Page' and @sid=3]").click()
        except:
            break
        time.sleep(5)
    return items

def page_parser(html):
    try:
        table=BeautifulSoup(html,'lxml').find('div',{'class':'content'}).find_all('div',{'class':"rprt"})
    except:
        return []
    result=[]
    for div in table:
        try:
            title=div.find('a').get_text()
            url='http://www.ncbi.nlm.nih.gov/'+div.find('a').get('href')
            result.append({'title':title,'url':url})
        except:
            continue
    return result

def get_infor(item):
    html=requests.get(item['url'],headers=headers,timeout=30).text
    try:
        afflist=BeautifulSoup(html,'lxml').find('div',{'class':'rprt_all'}).find('div',{'class':'afflist'}).find_all('li')
    except:
        afflist=[]
    author_infor=''
    for li in afflist:
        author_infor+=li.get_text().replace('\r','').replace('\n','')+'\n'
    item['author_infor']=author_infor
    return item

def write_to_excel(result):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for item in result:
        sheet.append([item['title'],item['url'],item['author_infor']])
    timenow=time.strftime('%Y%m%d_%H%M%S')
    excel.save(timenow+'.xlsx')

def main():
    journal='Angewandte Chemie (International ed. in English)'
    date_from='2015/12/31'
    date_to='2016/01/10'
    term=get_term(journal=journal,date_from=date_from,date_to=date_to)
    urls=get_urls(term)
    result=[]
    for url in urls:
        try:
            item=get_infor(url)
        except:
            print(url['title'],'failed')
            continue
        result.append(item)
        print(item['title'],'ok')
        time.sleep(1)
    write_to_excel(result)

main()
