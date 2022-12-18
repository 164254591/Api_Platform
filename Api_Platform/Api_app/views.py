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
import requests
import easyocr
import Levenshtein
from python_jenkins_monitor.python_jenkins_monitor import get_next_time

logger = logging.getLogger('django')


# Create your views here.


def help(request):
    logger.warning('%s 刚刚进入帮助页面' % request.user.username)
    logger.error('%s 刚刚进入帮助页面' % request.user.username)
    return render(request, 'help.html')


def login(request, message=''):
    res = {}
    res['notices'] = list(DB_notice.objects.all().values('content'))[::-1][:2]
    res['message'] = message
    return render(request, 'login.html', res)


def login_action(request):
    time.sleep(0.5)
    username = request.POST.get('user', None)  # 使用登录的form表单中的input标签的name属性
    password = request.POST.get('password', None)
    # 去数据库进行比对
    user = auth.authenticate(username=username, password=password)
    if user is None:
        message = '用户名或者密码错误，请重试！'
        return login(request, message)
    else:
        auth.login(request, user)
        request.session['user'] = username  # 设置session
        return HttpResponseRedirect('/index/')


# 注册功能
def register_action(request):
    time.sleep(0.5)
    username = request.GET.get('user', None)  # 使用登录的form表单中的input标签的name属性
    password = request.GET.get('password', None)  # 可以简化为：request.GET['password']
    print('进入get user')
    user = auth.get_user(request)
    print('判断用户是否存在： ' + username, user)
    # 先判断用户是否存在，如果存在，则提示直接进行登录
    if user is None:
        message = f'恭喜你，用户{username}已注册成功！'
        new_user = User.objects.create_user(username=username, password=password)
        new_user.save()
        return login(request, message)
    else:
        user_flag = auth.authenticate(username=username, password=password)
        print(user_flag)
        # 用户密码正确
        if user_flag is not None:
            request.session['user'] = username
            auth.login(request, user)

            return HttpResponseRedirect('/index/')
        else:
            message = f'该用户名：【{username}】 已注册过，无需重复注册！'
            return login(request, message)


@login_required()
def index(request):
    return render(request, 'index.html')


def get_tj_datas(request):
    # 获取用户id，或者用户姓名request.user.username
    user_id = request.user.id
    # print(user_id)
    tj_datas = {}
    tj_datas['notices'] = list(DB_notice.objects.all().values('content'))[::-1]
    # tj_datas['news'] = [{"content": "哈哈哈"}]
    tj_datas['news'] = list(DB_news.objects.filter(to_user_id=user_id).values()[::-1])
    # print(tj_datas['news'])
    for i in tj_datas['news']:
        from_user_name = get_object_or_404(User, pk=i['from_user_id']).username
        i['from_user_name'] = from_user_name
        i['content'] = i['content'] + '...' if len(i['content']) > 3 else i['content']
    # print(tj_datas['news'])
    tj_datas['overview'] = {
        "project_count": 80,
        'api_count': 20,
        "case_count": 60,
        "user_count": 50,
        "env_count": 70
    }
    tj_datas['monitors'] = {
        "case_pass": 35,
        "api_pass": 99,
        "case_fail": 78
    }
    tj_datas['contributes'] = {
        "project": 50,
        "case": 30,
        "api": 80,
        "monitor": 95
    }
    return HttpResponse(json.dumps(tj_datas), content_type='application/json')


def get_real_time_datas(request):
    userID = request.user.id
    real_time_datas = {
        "ApiShop_count": len(DB_api_shop_list.objects.all()),
        "UnReadNews_count": len(DB_news.objects.filter(to_user_id=userID, read=False)),
        "RunCase_count": 88,
        "Import_count": 94
    }
    return HttpResponse(json.dumps(real_time_datas), content_type='application/json')


# 退出
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')  # 返回到首页


# 获取项目列表
def get_project_list(request):
    keys = request.GET.get('keys', None)
    if keys:
        project_list_data = list((DB_project_list.objects.filter(name__contains=keys) | DB_project_list.objects.filter(
            desc__contains=keys)).values())[::-1]
    else:
        # project_list_data = list(DB_project_list.objects.all().values())[::-1]
        project_list_data = list(DB_project_list.objects.filter(deleted=False).values())[::-1]  # 不显示逻辑删除的数据
    for i in project_list_data:
        try:
            user_name = get_object_or_404(User, pk=i['creator']).username
        except:
            user_name = '无人认领'
        i['user_name'] = user_name
    print(project_list_data)
    return HttpResponse(json.dumps(project_list_data), content_type='application/json')


