import requests
import xlwt3
from bs4 import BeautifulSoup
import datetime

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}


def personInfor(url):
    html=requests.get(url,headers=headers,timeout=50).text.encode('ISO-8859-1').decode('utf-8','ignore')
    soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'user_homepage_nav clearfix'})
    left=soup.find('div',attrs={'class':'my-f-left left_user_nav  fl'}).find('ul').find_all('li')
    userinfor=''
    lists=[]
    for item in left[1].find_all('p'):
        userinfor+='|'+item.get_text().replace(' ','').replace('\r','').replace('\n','')
    return userinfor

def loaninfor(url):
    html=requests.get(url,headers=headers).text
    soup=BeautifulSoup(html,'lxml').find('div',attrs={'class':'wrapNewLendDetailInfoLeft'})
    infor=soup.find('div',attrs={'class':'newLendDetailInfoLeft'})
    biao_table=soup.find('div',attrs={'class':'newLendDetailMoneyLeft'}).find_all('dl')
    jin_table=soup.find('div',attrs={'class':'newLendDetailRefundLeft'}).find_all('div',attrs={'class':'part'})[1].find_all('div')
    text=infor.find('a',attrs={'class':'username'}).get_text()+'|'+infor.find('a',attrs={'class':'altQust'}).find('span').get('class')[-1]
    url=infor.find('a').get('href')
    userinfor=personInfor(url)
    text+='|'+userinfor
    for i in biao_table:
        text+='|'+i.get_text().replace('\r','').replace('\n','').replace(' ','')
    for i in jin_table:
        text+='|'+i.get_text().replace('\r','').replace('\n','').replace(' ','')
    history=[]
    try:
        lendDetail=BeautifulSoup(html,'lxml').find('div',attrs={'class':'lendDetailTab_divContent_Div'}).find_all('ol')
        for item in lendDetail:
            lis=item.find_all('li')
            lend=''
            lend+=lis[2].get_text()
            lend+='-'+lis[3].get_text()
            history.append(lend)
    except:
        pass
    return text+'|'+str(history)

def geturls(url):
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'wapBorrowList clearfix'}).find_all('li')
    result=[]
    for li in table:
        a=li.find('a',attrs={'class':['title','ell']})
        text=a.get('title')+'|'+a.get('href')
        if '新手体验-模拟投资' in text:
            continue
        result.append(text)
    if result==[]:
        return result[1]
    return result

def calculate_time(time1,time2):
    t1=datetime.datetime.strptime(time1,'%Y/%m/%d %H:%M:%S')
    t2=datetime.datetime.strptime(time2,'%Y/%m/%d %H:%M:%S')
    result=((t1-t2).seconds)/60
    print(time1,time2,result)
    return result

def main():
    pageurls=['http://invest.ppdai.com/loan/list_safe_s0_ppage?Rate=0','http://invest.ppdai.com/loan/list_riskmiddle_s0_ppage?Rate=0','http://invest.ppdai.com/loan/list_riskhigh_s0_ppage?Rate=0']
    labels=['新手收益区','中风险收益区','高风险收益区']
    excel=xlwt3.Workbook()
    for index in range(len(pageurls)):
        sheet=excel.add_sheet(labels[index])
        count=0
        pageurl=pageurls[index]
        for page in range(1,100):
            try:
                urls=geturls(pageurl.replace('page',str(page)))
            except:
                break
            for url in urls:
                try:
                    loan=loaninfor(url.split('|')[-1])
                except:
                    continue
                result=[]
                result.append(url.split('|')[0])
                lists=loan.split('|')
                result.append(lists[1])
                result.append(lists[3].replace('借入信用：',''))
                result.append(lists[5].replace('借款金额：',''))
                result.append(lists[6].replace('年利率：',''))
                result.append(lists[7].replace('期限：',''))
                result.append(lists[8].replace('进度条：',''))
                history=eval(lists[-1])
                if history==[]:
                    continue
                sum=0
                for index_hi in range(len(history)-1):
                    try:
                        sum+=calculate_time(history[index_hi].split('-')[1],history[index_hi+1].split('-')[1])
                    except:
                        continue
                try:
                    diff=sum/(len(history)-1)
                except:
                    continue
                for item in history:
                     num=0
                     for i in result:
                         sheet.write(count,num,i)
                         num+=1
                     sheet.write(count,num,item.split('-')[0])
                     sheet.write(count,num+1,item.split('-')[1])
                     sheet.write(count,num+2,diff)
                     count+=1
                excel.save('result.xls')
            print(labels[index],'--',page,'--ok')

main()
