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

logger = logging.getLogger('django')


# --------------------------------------文件作用：发送接口请求
class SENDAPI():
    def __init__(self, api):
        self.api = api

    def make_url(self):
        """拼接url"""

    def make_header(self):
        """请求头"""

    def make_method(self):
        """整理成标准的请求头格式"""

    def make_RD(self):
        """生成返回头等数据"""

    def do_configure(self, configure):
        """执行配置函数"""
        print(configure['label'])

    def send(self):
        """执行接口"""

    def index(self):
        """入口函数"""
        children = self.api['children']
        print(children)
        for i in children:
            if i['do_time'] == 'before':
                self.do_configure(i)
                children.remove(i)
        self.send()
        for i in children:
            self.do_configure(i)
        return self.response_data()

    def response_data(self):
        ...
