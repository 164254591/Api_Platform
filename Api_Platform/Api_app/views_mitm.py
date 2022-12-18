import json
import threading
import django
import sys, os

sys.path.append('D:\Git\dlz\Api_Platform')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Api_platform/settings.py')
django.setup()

from Api_app.models import *


def request(flow):
    '任何一个请求结果的时候，都会自动运行该函数'
    params = []
    if '?' in flow.request.url:
        for i in flow.request.url.split('?')[1].split('&'):
            params.append({'key': i.split('=')[0], 'value': i.split('=')[1]})
    headers = []
    for i in flow.request.headers:
        headers.append({'key': i, 'value': str(flow.request.headers[i])})
    form_data = {
        'path': '/' + '/'.join(flow.request.url.split('/')[3:]).split('?')[0],
        'type': 'api',
        'children': '[]',
        'host': flow.request.url.split('/'[:3]),
        'method': flow.request.method,
        'params': str(params),
        'headers': str(headers),

    }
    form_data['label'] = form_data['path']
    if flow.request.method.lower() in ['post', 'get']:
        if 'x-www' in flow.request.headers['Content-Type']:
            form_data['payload_method'] = 'x-www-form-urlencode'
            tmp = []
            d = flow.request.urlencode_form
            for i in d.keys():
                tmp.append({'key': i, 'value': d.get(i, '报错')})
            form_data['payload_xwfu'] = str(tmp)
        elif 'form-data' in flow.request.headers['Content-Type']:
            form_data['payload_method'] = 'form-data'
            tmp = []
            d = flow.request.multipart_form
            for i in d.keys():
                if i == 'file':
                    tmp.append({'key': i, 'value': '手动上传文件'})
                else:
                    tmp.append({'key': i, 'value': d.get(i, '报错')})
            form_data['payload_fd'] = str(tmp)
        elif 'plain' in flow.request.headers['Content-Type']:
            form_data['payload_method'] = 'raw'
            form_data['payload_method_raw'] = 'Text'
            form_data['payload_raw'] = str(flow.request.content)
        elif 'javascript' in  flow.request.headers['Content-Type']:
            form_data['payload_method'] = 'raw'
            form_data['payload_method_raw'] = 'JavaScript'
            form_data['payload_raw'] = str(flow.request.content)
        elif 'json' in flow.request.headers['Content-Type']:
            if 'query' in flow.request.content:
                form_data['payload_method'] = 'GraphQL'
                form_data['payload_GQL_q'] = json.loads(flow.request.content)['query']
                form_data['payload_GQL_g'] = json.loads(flow.request.content)['variables','']
            else:
                form_data['payload_method'] = 'raw'
                form_data['payload_method_raw'] = 'JSON'
                form_data['payload_raw'] = str(flow.request.content)
        elif 'xml' in flow.request.headers['Content-Type']:
            form_data['payload_method'] = 'raw'
            form_data['payload_method_raw'] = 'XML'
            form_data['payload_raw'] = str(flow.request.content)
        elif 'hxml' in flow.request.headers['Content-Type']:
            form_data['payload_method'] = 'raw'
            form_data['payload_method_raw'] = 'HTML'
            form_data['payload_raw'] = str(flow.request.content)
        else:
            form_data['payload_method'] = 'binary'


    t = threading.Thread(target=ttt, args=[form_data, ])
    t.setDaemon(True)
    t.start()


def ttt(form_data):
    '要把所有流经的数据放到数据库中'
    projects = DB_project_list.objects.filter(catch_status=True)
    for project in projects:
        form_data['project_id'] = project.id
        DB_apis.objects.create(**form_data)
