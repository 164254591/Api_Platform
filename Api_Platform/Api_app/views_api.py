from django.shortcuts import render
from Api_app.models import *
import time
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
import logging

logger = logging.getLogger('django')


# ------------------------------------------------- 项目内的接口用例模块、视图逻辑层

# 获取接口和配置数据
def get_apis(request):
    project_id = request.GET['project_id']
    apis = list(DB_apis.objects.filter(project_id=project_id).values())
    for i in apis:
        i['children'] = eval(i['children'])
    return HttpResponse(json.dumps(apis), content_type='application/json')


# 获取项目默认选中的接口和配置列表
def get_dck(request):
    project_id = request.GET['project_id']
    dck = DB_project_list.objects.filter(id=project_id)[0].dck.split(',')
    return HttpResponse(json.dumps(dck), content_type='application/json')


# 设置选中列表dck
def set_dck(request):
    project_id = request.GET['project_id']
    dck = request.GET['dck']
    DB_project_list.objects.filter(id=project_id).update(dck=dck)
    return get_dck(request)


# 新增空白接口
def add_apis(request):
    project_id = request.GET['project_id']
    new_api = DB_apis.objects.create(project_id=project_id)
    new_api.children = str(
        [{"do_time": "before", "type": "configure", "label": "仅运行", "method": "only_play", "select": "", "value": "",
          "id": "%d_%d" % (new_api.id, 1)}])
    new_api.save()
    return get_apis(request)