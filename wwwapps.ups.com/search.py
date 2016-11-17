import requests
from bs4 import BeautifulSoup
import threading
import time

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def search(fromcode,tocode):
    data={
    'timeOnlyRts':'false',
    'ctcModAccountFlag':'show',
    'addressDiffFromBook':'NO',
    'page':'shipping/wwdt/tim(1ent).html',
    'loc':'en_US',
    'accImsFlag':'false',
    'mypacking':'My Packaging',
    'upsletter':'UPS Letter',
    'expressbox':'UPS Express Box',
    'smallbox':'UPS Express Box - Small',
    'mediumbox':'UPS Express Box - Medium',
    'largebox':'UPS Express Box - Large',
    'tube':'UPS Tube',
    'pack':'UPS Pak',
    'tenkg':'UPS Worldwide Express 10KG Box',
    'twentyfivekg':'UPS Worldwide Express 25KG Box',
    'palletPkgType':'Pallet',
    'timeOnlyCountries':'AS,AD,AI,AG,AM,AW,BB,BY,BZ,BJ,BT,BW,VG,BN,BF,KH,CV,CF,TD,CG,CK,DM,GQ,ER,FO,FJ,GF,PF,GA,GM,GE,GL,GD,GP,GU,GN,GW,GY,HT,IS,JM,KI,LA,LB,LS,LR,LI,MK,MG,MV,ML,MH,MQ,MR,FM,MC,MN,MS,MP,ME,NA,NP,AN,NC,NE,NF,PW,PG,RE,SM,SN,SC,SL,SB,KN,LC,VC,SR,SZ,SY,TJ,TG,TO,TT,TC,TV,UA,UZ,VU,WF,WS,YE',
    'isOrigDestDutiable':'false',
    'quoteselected':'none',
    'fromCountryChange':'init',
    'toCountryChange':'init',
    'preferenceaddresskey':000,
    'palletselected':0,
    'ddoPref':'false',
    'pickupSupportIndicator':'true',
    'countriesToCheckDropOffLocations':'false',
    'countriesSupportingPickupsDomestic':'US,PR',
    'inTranslation':'inches',
    'cmTranslation':'cm.',
    'lbsTranslation':'lbs.',
    'kgsTranslation':'kgs.',
    'weightTranslation':'Weight',
    'widthTranslation':'Width',
    'heightTranslation':'Height',
    'quoteType':'transitTimeOnly',
    'origCountry':'US',
    'origCity':'',
    'origPostal':fromcode,
    'origLocale':'en_US',
    'origRIFClient':'CTC',
    'shipmentType':'smallPkg',
    'destCountry':'US',
    'destCity':'',
    'destPostal':tocode,
    'destLocale':'en_US',
    'destRIFClient':'CTC',
    'shipDate':'2016-11-21',
    'currencyUnits':'USD',
    'weight':1,
    'weightType':'LBS',
    'diUnit':'IN',
    'shipWeightUnit':'LBS',
    'WT.svl':'Footer',
    'emailAddress':'Enter e-mail address'
    }
    html=requests.post('https://wwwapps.ups.com/ctc/request',data=data,headers=headers,timeout=30).text
    f=open('html.html','w')
    f.write(html)
    f.close()
    soup=BeautifulSoup(html,'lxml').find('table',{'class':'dataTable'}).find_all('tr')
    for tr in soup:
        if 'UPS Ground' in str(tr):
            spans=tr.find_all('span',{'class':'label'})
            for span in spans:
                if 'Days In Transit' in str(span):
                    day=span.find('strong').get_text()
                    return day

    return False


def deal():
    codes=[line.replace('\n','').replace(' ','') for line in open('data','r')]
    length=len(codes)
    f=open('codes.txt','w')
    for index in range(length):
        code=codes[index]
        if len(code)==4:
            code='0'+code
        try:
            for another in codes[index+1:]:
                if len(another)==4:
                    another='0'+another
                f.write("%s-%s"%(code,another)+'\n')
        except:
            continue
    f.close()

class GetDay(threading.Thread):
    def __init__(self,fromcode,tocode):
        super(GetDay,self).__init__()
        self.fromcode=fromcode
        self.tocode=tocode

    def run(self):
        self.flag=True
        try:
            self.day=search(self.fromcode,self.tocode)
            if self.day==False:
                self.flag=False
        except:
            self.flag=False


def main():
    codes=[line.replace('\n','').split('-') for line in open('codes.txt','r')]
    num=0
    while len(codes):
        threadings=[]
        count=0
        while count<10:
            try:
                code=codes.pop(0)
                num+=1
                work=GetDay(code[0],code[1])
                work.setDaemon(True)
                threadings.append(work)
                count+=1
            except:
                break
        for work in threadings:
            work.start()
        for work in threadings:
            work.join()
        f_result=open('result.txt','a')
        for work in threadings:
            if work.flag==False:
                f=open('failed.txt','a')
                f.write('%s-%s\n'%(work.fromcode,work.tocode))
                f.close()
                continue
            f_result.write("%s-%s-%s\n"%(work.fromcode,work.tocode,work.day))
        f_result.close()
        print(num)

main()
