import json

from django.test import TestCase


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
print(C)

# print(str(A))
# d = json.loads(str(A))
# print(d['b']['c'])


import numpy as np

list2 = [5, 5, 5, 8, 8, 9, 1]


def num(lis):
    lis = np.array(lis)
    key = np.unique(lis)
    result = {}
    for k in key:
        mask = (lis == k)
        list_new = lis[mask]
        v = list_new.size
        result[k] = v
    return result


print(num(list2))
