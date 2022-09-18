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
    # new_api.children = str(
    #     [{"do_time": "before", "type": "configure", "label": "仅运行", "method": "仅运行", "select": "", "value": "",
    #       "id": "%d_%d" % (new_api.id, 1)}])
    new_api.save()
    return get_apis(request)


def remove_ac(request):
    id = request.GET['id']
    if '_' in id:
        apis_id = id.split('_')[0]
        api = DB_apis.objects.filter(id=apis_id)[0]
        children = eval(api.children)
        for i in children:
            if i['id'] == id:
                children.remove(i)
                break
        api.children = str(children)
        api.save()  # 修改完数据库内容需要保存

    else:
        DB_apis.objects.filter(id=id).delete()
    return get_apis(request)


# 增加配置
def add_configure(request):
    id = request.GET['id']  # 一定是接口的id
    api = DB_apis.objects.filter(id=id)[0]
    children = eval(api.children)
    # 因为排序后会将顺序打乱，新增时需要判断当前接口中最大配置id
    if children:
        seq = []
        for i in range(len(children)):
            seq.append(children[i]['id'])
        max = sorted(seq)[-1]
        cid = int(max.split('_')[1]) + 1
    else:
        cid = 1
    # cid = int(children[-1]['id'].split('_')[1]) + 1 if children else 1
    children.append({"do_time": "after", "type": "configure", "label": "新配置", "method": "", "select": "", "value": "",
                     "id": "%d_%d" % (int(id), cid)})
    api.children = str(children)
    api.save()
    return get_apis(request)


# 保存配置
def save_configure(request):
    configure = json.loads(request.body.decode('utf-8'))
    api_id = configure['id'].split('_')[0]
    api = DB_apis.objects.filter(id=api_id)[0]
    children = eval(api.children)
    for i in range(len(children)):
        if children[i]['id'] == configure['id']:
            children[i] = configure
            break
    else:
        children.append(configure)
    api.children = str(children)
    api.save()
    return HttpResponse('')


# 向上移动配置
def up_configure(request):
    configure_id = request.GET['configure_id']
    api = DB_apis.objects.filter(id=configure_id.split('_')[0])[0]
    children = eval(api.children)
    for i in range(len(children)):
        if children[i]['id'] == configure_id:
            if i > 0:
                children[i], children[i - 1] = children[i - 1], children[i]
                break
    api.children = str(children)
    api.save()
    return get_apis(request)


# 向下移动配置
def down_configure(request):
    configure_id = request.GET['configure_id']
    api = DB_apis.objects.filter(id=configure_id.split('_')[0])[0]
    children = eval(api.children)
    for i in range(len(children)):
        if children[i]['id'] == configure_id:
            if i < len(children) - 1:
                children[i], children[i + 1] = children[i + 1], children[i]
                break
    api.children = str(children)
    api.save()
    return get_apis(request)
