from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
import smtplib
import time

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def sendEmail(fromemail,passwd,toemail,subject,text):
    msg = MIMEText(text, 'html', 'utf-8')
    msg['Subject']=Header(subject, 'utf-8').encode()
    msg['From'] = _format_addr(fromemail)
    msg['To'] = _format_addr(toemail)
    server=smtplib.SMTP('smtp-mail.outlook.com',587)
    server.starttls()
    server.login(fromemail,passwd)
    server.sendmail(fromemail, [toemail], msg.as_string())
    server.quit()

def load_emails():
    f=open('./20160921.txt','r',encoding='utf-8').read()
    emails=[]
    for item in f.split('---'*8):
        try:
            lines=item.split('***'*4)
            subject=lines[0].replace('\r\n','')
            email=lines[1].replace('\r\n','').replace(' ','')
            text=lines[2]
            emails.append([email,subject,text])
        except:
            continue
    return emails

def main():
    fromemail=''
    passwd=''
    emails=load_emails()
    for i in range(13,20):
        email=emails[i]
        sendEmail(fromemail,passwd,email[0],email[1],email[2])
        time.sleep(2)
        print(email[1])
main()
