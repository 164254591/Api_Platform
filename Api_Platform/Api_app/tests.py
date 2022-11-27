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
list1 = []
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
d = v.split('=', 1)
right = '='.join(v.split('=')[1:]).strip()
# print(d)
# print(right)

import time

print(time.time())
print(int(time.time() - time.timezone) % 86400)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time() - time.timezone))))
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time() - time.timezone) % 86400)))
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time() - int(time.time() - time.timezone) % 86400))))
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

a = {'A': 'b',
     "B": 'code',
     "C":'33'
     }
print(a.get('A3',''))
