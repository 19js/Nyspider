import requests
import json
import datetime
import openpyxl
import re

ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

headers = {
    'Host':'piaofang.wepiao.com',
    'Referer':'https://piaofang.wepiao.com/?dateStart=2017-01-08&dateEnd=2017-01-08&scheduleState=day',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type':'application/json',
    'Cookie':'bid=92f29664cc5349e5aec882b20c154843; _ga=GA1.2.787255948.1484027508; sid=60a4b8317a114c44b42ff551d10917fd; _ga=GA1.3.649727203.1484027202; _wp_uid_=2268946e-7889-4506-a5a2-1c7eb3944e2d'}

def day_get(d):
    oneday = datetime.timedelta(days=1)
    day = d - oneday
    return day

def product_box_office(day):
    data={
    "movieFilter":{"showDateFrom":day,"showDateTo":day,"sortType":"desc"},
    "paging":{"pageSize":"30"},
    "lang":"cn"
    }
    html=requests.post('https://piaofang.wepiao.com/api/v1/index',data=json.dumps(data),headers=headers,timeout=30).text
    json_data=json.loads(html)
    nationalBoxOffice=json_data['nationalBoxOffice']
    json_data=json_data['movieBoxOffices']
    movies=[]
    keys=['movieId','movieName','showDate','productBoxOffice','productTotalBoxOffice','productBoxOfficeRate','productScheduleRate','productTicketSeatRate','releaseDate']
    for item in json_data:
        line=[]
        for key in keys:
            try:
                line.append(item[key])
            except:
                line.append('')
        line.append(nationalBoxOffice)
        movies.append(line)
    return movies

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    sheet.append(['movieId','movieName','showDate','productBoxOffice','productTotalBoxOffice','productBoxOfficeRate','productScheduleRate','productTicketSeatRate','releaseDate','nationalBoxOffice'])
    for line in open('./movies.txt','r'):
        line=ILLEGAL_CHARACTERS_RE.sub('',line)
        line=eval(line)
        sheet.append(line)
    excel.save('movies.xlsx')

if __name__=='__main__':
    day=datetime.datetime.now()
    day=day_get(day)
    while True:
        day_str=str(day).split(' ')[0]
        if day_str=='2014-01-01':
            break
        try:
            movies=product_box_office(day_str)
        except:
            print(day_str,'failed')
            continue
        f=open('movies.txt','a')
        for movie in movies:
            f.write(str(movie)+'\n')
        f.close()
        print(day_str,'ok')
        day=day_get(day)
