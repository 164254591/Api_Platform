from django.test import TestCase

# Create your tests here.
def a():
    return 500
def b():
    return 800
def m():
    y = 'b'
    x = locals()
    exec('x=%s()'%y)
    print(x['x'])
    print(x)
m()