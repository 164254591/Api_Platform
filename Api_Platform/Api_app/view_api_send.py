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

    def index(self):
        """入口函数"""
        pass

    def response_data(self):
        ...
