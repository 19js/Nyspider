#coding:utf-8

import requests
import xlwt3
import re
import requests
requests.packages.urllib3.disable_warnings()

class Get_comments(object):
    """docstring for Get_comments"""
    def __init__(self):
        super(Get_comments, self).__init__()
        self.f=xlwt3.Workbook()
        self.sheet=self.f.add_sheet('sheet')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Cookie':"isg=1895AE3ACA648D8B28455A6D1992F41F; l=AvX1ovPGHd3jI30I58r3v3IcJXuvcqmE; t=1e6dd9b5d55aacb2ca5e07cb5be03a2b; thw=cn; cna=7Dd0DgMB+HcCAXrNCByTSHxR; uc3=nk2=1pCplIlkFn7n&id2=WvAz2mB1qeE%2F&vt3=F8dASMh%2Fnu8OGgfEtGM%3D&lg2=URm48syIIVrSKA%3D%3D; tracknick=%5Cu98A0%5Cu6C9B%5Cu4E4B%5Cu590F3; _cc_=URm48syIZQ%3D%3D; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; mt=np=&ci=-1_0&cyk=0_0; ali_ab=211.69.194.131.1444291484725.8; lgc=%5Cu98A0%5Cu6C9B%5Cu4E4B%5Cu590F3; lzstat_uv=13179738183169067975|3492151@3600092@3288243@3260534; v=0; cookie2=1cdef8cc85ef4b19772fd48de808f9c0; _tb_token_=0BF8LVbNvUzT; uc1=cookie14=UoWzXLHAxnd7aw%3D%3D&existShop=true&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=WqG3DMC9Edo1SB5NB6Qtng%3D%3D&tag=2&cookie15=W5iHLLyFOGW7aA%3D%3D&pas=0; hng=CN%7Czh-cn%7CCHN; existShop=MTQ0NTE1NzMzOQ%3D%3D; sg=343; cookie1=BYTvDkInmXl2wO%2F6AW0tX%2Bpb6nHX4a5Olly%2Fg4DvWfE%3D; unb=907324234; skt=ae45361e45082d58; publishItemObj=Ng%3D%3D; _l_g_=Ug%3D%3D; _nk_=%5Cu98A0%5Cu6C9B%5Cu4E4B%5Cu590F3; cookie17=WvAz2mB1qeE%2F",
            'Connection': 'keep-alive'}
        self.count=0
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        self.url='https://rate.taobao.com/feedRateList.htm?callback=jsonp_reviews_list&userNumId=84131819&auctionNumId=6774286903&siteID=3&rateType=&orderType=sort_weight&showContent=1&attribute=&currentPageNum='
    def run(self):
        cert='/home/nyloner/work/ali_comments/cert.pem'
        for page in range(80):
            html=requests.get(self.url+str(page+1),headers=self.headers,verify=False).text
            print(html)
            rel='content":"(.*?)"'
            comments=re.findall(rel,html)
            for item in comments:
                self.sheet.write(self.count,0,item)
                self.count+=1
            self.f.save('麻辣花生.xls')
            print(self.count)

work=Get_comments()
work.run()
