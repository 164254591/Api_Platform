import json

from django.test import TestCase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Create your tests here.
def a():
    return 500


def b():
    return 800


def m():
    y = 'b'
    c = '5'
    x = locals()

    exec('x=%s()' % y)
    # print(x['x'])
    # print(x)


m()

A = '{"a": "22", "b": {"c": "001", "d": "02"}}'
B = "['d']['c']"
C = eval('{"a": "22", "b": {"c": "001", "d": "02"}}' + "['b']['c']")
# print(C)

# print(str(A))
# d = json.loads(str(A))
# print(d['b']['c'])


# import numpy as np
list1=[]
list2 = [5, 5, 5, 8, 8, 9, 1]
for i in list2:
    if i == 8:
        list1.append(i)
        list2.remove(i)
        # print(list2)

# def num(lis):
#     lis = np.array(lis)
#     key = np.unique(lis)
#     result = {}
#     for k in key:
#         mask = (lis == k)
#         list_new = lis[mask]
#         v = list_new.size
#         result[k] = v
#     return result


# print(num(list2))

v = 'aaa= select name from table where name ="dlz"'
d = v.split('=',1)
right = '='.join(v.split('=')[1:]).strip()
# print(d)
# print(right)

import time
print(time.time())
print(int(time.time() - time.timezone)% 86400)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time() - time.timezone))))
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time() - time.timezone)% 86400)))
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time() - int(time.time() - time.timezone) % 86400))))
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

def email(adresss, content):
    adresss = '164254591@qq.com'
    mail_to = adresss.split(',')
    mail_to =['164254591@qq.com','1343311617@qq.com ']
    mail_to = ','.join(mail_to)
    mail_host = 'smtp.qq.com'
    mail_user = '164254591@qq.com'  # 发送者邮箱地址
    mail_pass = 'nfsesqiwyzjacafj'  # smtp授权码

    c = MIMEText(content, 'html', 'utf-8')
    msg = MIMEMultipart('related')
    msg['From'] = mail_user
    msg['To'] = mail_to
    msg['Subject'] = '接口测试平台线上监控报告'
    msg.attach(c)

    # try:
    server = smtplib.SMTP()
    server.connect(mail_host, 25)
    server.login(mail_user, mail_pass)
    server.sendmail(mail_user, str(mail_to), msg.as_string())
    print('发送邮件成功')
    server.close()
    # except:
    #     print('邮件发送失败')
email('164254591@qq.com','dddddd')
# print(time.localtime(time.time()))