# 增加项目
def add_project(request):
    uid = request.user.id if request.user.id else 0
    DB_project_list.objects.create(creator=uid, name='项目', desc='项目描述1')
    return get_project_list(request)


# 删除项目
def delete_project(request):
    project_id = request.GET['project_id']
    # DB_project_list.objects.filter(id=project_id).delete()
    DB_project_list.objects.filter(id=project_id).update(deleted=True)  # 逻辑删除
    return get_project_list(request)


# 获取单个项目详情
def get_project_detail(request):
    id = request.GET['id']
    form = list(DB_project_list.objects.filter(id=id).values())[0]
    return HttpResponse(json.dumps(form), content_type='application/json')


# 保存项目
def save_project(request):
    # 将字符串转换成字典
    form = json.loads(request.body.decode('utf-8'))
    DB_project_list.objects.filter(id=form['id']).update(**form)
    return HttpResponse('', content_type='application/json')
    # return get_project_list(request)


def get_env_list(request):
    env_list_data = list(DB_env_list.objects.all().values())[::-1]
    return HttpResponse(json.dumps(env_list_data), content_type='application/json')


def add_env(request):
    form_data = json.loads(request.body.decode('utf-8'))
    DB_env_list.objects.create(**form_data)
    return get_env_list(request)


def delete_env(request):
    env_id = request.GET['env_id']
    DB_env_list.objects.filter(id=env_id).delete()  # 物理删除
    return get_env_list(request)


# -----------------------------接口商店--------------------------------------------
def get_api_shop_list(request):
    api_shop_list_data = DB_api_shop_list.objects.all().values()[::-1]
    return HttpResponse(json.dumps(api_shop_list_data), content_type='application/json')


def save_api_shop(request):
    form_data = json.loads(request.body.decode('utf-8'))
    try:
        DB_api_shop_list.objects.filter(id=form_data['id']).update(**form_data)  # 编辑
    except:
        DB_api_shop_list.objects.create(**form_data)  # 新增
    return get_api_shop_list(request)


def add_api_shop(request):
    form_data = json.loads(request.body.decode('utf-8'))
    DB_api_shop_list.objects.create(**form_data)
    return get_api_shop_list(request)


def delete_api_shop(request):
    api_shop_id = request.GET['api_shop_id']
    DB_api_shop_list.objects.filter(id=api_shop_id).delete()
    return get_api_shop_list(request)


# 获取用户信息
def get_user_list(request):
    form_data = {
        'user_id': request.user.id,
        'user_name': request.user.username,
        'password': '********',
    }
    try:
        form_data['title'] = request.user.first_name
    except:
        form_data['title'] = ''
    return HttpResponse(json.dumps(form_data), content_type='application/json')


# 保存用户信息
def save_user_detail(request):
    form = json.loads(request.body.decode('utf-8'))
    user = User.objects.get(id=request.user.id)
    user.username = form['user_name']
    user.first_name = form['title']
    if form['password'] != '********':
        user.set_password(form['password'])
    user.save()
    return HttpResponse('')


# 上传用户头像
def upload_user_avatar(request):
    myFile = request.FILES.get('user_avatar', None)  # 获取原始文件名
    user_id = request.user.id
    file_name = 'userImage_' + str(user_id) + '.jpg'
    fp = open('Api_app/static/user_avatar/' + file_name, 'wb+')  # 需要手动先创建文件目录
    for i in myFile.chunks():
        fp.write(i)
    fp.close()
    return HttpResponse('')


# 获取户列表和消息
def get_to_user_list(request):
    res = {}
    to_user_list = list(User.objects.all().values('username', 'id', 'first_name'))
    for i in range(len(to_user_list)):
        to_user_list[i]['value'] = to_user_list[i]['username']  # 前端下拉框需要用value进行传值，所以需要增加value字段
    res['to_user_list'] = to_user_list
    # 获取消息
    news = DB_news.objects.filter(to_user_id=request.user.id)
    news.update(read=True)
    news = list(news.values()[::-1])
    for i in news:
        from_user_name = get_object_or_404(User, pk=i["from_user_id"]).username
        i['from_user_name'] = from_user_name
    res['news'] = news
    return HttpResponse(json.dumps(res), content_type='applications/json')


# 发送消息
def send_news(request):
    data = json.loads(request.body.decode('utf-8'))
    user_id = data['user_id']
    content = data['content']
    from_user_id = request.user.id
    date = str(time.strftime('%Y-%m-%d %H:%M:%S'))
    DB_news.objects.create(to_user_id=user_id, content=content, from_user_id=from_user_id, date=date)
    return HttpResponse('')


