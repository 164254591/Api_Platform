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
    form_data = {
        "label": '接口111'
    }
    t = threading.Thread(target=ttt, args=[form_data, ])
    t.setDaemon(True)
    t.start()


def ttt(form_data):
    '要把所有流经的数据放到数据库中'
    projects = DB_project_list.objects.filter(catch_status=True)
    for project in projects:
        form_data['project_id'] = project.id
        DB_apis.objects.create(**form_data)
