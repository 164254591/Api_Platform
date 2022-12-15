import subprocess

from django.contrib import admin
import threading
import time
import json
import requests

# Register your models here.
from Api_app.models import *
from Api_app.views_api import run
from Api_app.views import set_monitor_next
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

admin.site.register(DB_notice)
admin.site.register(DB_news)
admin.site.register(DB_project_list)
admin.site.register(DB_env_list)
admin.site.register(DB_power_list)
admin.site.register(DB_apis)


# 监控
def email(adresss, content):
    # adresss = '164254591@qq.com'
    # mail_to = adresss.split(',')
    mail_to = adresss
    mail_host = 'smtp.qq.com'
    mail_user = '164254591@qq.com'  # 发送者邮箱地址
    mail_pass = 'nfsesqiwyzjacafj'  # smtp授权码

    c = MIMEText(content, 'html', 'utf-8')
    msg = MIMEMultipart('related')
    msg['From'] = mail_user
    msg['To'] = mail_to
    msg['Subject'] = '接口测试平台线上监控报告'
    msg.attach(c)

    try:
        server = smtplib.SMTP()
        server.connect(mail_host, 25)
        server.login(mail_user, mail_pass)
        server.sendmail(mail_user, mail_to, msg.as_string())
        print('发送邮件成功')
        server.close()
    except:
        print('邮件发送失败')


def robotApi(url, content):
    data = {"msg_type": "text", "content": {"text": content}}
    try:
        re = requests.post(url, data=json.dumps(data))
        print(re.text)
    except:
        print('机器人发送消息失败')


def monitor_thread():
    """
    巡逻线程
    :return:
    """
    while True:
        monitors = DB_monitor.objects.all()
        for monitor in monitors:
            if monitor.status != True:
                continue
            if abs(time.time() - float(monitor.next)) < 60:
                project_id = monitor.project_id
                res = run(request='', project_id=project_id)
                set_monitor_next(monitor, 'sys')
                monitor.save()
                # print(res.content)
                if res.content == b'False':
                    last_report = DB_report.objects.filter(project_id=project_id)[::-1][0]
                    r = ''
                    for i in eval(last_report.api_result):
                        i = eval(i)
                        r += '\n' + str(i['label']) + ':' + str(i['result'])
                    content = '【%s】线上监控项目报错！详情如下：%s' % (monitor.label, r)
                    print(monitor.email)
                    email(monitor.email, content)
                    robotApi(monitor.robot, content)


t = threading.Thread(target=monitor_thread)
t.setDaemon(True)
t.start()


# 抓包
def mitm_start():
    cmd = 'nohup mitmdump -p 8005'
    subprocess.call(cmd, shell=True)

m = threading.Thread(target=mitm_start)
m.setDaemon(True)
m.start()
