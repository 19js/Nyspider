#coding:utf-8

import requests
import xlwt3
from bs4 import BeautifulSoup
import socket
import re

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def get_urls(page):
    html=requests.get('http://www.watchseries.li/series/%s'%page,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('ul',attrs={'class':'listings'}).find_all('li',attrs={'class':'col-sm-6 col-xs-12'})
    '''
    提取li
    <li style="/*width:370px;*/ float:left; padding:5px 10px 5px 30px; margin:0; height:160px;" class="col-sm-6 col-xs-12">
                        <a href="/serie/Shining_Inheritance" title="Shining Inheritance" class="title-series"><b style="font-size:14px;">Shining Inheritance</b> (2009)</a>
                        <div class="_image_container tv" style="float:left; width:100px;">
                            <div class="mask">
                                <a href="/serie/Shining_Inheritance" title="Shining Inheritance">
                                    <img src="http://www.watchseries.li/thumbs/2009/7423-shining_inheritance.jpg" alt="Shining Inheritance" title="Shining Inheritance" style="width:90px; height:113px;">
                                </a>
                            </div>
                        </div>
                        <div class="info" style="float:left; width:240px;">
                            <div class="description" style="color:#666;">
                                    Go Eun Sung's life is similar to Cinderella's. After her father died, her step-mother, Baek Sung Hee, took away all of her assets and her yo
                            </div>
                            <ul class="tab_links" style="margin-top:4px;">
                                <li style="border:0; float:left;"><a href="/serie/Shining_Inheritance" class="more-info-links">
                                    <span class="fontPathway p15 fontnormal"><b>Show Summary</b></span></a>
                                </li>
                                <!--
                                <li style="border:0; float:left;">&nbsp;|&nbsp;</li>
                                <li style="border:0; float:left;">
                                    <a href="/episode/" class="more-info-links"><span class="fontPathway p15 fontnormal"><b>Latest Episode</b></span></a>
                                </li>
                                -->
                            </ul>
                        </div>
                    </li>
    '''
    urls=[]
    for li in table:
        try:
            a=li.find('a')
        except:
            continue
        if a==None:
            continue
        line=a.get('title')+'||http://www.watchseries.li'+a.get('href')
        '''
        提取标签 a
        <a href="/serie/Shining_Inheritance" title="Shining Inheritance" class="title-series"><b style="font-size:14px;">Shining Inheritance</b> (2009)</a>
        '''
        urls.append(line)
    return urls

def get_infor(url):
    html=requests.get(url,headers=headers).text
    url='http://www.watchseries.li'+BeautifulSoup(html,'lxml').find('div',attrs={'class':'latest-episode'}).find('center').find('a').get('href')
    '''
    获取链接
    <div class="latest-episode" style="font-size:15px; line-height:26px; border-bottom:1px solid #59789E; background-color:#EDEDED;">
				<center><strong>Latest Episode :</strong> <a href="/episode/future_worm__s1_e4.html">Season 1 Episode 4 Future Danny</a> (2015-06-22)</center>
			</div>
    '''
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('table',id='myTable').find_all('tr')
    '''
    <table id="myTable" style="border-collapse:collapse">
					<tbody>
							<tr class="download_link_allmyvideos.net" id="link_219">
							<td>
								<span>
									<img src="/images/hosts/allmyvideos.png" style="vertical-align: middle;" height="16px"> allmyvideos.net
																													<a href="#" class="showmore" hoster="allmyvideos.net" style="font-size:9px;" onclick="return false;">(Show more)</a>
																											</span>
							</td>
							<td>
								<a href="/link/219" class="buttonlink" target="_blank" title="allmyvideos.net" style="cursor:pointer;" onclick="$(this).css('color','#AE3939'); $(this).css('text-decoration','line-through');">Watch This Link!</a>
							</td>
							<td>
					</table>
    '''
    lists=[]
    for item in table:
        td=item.find('td')
        lists.append(re.sub('#\d+','',td.get_text().replace('(Show more)','').replace('\n','').replace('\t','').replace(' ','')))
    lists=list(set(lists))#去重
    return lists

def get_ip(lists):#获取ip
    ips=[]
    for url in lists:
        try:
            if url.startswith('www'):
                ip=socket.gethostbyname(url)
            else:
                ip = socket.gethostbyname('www.'+url)
        except:
            continue
        ips.append(url+'||'+ip)
    return ips

def main():
    pagefrom=int(input("Page From:"))
    pageto=int(input("Page To:"))
    f=xlwt3.Workbook()
    sheet=f.add_sheet('sheet')
    count=0
    number=0
    while pagefrom<=pageto:
        try:
            urls=get_urls(pagefrom)
        except:
            continue
        pagefrom+=1
        for url in urls:
            title=url.split('||')[0]
            try:
                lists=get_infor(url.split('||')[-1])
            except:
                sheet.write(count,0,title)
                count+=1
                continue
            ips=get_ip(lists)
            statue=0
            for item in ips:
                sheet.write(count,0,title)
                statue=1
                num=1
                for i in item.split('||'):
                    sheet.write(count,num,i)
                    num+=1
                count+=1
            if statue==0:
                sheet.write(count,0,title)
                count+=1
            number+=1
            print(number)
        f.save('data.xls')

main()
