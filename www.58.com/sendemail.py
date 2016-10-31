import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import time


def sendmail():
    sender = 'xxx@qq.com'
    receivers = ['xxx@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("xxxx", 'utf-8')
    message['To'] =  Header("xxx@qq.com", 'utf-8')
    subject ='time.strftime("%Y-%m-%d %H:%M:%S")'
    message['Subject'] = Header(subject, 'utf-8')
    #邮件正文内容
    message.attach(MIMEText('time.strftime("%Y-%m-%d %H:%M:%S")', 'plain', 'utf-8'))
    att1 = MIMEText(open('result.xls', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="result.xls"'
    message.attach(att1)
    server=smtplib.SMTP_SSL('smtp.qq.com')
    server.ehlo('smtp.qq.com')
    server.login(sender,passwd)
    server.sendmail(sender, receivers, message.as_string())

sendmail()
