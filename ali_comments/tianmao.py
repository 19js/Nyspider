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
            'Cookie':"isg=54E6C4202C463F733AA0851CEF5460A5; l=AgYG/70OSdHqxy51IJ/0Om7ydvaLEUp6; cna=7Dd0DgMB+HcCAXrNCByTSHxR; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; t=1e6dd9b5d55aacb2ca5e07cb5be03a2b; uc3=nk2=1pCplIlkFn7n&id2=WvAz2mB1qeE%2F&vt3=F8dASMh93v8JH66milo%3D&lg2=W5iHLLyFOGW7aA%3D%3D; tracknick=%5Cu98A0%5Cu6C9B%5Cu4E4B%5Cu590F3; lgc=%5Cu98A0%5Cu6C9B%5Cu4E4B%5Cu590F3; cookie2=1cdef8cc85ef4b19772fd48de808f9c0; _tb_token_=0BF8LVbNvUzT; JSESSIONID=O91N37$Dld004lRG; tmallrateweb0=kFRcK6prBN%2FIWAPFgzdiHk6piSznQhr1I7CcH54OBBPAikp5PPqjJoPi6hHymxtvOdNEq6XWR2avirwX8x9xJVXYrWE5HeupUMAxP5btA4pwpgm%2Fx0qwL6N4QhvZznJjNru99fxhM11qN89iHmSEaNzoyKEg9n83vWEX1J09WyoTE%2BF0zrsaYE0Kxku5XobfQ00lE3AUbJ84kanO8KDLTfeqecWQmNFkmdv44KxHAY9piKJowYEwjEkRTP2XYxf8hj7BGzEQwH%2B%2BJfsebT9uPlRHisMEwqGofq11NwhHKhOW8vMHp%2FbfmTtMfiQ5shj0X3I%2BVXW0MyhsxTUMpgWWAQ%3D%3D; hng=CN%7Czh-cn%7CCHN",
            'Connection': 'keep-alive'}
        self.count=0
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        self.url='https://rate.tmall.com/list_detail_rate.htm?itemId=40719897239&spuId=292309125&sellerId=194215397&order=3&append=0&content=1&tagId=&posi=&picture=&ua=176UW5TcyMNYQwiAiwTR3tCf0J%2FQnhEcUpkMmQ%3D|Um5OcktySnZOe0Z9R39Eeiw%3D|U2xMHDJ%2BH2QJZwBxX39RaFR6WnQyUzVJOBZAFg%3D%3D|VGhXd1llXGVdYVlsUWpQaFNtWmdFfUV8QXxAe0V5THNKf0RxTmA2|VWldfS0QMA86ACAcJQUrFDJPJhYmSHdMbVJ3BXpUAlQ%3D|VmhIGCQbIAA%2FBDwcIBsiHDwFOQc4GCQQLxIyDjMGOxsnEywRMQ0wCDZgNg%3D%3D|V29PHzEfP29UbFNzT3NNdVVuU2lLc1NrVW9NcEtwS3NOcER5Qn1FZVlmWXlFfCoKNxc5FzcPOw9ZDw%3D%3D|WGFBET8RMQozDCwQLBMmBjoGPgtdCw%3D%3D|WWBAED4QMAs%2FBCQYIBggAD4GOANVAw%3D%3D|WmNDEz19KXAdYgNuEGpEZF9rU3NPdE10VG9bYVQCVA%3D%3D|W2JCEjwSMgg1CysXLBMoCDwJNw1bDQ%3D%3D|XGVFFTsVNQ8yDCwSJx4kBDgCOAQ5bzk%3D|XWZGFjgWNgo1CysWNgo%2FBDsOWA4%3D|XmdHFzkXNwM3CysVIRwkBDgMOAc%2FaT8%3D|X2dHFzkXN2dbZlpnR3lNc09vW25XdU1tVW1ScE12TXZOc015RH9AeFhmXHxCdiAAPR0zHT0CPwY%2FClwK|QHlEeVlkRHtbZ15iQnxEfl5nR3tPb1t7Tm5UdE9vV3dIcVFvT3NPGQ%3D%3D&isg=6D20A05EBD8D55C9B24CEECE9E00CEA9&_thwlang=zh_CN%3ATB-GBK&_ksTS=1445158088159_3877&callback=jsonp3878&currentPage='
    def run(self):
        cert='/home/nyloner/work/ali_comments/cert.pem'
        for page in range(80):
            html=requests.get(self.url+str(page+1),headers=self.headers,verify=False).text
            print(html)
            rel='ontent":"(.*?)"'
            comments=re.findall(rel,html)
            for item in comments:
                self.sheet.write(self.count,0,item)
                self.count+=1
            self.f.save('相机.xls')
            print(self.count)

work=Get_comments()
work.run()