# 发送公告
def send_notice(request):
    data = json.loads(request.body.decode('utf-8'))
    content = data['content']
    date = str(time.strftime('%Y-%m-%d %H:%M:%S'))
    DB_notice.objects.create(content=content, date=date)
    return HttpResponse('')


# 查看文件
def look_log(request):
    res = {
        "logs": '',
        "error_count": 0,
        "error_lines": [],
        "waring_count": 0,
        "waring_lines": [],
    }
    with open('dlz.info.log', 'r', encoding='utf-8') as fp:
        L = fp.readlines()[-1000:]  # 最新的100条记录

    for i in range(len(L)):
        if '[ERROR]' in L[i]:
            res['error_count'] += 1
            res['error_lines'].append(i + 1)
            res['logs'] += str(i + 1) + ' ' + "[错误行]：" + L[i]
        elif '[WARING]' in L[i]:
            res['waring_count'] += 1
            res['waring_lines'].append(i + 1)
            res['logs'] += str(i + 1) + ' ' + "[警告行]：" + L[i]
        else:
            res['logs'] += str(i + 1) + ' ' + L[i]

    return HttpResponse(json.dumps(res), content_type='application/json')


# 获取权限列表
def get_power_list(request):
    if request.user.id != 1:
        logger.warning('%s 试图进入权限管理模块，已被固定最高级别权限拦截！' % request.user.username)
        return HttpResponse(json.dumps({}), content_type='application/json')
    res = {}
    power_list_data = list(DB_power_list.objects.all().values())
    for i in power_list_data:
        i['users'] = eval(i['users'])  # 将字符串转换成列表
    res['power_list_data'] = power_list_data

    all_user = list(User.objects.all().values('id', 'username', 'first_name'))
    for i in all_user:
        i['title'] = i['first_name']
    res['all_user'] = all_user

    all_paths = '和path同名的函数如下：\n-----------------------\n'
    with open('Api_app/views.py', 'r', encoding='utf-8') as fp:
        L = fp.readlines()
        for i in L:
            if 'def ' in i:
                if '(request' in i:
                    all_paths += i + '\n'
    res['all_paths'] = all_paths
    return HttpResponse(json.dumps(res), content_type='application/json')


# 保存权限
def save_power(request):
    form = json.loads(request.body.decode('utf-8'))
    DB_power_list.objects.filter(id=form['id']).update(**form)
    return get_power_list(request)


# 删除权限
def delete_power(request):
    id = request.GET['id']
    DB_power_list.objects.filter(id=id).delete()
    return get_power_list(request)


# 增加权限
def add_power(request):
    DB_power_list.objects.create()
    return get_power_list(request)


# 自定义权限判定
def diy_power(request, path):
    power = DB_power_list.objects.filter(path=path)
    if power:  # 中了权限监管
        user_ids = [i.split('-')[0] for i in eval(power[0].users)]
        if str(request.user.id) in user_ids:
            # 有权限
            r = locals()
            exec('r=%s(request)' % path)
            return r['r']
        else:
            return HttpResponse('没有权限')
    else:  # 没中
        return default_power(request, path)


# 自然默认权限判定
def default_power(request, path):
    if path == 'delete_project':
        project_id = request.GET['project_id']
        if request.user.id != DB_project_list.objects.filter(id=project_id)[0].creator:
            return HttpResponse('没有权限')
    if path in ['favicon.ico']:
        return HttpResponse('')

    # 有权限
    r = locals()
    exec('r=%s(request)' % path)
    return r['r']


# 接口商店下载
def download_api(request):
    project_id = request.GET['project_id']
    api_id = request.GET['api_id']
    api = list(DB_api_shop_list.objects.filter(id=int(api_id)).values())[0]
    # print(api)
    api['project_id'] = project_id
    del api['id']
    DB_apis.objects.create(**api)
    return HttpResponse('')


# 查询
def get_monitor_list(request):
    moniter_list = list(DB_monitor.objects.all().values())
    for i in moniter_list:
        if i['method'] in ('间隔时间', '每日定时') and i['next'] and '-' not in i['next']:
            i['next'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i['next'])))
    return HttpResponse(json.dumps(moniter_list), content_type='application/json')


# 增加
def add_monitor(request):
    DB_monitor.objects.create()
    return get_monitor_list(request)


# 更改
def change_monitor_status(request):
    id = request.GET['id']
    monitor = DB_monitor.objects.filter(id=int(id))[0]
    if monitor.status == True:  # 我要关上
        monitor.status = False
    else:  # 我要打开
        monitor.status = True
        set_monitor_next(monitor, 'human')
    monitor.save()
    return get_monitor_list(request)


