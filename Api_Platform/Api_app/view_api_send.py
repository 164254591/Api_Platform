# from django.shortcuts import render
# from Api_app.models import *
# import time
# from django.contrib import auth
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404
# import json
import logging
import requests

logger = logging.getLogger('django')


# --------------------------------------文件作用：发送接口请求
class SENDAPI():
    def __init__(self, api):
        self.api = api
        print(api)
        self.make_url()
        self.make_header()
        self.make_method()

    def make_url(self):
        """拼接url"""
        host = self.api['host']
        path = self.api['path']
        params = self.api['params']
        # 列表推导式------高级用法
        self.url = host + path + '?' + '&'.join(["%s=%s" % (i['key'], i['value']) for i in params])
        print(self.url)

    def make_header(self):
        """请求头"""
        self.headers = {}
        for i in self.api['headers']:
            self.headers[i['key']] = i['value']
        print(self.headers)

    def make_method(self):
        """整理成标准的请求头格式"""
        self.method = self.api['method']

    def make_RD(self):
        """生成返回头等数据"""
        self.RD = ''

    def do_configure(self, configure):
        """执行配置函数"""
        print(configure['label'])
        self.CR.append('[%s]=%s' % (configure['label'], False))

    def send(self):
        """执行接口"""
        if self.api['payload_method'] == 'none':
            self.response = requests.request(self.method, self.url, headers=self.headers, data={})
        elif self.api['payload_method'] == 'form-data':  # {"a":1,"b":2}
            file = []
            payload = {}
            for i in self.api['payload_fd']:
                payload[i['key']] = i['value']
            self.response = requests.request(self.method, self.url, headers=self.headers, data=payload, files=file)
        elif self.api['payload_method'] == 'x-www-form-urlencode':  # a=1&b=2
            # payload = ''
            # for i in self.api['payload_xwfu']:
            #     payload += '%s=%s&' % (i['key'], i['value'])
            payload = '&'.join([('%s=%s' % (i['key'], i['value'])) for i in self.api['payload_xwfu']])
            self.headers['Content-type'] = 'application/x-www-form-urlencode'
            self.response = requests.request(self.method, self.url, headers=self.headers, data=payload)

    def index(self):
        """入口函数"""
        self.CR = []
        children = self.api['children']
        print(children)
        for i in children:
            if i['do_time'] == 'before':
                self.do_configure(i)
                children.remove(i)
        self.send()
        for i in children:
            self.do_configure(i)
        self.make_RD()
        self.CR = '\n'.join(self.CR)
        return self.response_data()

    def response_data(self):
        """获取返回结果"""""
        r = {"R": "", "RD": self.RD, "CR": self.CR}
        return r
