import requests
import json


def get_location(address,city):
    url='http://api.map.baidu.com/place/v2/search?query=%s&region=%s&city_limit=true&output=json&ak=fh980b9Ga64S8bl8QblSC3kq'%(address,city)
    html=requests.get(url).text
    try:
        data=json.loads(html)['results'][0]['location']
    except:
        return ''
    lng=data['lng']
    lat=data['lat']
    return str(lng)+'|'+str(lat)

    
line=get_location('滨湖新区四川路与云谷路交口西北角','合肥')