# 保存
def save_monitor(request):
    form_data = json.loads(request.body.decode('utf-8'))
    # print(form_data)
    del form_data['next']
    monitor = DB_monitor.objects.filter(id=int(form_data['id']))
    monitor.update(**form_data)
    monitor.update(status=False)
    return get_monitor_list(request)


# 删除
def delete_monitor(request):
    id = request.GET['id']
    DB_monitor.objects.filter(id=int(id)).delete()
    return get_monitor_list(request)


# 计算下一次执行时间
def set_monitor_next(monitor, which):
    if monitor.method == '间隔时间':
        if which == 'human':
            monitor.next = int(time.time()) + int(monitor.value) * 60
        else:  # 巡逻线程调用
            monitor.next = int(monitor.next) + int(monitor.value) * 60
    elif monitor.method == '每日定时':
        h = int(monitor.value.split(':')[0])
        m = int(monitor.value.split(':')[1])
        hm = h * 3600 + m * 60
        today_s = int(time.time()) - int(time.time() - time.timezone) % 86400 + hm
        # print(today_s)
        if which == 'human':
            if today_s <= time.time():  # 今天来不及了
                monitor.next = today_s + 86400
            else:
                monitor.next = today_s
        else:  # 巡逻线程
            monitor.next = monitor.next + 86400
    elif monitor.method == 'jenkins':
        monitor.next = get_next_time(monitor.value)


# 解析接口文档
def jx_apiDoc(request):
    ad_url = request.GET['ad_url']
    response = requests.get(ad_url)
    # 发送请求，解析
    form_data = {}

    return HttpResponse(json.dumps(form_data), content_type='application/json')


# 导入接口文档
def import_api_ad(request):
    project_id = request.GET['project_id']
    form_data = json.loads(request.body.decode('utf-8'))
    form_data['project_id'] = project_id
    DB_apis.objects.create(**form_data)
    return HttpResponse('')


# postman文件上传
def upload_postman_file(request):
    myFile = request.FILES.get('postman_file', None)
    file_name = str(myFile)
    fp = open('Api_Platform/Api_app/static/postmanFile/' + file_name, 'wb+')
    for i in myFile.chunks():
        fp.write(i)
    fp.close()
    return HttpResponse('')


# postman文件导入
def import_api_postman(request):
    project_id = request.GET['project_id']
    file_name = request.GET['file_name']
    with open('Api_Platform/Api_app/static/postmanFile/' + file_name, 'r') as fp:
        s = fp.read()
    s = json.loads(s)
    items = s['item']
    for i in items:
        form_data = {
            'project_id': project_id,
            'label': i['name'],
            'type': 'api',
            'children': '[]',
            'desc': '[%s]postman导入的接口' % s['info']['name'],
            'host': i['request']['url']['protocol'] + '://' + '.'.join(i['request']['url']['host']),
            'path': '/' + '/'.join(i['request']['url']['path']),
            'method': i['request']['method'],
            'params': str(i['request']['url'].get('query', [])),
            'headers': str(i['request']['header']),
            'payload_method': i['request'].get('body', {}).get('mode', ''),

        }
        if i['request']['url'].get('port', None):
            form_data['host'] += ':' + str(i['request']['url']['port'])
        form_data['payload_method'] = form_data['payload_method'].replace('urlencoded',
                                                                          'x-www-form-urlencoded').replace('graphql',
                                                                                                           'GraphQL').replace(
            'formdata', 'form-data')
        if form_data['payload_method'] == 'form-data':
            form_data['payload_fd'] = str(i['request']['body']['formdata'])
        elif form_data['payload_method'] == 'x-www-form-urlencoded':
            form_data['payload_xwfu'] = str(i['request']['body']['urlencoded'])
        elif form_data['payload_method'] == 'GraphQL':
            form_data['payload_GQL_q'] = i['request']['body']['graphql']['query']
            form_data['payload_GQL_q'] = i['request']['body']['graphql']['variables']
        elif form_data['payload_method'] == 'raw':
            form_data['payload_GQL_q'] = i['request']['body']['raw']
            if i['request']['body'].get('options', None):
                form_data['payload_raw_method'] = i['request']['body']['raw']['language']
                form_data['payload_raw_method'] = form_data['payload_raw_method'].replace('javascript',
                                                                                          'JavaScript').replace('json',
                                                                                                                'JSON').replace(
                    'html', 'HTML').replace('xml', 'XML')
            else:
                form_data['payload_raw_method'] = 'Text'
        DB_apis.objects.create(**form_data)
    return HttpResponse('')


