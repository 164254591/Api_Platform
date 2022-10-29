from django.shortcuts import render
from Api_app.models import *
import time
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
# import sys
# sys.path.append("..")
import logging
from Api_app.view_api_send import SENDAPI

logger = logging.getLogger('django')


# ------------------------------------------------- 项目内的接口用例模块、视图逻辑层

# 获取接口和配置数据
def get_apis(request):
    project_id = request.GET['project_id']
    apis = list(DB_apis.objects.filter(project_id=project_id).values())
    for i in apis:
        i['children'] = eval(i['children'])
        i['params'] = eval(i['params'])
        i['headers'] = eval(i['headers'])
        i['payload_fd'] = eval(i['payload_fd'])
        i['payload_xwfu'] = eval(i['payload_xwfu'])
    return HttpResponse(json.dumps(apis), content_type='application/json')


# 获取项目默认选中的接口和配置列表
def get_dck(request):
    project_id = request.GET['project_id']
    dck = DB_project_list.objects.filter(id=int(project_id))[0].dck.split(',')
    return HttpResponse(json.dumps(dck), content_type='application/json')


# 设置选中列表dck
def set_dck(request):
    project_id = request.GET['project_id']
    dck = request.GET['dck']
    # print(dck)
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


# 接口上移
def up_api(request):
    # print('---' * 8)
    api_id = int(request.GET['api_id'])
    project_id = request.GET['project_id']
    all_api = DB_apis.objects.filter(project_id=project_id)
    # print(all_api)
    for i in range(len(all_api)):
        # print(all_api[i].id, api_id)
        if all_api[i].id == api_id:
            # print('1111')
            if i > 0:
                all_api[i].id, all_api[i - 1].id = all_api[i - 1].id, all_api[i].id
                children = eval(all_api[i].children)
                for j in range(len(children)):
                    old_cid = children[j]['id'].split('_')[1]
                    children[j]['id'] = "%d_%s" % (all_api[i].id, old_cid)
                all_api[i].children = str(children)

                children = eval(all_api[i - 1].children)
                for j in range(len(children)):
                    old_cid = children[j]['id'].split('_')[1]
                    children[j]['id'] = "%d_%s" % (all_api[i - 1].id, old_cid)
                all_api[i - 1].children = str(children)

                all_api[i].save()
                all_api[i - 1].save()
                break
    return get_apis(request)


# 接口下移
def down_api(request):
    api_id = int(request.GET['api_id'])
    project_id = request.GET['project_id']
    all_api = DB_apis.objects.filter(project_id=project_id)
    for i in range(len(all_api)):
        if all_api[i].id == api_id:
            if i < len(all_api) - 1:
                all_api[i].id, all_api[i + 1].id = all_api[i + 1].id, all_api[i].id
                children = eval(all_api[i].children)
                for j in range(len(children)):
                    old_cid = children[j]['id'].split('_')[1]
                    children[j]['id'] = "%d_%s" % (all_api[i].id, old_cid)
                all_api[i].children = str(children)

                children = eval(all_api[i + 1].children)
                for j in range(len(children)):
                    old_cid = children[j]['id'].split('_')[1]
                    children[j]['id'] = "%d_%s" % (all_api[i + 1].id, old_cid)
                all_api[i + 1].children = str(children)

                all_api[i].save()
                all_api[i + 1].save()
                break
    return get_apis(request)


# 保存接口
def save_api(request):
    api = json.loads(request.body.decode('utf-8'))
    DB_apis.objects.filter(id=api['id']).update(**api)
    return get_apis(request)


# 发送接口请求
def send_api(request):
    api = json.loads(request.body.decode('utf-8'))
    print(api)
    project_id = request.GET['project_id']
    s = SENDAPI(api, {}, api['children'])
    response_data = s.index()
    print(type(response_data))
    response_data = dict(response_data)
    print(response_data)
    return HttpResponse(json.dumps(response_data), content_type='application/json')


