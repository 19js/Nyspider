import requests
import json
import openpyxl
import time
from bs4 import BeautifulSoup

headers = {
    'Host':"www.jisilu.cn",
    'Accept':"application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    'Content-Type':"application/x-www-form-urlencoded; charset=UTF-8",
    'X-Requested-With':"XMLHttpRequest",
    'Cookie':"kbzw__Session=4sv8h9vjir144ijdh02h4nefd0; Hm_lvt_164fe01b1433a19b507595a43bf58262=1468934580; Hm_lpvt_164fe01b1433a19b507595a43bf58262=1468935752; kbz_newcookie=1; kbzw__user_login=7Obd08_P1ebax9aX5dvi0OXc5ZmcndHV7Ojg6N7bwNOM2KjZqpmgw6feqM6upamTqJmt3KbbkaKU17HXoNql2ZiXnKTs3Ny_zYylr6qgspyYnaO2uNXQo67f293l4cqooaWSlonPqKSzgcXD6efp3rSMw8vk1u-X67CXz5eotJXb76arlqSRoJe63cTb0KOrpZqpnKiSp4G94OXdx9_Zo62pl6k.",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

def login():
    logindata=open('user','r',encoding='utf-8').read().replace('\r','').replace('\n','')
    logindata=eval(logindata)
    data={
    'user_name':logindata['user_name'],
    'password':logindata['password'],
    'net_auto_login':1,
    '_post_type':'ajax',
    'return_url':'https://www.jisilu.cn'
    }
    session=requests.session()
    session.post('https://www.jisilu.cn/account/ajax/login_process/',data=data).text
    return session

def get_A(session):
    data={
    'is_funda_search':"0",
    'fundavolume':"100",
    'maturity':"",
    'amarket':["sh",'sz'],
    'coupon_descr':["+3.0%",'+3.2%','+3.5%','+4.0%','other'],
    'rp':"50",
    'page':'1'
    }
    timestr=str(time.time()).replace('.','')
    html=session.post('https://www.jisilu.cn/data/sfnew/funda_list/?___t=%s'%(timestr),data=data).text
    data=json.loads(html)['rows']
    result=[]
    keys=['funda_id','funda_name','funda_current_price','funda_increase_rt','funda_volume','funda_value'
        ,'funda_discount_rt','coupon_descr_s','funda_coupon','funda_coupon_next','funda_profit_rt_next','funda_left_year'
        ,'funda_index_name','funda_index_increase_rt','funda_lower_recalc_rt','lower_recalc_profit_rt'
        ,'fundb_upper_recalc_rt','funda_base_est_dis_rt','funda_base_est_dis_rt_t1','funda_base_est_dis_rt_t2'
        ,'funda_amount','funda_amount_increase','abrate','next_recalc_dt']
    for item in data:
        item=item['cell']
        line=[]
        for key in keys:
            if key=='next_recalc_dt':
                try:
                    value=BeautifulSoup(item[key],'html.parser').get_text()
                except:
                    value=item[key]
                line.append(value)
                continue
            try:
                line.append(item[key])
            except:
                line.append('')
        result.append(line)
    return result

def get_B(session):
    data={
    'rp':"50",
    'page':'1'
    }
    timestr=str(time.time()).replace('.','')
    html=session.post('https://www.jisilu.cn/data/sfnew/fundb_list/?___t=%s'%(timestr),data=data).text
    data=json.loads(html)['rows']
    result=[]
    keys=['fundb_id','fundb_name','fundb_current_price','fundb_increase_rt','fundb_volume','b_est_val'
        ,'fundb_value','fundb_discount_rt','fundb_left_year','coupon_descr_s','fundb_price_leverage_rt'
        ,'fundb_net_leverage_rt','fundb_capital_rasising_rt','fundb_index_name','fundb_index_increase_rt'
        ,'fundb_lower_recalc_rt','fundb_upper_recalc_rt','fundb_base_est_dis_rt','abrate','fundm_value']
    for item in data:
        item=item['cell']
        line=[]
        for key in keys:
            try:
                line.append(item[key])
            except:
                line.append('')
        result.append(line)
    return result

def get_M(session):
    data={
    'rp':"50",
    'page':'1'
    }
    timestr=str(time.time()).replace('.','')
    html=session.post('https://www.jisilu.cn/data/sfnew/fundm_list/?___t=%s'%(timestr),data=data).text
    data=json.loads(html)['rows']
    result=[]
    keys=['base_fund_id','base_fund_nm','price','last_chg_dt','index_nm','upper_recalc_price'
        ,'lower_recalc_price','issue_dt','maturity_dt','fundA_id','fundA_nm'
        ,'coupon','coupon_next','coupon_descr_s','fundB_id'
        ,'fundB_nm','abrate','base_est_dis_rt','fund_company_nm']
    for item in data:
        item=item['cell']
        line=[]
        for key in keys:
            try:
                line.append(item[key])
            except:
                line.append('')
        result.append(line)
    return result

def get_F(session):
    data={
    'is_search':"0",
    'avolume':"100",
    'bvolume':"100",
    'market':["sh","sz"],
    'ptype':"price",
    'rp':"50",
    'page':"1"
    }
    timestr=str(time.time()).replace('.','')
    html=session.post('https://www.jisilu.cn/data/sfnew/arbitrage_vip_list/?___t=%s'%timestr,data=data).text
    data=json.loads(html)['rows']
    result=[]
    keys=['fundA_id','fundA_nm','sell1A','increase_rtA','fundA_volume','fundA_amount_increase',
        'fundB_id','fundB_nm','sell1B','increase_rtB','fundB_volume','fundB_amount_increase',
        'abrate','merge_price','est_dis_rt','base_fund_id','base_fund_nm','base_nav','base_est_val',
        'index_nm','idx_incr_rt','asset_ratio','asset_ratio_last','apply_fee','redeem_fee']
    for item in data:
        item=item['cell']
        line=[]
        for key in keys:
            try:
                line.append(item[key])
            except:
                line.append('')
        result.append(line)
    return result

def get_ETF(session):
    data={
    'rp':"50",
    'page':'1'
    }
    timestr=str(time.time()).replace('.','')
    html=session.post('https://www.jisilu.cn/jisiludata/etf.php?___t=%s'%(timestr),data=data).text
    data=json.loads(html)['rows']
    result=[]
    keys=['fund_id','fund_nm','price','increase_rt','volume','index_nm'
        ,'pe','pb','index_increase_rt','estimate_value','fund_nav'
        ,'nav_dt','discount_rt','creation_unit','amount'
        ,'unit_incr','unit_total']
    for item in data:
        item=item['cell']
        line=[]
        for key in keys:
            try:
                line.append(item[key])
            except:
                line.append('')
        result.append(line)
    return result

def write_to_excel():
    excel=openpyxl.Workbook(write_only=True)
    sheet=excel.create_sheet()
    for item in data:
        cell=[]
        for key in keys:
            try:
                cell.append(item['cell'][key])
            except:
                cell.append('-')
        sheet.append(cell)
    excel.save('result.xlsx')
