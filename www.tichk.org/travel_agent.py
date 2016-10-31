import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import string

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def agents():
    urls=[]
    for word in string.ascii_uppercase:
        url='http://www.tichk.org/public/website/b5/agents/%s.html'%word
        html=requests.get(url,headers=headers).text
        table=BeautifulSoup(html).find_all('a')
        for item in table:
            url=item.get('href')
            if 'detail' not in url:
                continue
            if url in urls:
                continue
            urls.append(url)
        time.sleep(1)
        print(word,'ok')
    return urls

def agent_infor_cn(url):
    url='http://www.tichk.org/public/website/b5/agents'+url.replace('./','/')
    html=requests.get(url,headers=headers).text
    name=BeautifulSoup(html).find('span',{'class':'style12'}).get_text()
    table=BeautifulSoup(html).find_all('tr',{'bgcolor':'#F3F3F3'})
    table+=BeautifulSoup(html).find_all('tr',{'bgcolor':'#FCFCFC'})
    result={'cnname':name}
    for item in table:
        try:
            key=item.find('td').get_text()
            value=item.find_all('td')[-1].get_text()
            result[key]=value
        except:
            continue
    return result


def agent_infor_en(url):
    url='http://www.tichk.org/public/website/en/agents'+url.replace('./','/')
    html=requests.get(url,headers=headers).text
    name=BeautifulSoup(html).find('span',{'class':'style12'}).get_text()
    table=BeautifulSoup(html).find_all('tr',{'bgcolor':'#F3F3F3'})
    table+=BeautifulSoup(html).find_all('tr',{'bgcolor':'#FCFCFC'})
    result={'enname':name}
    for item in table:
        try:
            key=item.find('td').get_text()
            value=item.find_all('td')[-1].get_text()
            result[key]=value
        except:
            continue
    return result

def write_to_excel(result):
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for line in result:
        sheet.append(line)
    excel.save('result.xlsx')

def main():
    urls=agents()
    cnkeys=['cnname','牌照號碼','營業名稱','地址','電話','傳真','網址','電郵','所屬屬會','會籍類別']
    cnkeys_2=['旅行團 (零售)','旅行團 (批發 / 組團社)','票務 (零售)','票務 (批發)','機票加酒店套餐','商務旅遊','會議、展覽及獎勵旅遊','代訂酒店','郵輪假期','長線 (例如：美洲 / 歐洲 / 非洲 / 澳紐)', '日本 / 韓國 / 東南亞 / 印度', '中國內地 / 台灣', '本地遊旅行團 / 租車 / 為本地人預訂本地酒店','國家旅遊局確認香港遊接待社 (須經議會向國家旅遊局申請)']
    en_keys=['enname','Licence No.','Trade Name','Address','Tel.','Fax','Website','Email','Association Membership','Membership Type']
    en_keys_2=['Package Tour (Retail)', 'Package Tour (Wholesale / Tour Operator)', 'Ticketing (Retail)', 'Ticketing (Wholesale)','Air-plus-hotel Packages',  'Corporate / Business Travel','MICE (Meetings, Incentives, Conventions and Exhibitions)', 'Cruise Package', 'Hotel Reservation','Local Tour / Car Hire / Hotel Booking for Locals', 'Longhaul (e.g.: America / Europe / Africa / Australia and New Zealand)', 'Mainland China / Taiwan', 'Japan / Korea / Southeast Asia / India', 'CNTA-endorsed Hong Kong Receiving Agent for Chinese Tours (Applications to CNTA via TIC needed)']
    result=[]
    result.append(en_keys+en_keys_2+cnkeys+cnkeys_2)
    for url in urls:
        try:
            item=agent_infor_en(url)
        except:
            failed=open('failed.txt','a',encoding='utf-8')
            failed.write(url+'\n')
            failed.close()
            continue
        line=[]
        for key in en_keys:
            try:
                line.append(item[key])
            except:
                line.append('')
        for key in en_keys_2:
            if key in item:
                line.append('*')
            else:
                line.append('')
        try:
            item=agent_infor_cn(url)
        except:
            failed=open('failed.txt','a',encoding='utf-8')
            failed.write(url+'\n')
            failed.close()
            continue
        for key in cnkeys:
            try:
                line.append(item[key])
            except:
                line.append('')
        for key in cnkeys_2:
            if key in item:
                line.append('*')
            else:
                line.append('')
        result.append(line)
        try:
            print(line)
        except:
            continue
        time.sleep(0.2)
    write_to_excel(result)

main()
