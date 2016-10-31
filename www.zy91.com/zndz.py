import requests
from bs4 import BeautifulSoup
import time
import base64
import openpyxl

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def symptomList(sex):
    data={
        'sex':sex,
        'age':22
    }
    html=requests.post('http://www.zy91.com/zyyy/intelligent/bodyList.html',data=data,headers=headers).text
    table=BeautifulSoup(html,'lxml').find('div',id='bwList').find_all('a')
    body_area=[]
    for item in table:
        name=item.get_text()
        value=item.get('id').replace('symptomList_','')
        area=[name,value]
        if area in body_area:
            continue
        body_area.append(area)
    for item in body_area:
        bodyid=item[-1]
        html=requests.get('http://www.zy91.com/zyyy/intelligent/symptomList.html?_=1477644249745&humanBodyId=%s&age=22&sex=%s'%(bodyid,sex),headers=headers).text
        table=BeautifulSoup(html,'lxml').find_all('a')
        f=open('%s_symptomList.txt'%sex,'a')
        for a in table:
            name=a.get('v')
            sym_id=a.get('id').replace('symptomName_','')
            f.write(str([item[0],name,sym_id])+'\n')
        f.close()
        print(item[0])

def questionOptionList(symptomid,sex,name):
    url='http://www.zy91.com/zyyy/intelligent/questionOptionList.html?id=%s&symptomName=%s&sex=%s'%(symptomid,base64.b64encode(name.encode('utf-8')).decode(),sex)
    html=requests.get(url,headers=headers).text
    try:
        table=BeautifulSoup(html,'lxml').find('div',id='questionOptionList').find_all('div',{'class':'wormanDisplay'})
    except:
        return ['']*10,[]
    names=['']*10
    idlist=[]
    for div in table:
        m=div.get('m')
        if m==None:
            continue
        index=int(div.get('id').replace('co_',''))-1
        name=div.get_text()
        names[index]+=name+' \n'
        idlist.append(m)
    return names,idlist

def possibleDisease(sex,idlist,symptomid):
    url='http://www.zy91.com/zyyy/intelligent/possibleDisease.html?sex=%s&age=22&symptomIdList=%s&questionPptionIdList=%s'%(sex,symptomid,','.join(idlist))
    html=requests.get(url,headers=headers).text
    table=BeautifulSoup(html,'lxml').find_all('div',{'class':'igresults'})
    result=[]
    for item in table:
        igresultli=item.find_all('div',{'class':'igresultli'})
        possible_disease=igresultli[0].get_text().replace('可能疾病','')
        room=igresultli[1].get_text().replace('推荐科室','')
        result+=[possible_disease,room]
    return result

def main():
    for sex in ['M','F']:
        excel=openpyxl.Workbook(write_only=True)
        sheet=excel.create_sheet()
        symptomList=[eval(line) for line in open('%s_symptomList.txt'%sex,'r',encoding='utf-8')]
        for line in symptomList:
            symptom=line[1]
            symptomid=line[-1]
            names,idlist=questionOptionList(symptomid,sex,symptom)
            result=possibleDisease(sex,idlist,symptomid)
            sheet.append(line+names+result)
            try:
                print(sex,line,'ok')
            except:
                pass
        excel.save('%s_possibleDisease.xlsx'%sex)
main()