# 改变项目是否可抓包导入的状态
def change_catch_status(request):
    project_id = request.GET['project_id']
    project = DB_project_list.objects.filter(id=int(project_id))[0]
    project.catch_status = (project.catch_status == False)
    project.save()
    return get_project_list(request)


# img文件上传
def upload_img_file(request):
    myFile = request.FILES.get('img_file', None)
    file_name = str(myFile)
    fp = open('Api_app/static/imgFile/' + file_name, 'wb+')
    for i in myFile.chunks():
        fp.write(i)
    fp.close()
    return HttpResponse('')


# 解析图片
def jx_img(request):
    file_name = request.GET['file_name']
    print(file_name)
    form_data = {'des': '图片识别导入'}
    reader = easyocr.Reader(['ch_sim', 'en'])
    L = reader.readtext('Api_app/static/imgFile/' + file_name, detail=0)
    print(L)
    ############# 设计需求锚点，默认误差距离为1 ####
    pars = {
        'label': ['接口描述', '接口名字', '接口名称', '接口name'],
        'host': ['HOST', '域名'],
        'method': ['METHOD', '请求方式'],
        'payload_method': ['请求类型', '请求体类型'],
        'path': ['URL', 'url', 'PATH', '路由'],
        'headers': ['headers', '请求头'],
        'params': ['params', 'Params', 'url参数'],
        '参数锚点': ['参数名', '参数列表', '请求体参数'],
    }
    ############## 矫正列表 #########
    news = {
        'multipart/form-data': {'payload_method': 'form-data'},
        'application/x-www-form-urlencoded': {'payload_method': 'x-www-form-urlencoded'},
        'application/json': {'payload_method': 'raw', 'payload_raw_method': 'JSON'},
        'text/xml': {'payload_method': 'raw', 'payload_raw_method': 'XML'},
        'text/html': {'payload_method': 'raw', 'payload_raw_method': 'HTML'},
        'text/plain': {'payload_method': 'raw', 'payload_raw_method': 'TEXT'},
        'text/javascript': {'payload_method': 'raw', 'payload_raw_method': 'JavaScript'},
    }
    # 参数部分
    payload_index = 0  # 参数起始位置
    payload_step = 5  # 根据公司业务具体情况而定

    def write_payload(payload_method):
        if payload_method == 'form_data':
            payload_tmp = []
            for i in range(payload_index, len(L), payload_step):
                payload_tmp.append({'key': L[i]})
            form_data['payload_fd'] = str(payload_tmp)
        elif payload_method == 'x-www-form-urlencoded':
            payload_tmp = []
            for i in range(payload_index, len(L), payload_step):
                payload_tmp.append({'key': L[i]})
            form_data['payload_xwfu'] = str(payload_tmp)
        elif payload_method == 'raw':
            if form_data['payload_raw_method'] == 'JSON':
                payload_tmp = []
                for i in range(payload_index, len(L), payload_step):
                    payload_tmp[L[i]] = ''
                form_data['payload_raw'] = json.dumps(payload_tmp)

    for par in pars.keys():
        max = [0, 0]  # 得分，下标
        for v in pars[par]:
            for l in range(len(L)):
                score = Levenshtein.ratio(v, L[l])
                if score > max[0] and score > 0.5:  # 具体多少根据实际情况设置
                    max = [score, l]
                if max[0] == 1:  # 如果已经是满分了
                    break
            else:
                continue
            break
        if max[0] > 0.5:
            # 找到锚点
            try:
                old = L[max[1] + 1]
                max_n = [0, '']  # 存放最可能的矫正值
                for new in news.keys():
                    score_n = Levenshtein.ratio(new, old)
                    if score_n > max_n[0] and score_n > 0.7:
                        max_n = [score_n, new]
                    if max_n[0] == 1:
                        break
                if max_n[0] > 0.7:
                    form_data.update(news[max_n[1]])
                else:
                    form_data[par] = old
                # 特殊处理
                if par == 'url':
                    params = []
                    if '?' in old:
                        for i in old.split('?')[1].split('&'):
                            params.append({'key': i.split('=')[0], 'value': i.split('=')[1]})
                    form_data['params'] = str(params)
                if par == "参数锚点":
                    payload_index = max[1] + payload_step
            except:
                pass
    if form_data.get('参数锚点', None):
        # 写入参数
        write_payload(form_data.get('payload_method', None))
        # 删除参数锚点
        del form_data['参数锚点']

    return HttpResponse(json.dumps(form_data), content_type='application/json')
