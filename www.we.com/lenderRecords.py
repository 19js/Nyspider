#coding:utf-8
import json
import codecs
from util import *


def get_lender_records(loan_id):
    url='https://www.renrendai.com/pc/transfer/detail/loanInvestment?loanId={}'.format(loan_id)
    req=build_request(url)
    data=req.json()
    if 'status' in data and data['status']==0:
        result={
            'data':data['data'],
            'loanId':loan_id
        }
        return result
    return None

def crawl():
    id_from = 2121001
    id_to = 2486529
    for loan_id in range(int(id_from), int(id_to)+1):
        try:
            result=get_lender_records(loan_id)
        except:
            failed_f = codecs.open(
                './files/lender_failed.txt', 'a', encoding='utf-8')
            failed_f.write(str(loan_id)+'\n')
            failed_f.close()
            continue
        f = open('./files/lender_result', 'a')
        f.write(json.dumps(result)+'\n')
        f.close()
        print(loan_id,'OK')

crawl()
        
