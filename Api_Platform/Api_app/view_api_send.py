# from django.shortcuts import render
# from Api_app.models import *
# import time
# from django.contrib import auth
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404
# import json
import json
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
        """生成返回头、返回码等数据"""
        self.RD = ''
        self.RD += '\n[%s]:%s\n' % ('status_code', self.response.status_code)
        self.RD += '\n[%s]:%s\n' % ('header', self.response.headers)

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

        elif self.api['payload_method'] == 'raw':
            if self.api['payload_raw_method'] == 'Text':
                self.headers['Content-Type'] = 'text/plain'
            elif self.api['payload_raw_method'] == 'JavaScript':
                self.headers['Content-Type'] = 'application/javascript'
            elif self.api['payload_raw_method'] == 'JSON':
                self.headers['Content-Type'] = 'application/json'
            elif self.api['payload_raw_method'] == 'XML':
                self.headers['Content-Type'] = 'application/xml'
            elif self.api['payload_raw_method'] == 'HTML':
                self.headers['Content-Type'] = 'text/html'
            self.response = requests.request(self.method, self.url, headers=self.headers, data=self.api['payload_raw'])
        elif self.api['payload_method'] == 'binary':
            ...
        elif self.api['payload_method'] == 'GraphQL':
            self.headers['Content-Type'] = 'application/json'
            payload = json.dumps({"query": self.api['payload_GQL_q'], "variables": eval(self.api['payload_GQL_q'])})
            self.response = requests.request(self.method, self.url, headers=self.headers, data=payload)
        try:
            self.R = json.dumps(self.response.json(), ensure_ascii=False)  # 防止中文乱码
        except:
            # 如果返回是字典，用text接受就会乱码
            self.R = self.response.text

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