# 上传binary文件
def upload_binary_file(request):
    ApiID = request.GET['ApiID']
    file = request.FILES.get('binary_file', None)
    file_name = '%s_%s' % (ApiID, file)
    fp = open('Api_app/static/tmp/' + file_name, 'wb+')
    for i in file.chunks():
        fp.write(i)
    fp.close()
    DB_apis.objects.filter(id=int(ApiID)).update(payload_binary=file_name)
    return HttpResponse('')


# 上传fd文件
def upload_fd_file(request):
    ApiID = request.GET['ApiID']
    file = request.FILES.get('fd_file', None)
    file_name = '%s_%s' % (ApiID, file)
    fp = open('Api_app/static/tmp/' + file_name, 'wb+')
    for i in file.chunks():
        fp.write(i)
    fp.close()
    return HttpResponse('')


# 获取可用变量
def get_userable_par(request):
    api_id = request.GET['api_id']
    project_id = request.GET['project_id']
    res = ''
    apis = DB_apis.objects.filter(project_id=project_id, id__lt=int(api_id))
    # print(apis)
    for i in apis:
        children = eval(i.children)
        res += '【%s】:' % i.label
        for j in children:
            if j['method'] == '提取':
                res += j['value'] + ' '
        res += '\n'
    return HttpResponse(res)


# 获取正在执行的接口名
def doing_api(request):
    project_id = request.GET['project_id']
    doing_api = DB_project_list.objects.filter(id=int(project_id))[0].doing_api
    print('正在执行：'+str(doing_api))
    return HttpResponse(doing_api)


# 执行大用例
def run(request):
    project_id = request.GET['project_id']
    dck = request.GET['dck'].split(',')
    print(dck)
    TQ = {}
    # 生成新的报告
    report = DB_report.objects.create()
    report.project_id = project_id
    report.ctime = time.strftime("%Y-%m-%d %H:%M:%S")
    apis_result = []

    for i in range(len(dck)):
        if '_' not in dck[i]:  # 判断是否为接口还是配置
            need_children = []
            print(dck[i])
            for j in range(i + 1, len(dck)):
                if '%s_' % dck[i] in dck[j]:
                    need_children.append(dck[j])
                else:
                    break
            print(need_children)
            # 实际去请求该接口了
            api = DB_apis.objects.filter(id=int(dck[i])).values()[0]
            DB_project_list.objects.filter(id=int(project_id)).update(doing_api=api['label'])
            api['children'] = eval(api['children'])
            children = []
            for c in api['children']:
                if c['id'] in need_children:
                    children.append(c)
            api['params'] = eval(api['params'])
            api['headers'] = eval(api['headers'])
            api['payload_fd'] = eval(api['payload_fd'])
            api['payload_xwfu'] = eval(api['payload_xwfu'])
            # 调用类执行
            s = SENDAPI(api, TQ, children)
            response_data = s.index()
            TQ = response_data['TQ']
            apis_result.append(response_data['REPORT'])
            print('dlz22222')
            print(response_data)
            if eval(response_data['REPORT'])['result'] == False:
                report.all_result = False
    report.api_result = str(apis_result)
    report.save()
    return HttpResponse(str(report.all_result))


# 清空所有报告
def clear_all_reports(request):
    project_id = request.GET['project_id']
    DB_report.objects.filter(project_id=project_id).delete()
    return HttpResponse('')


def get_all_reports(request):
    project_id = request.GET['project_id']
    all_reports = list(DB_report.objects.filter(project_id=project_id).values())[::-1]
    for report in all_reports:
        report['api_result'] = eval(report['api_result'])
    return HttpResponse(json.dumps(all_reports), content_type='application/json')


def test_a(request):
    # print(request.body)
    return HttpResponse('{"a": "111", "b": {"c": [1,123], "d": "01"}}', content_type='application/json')


def test_b(request):
    print(request.body)
    return HttpResponse('{"a": "222", "b": {"c": [2,456], "d": "02"}}', content_type='application/json')
