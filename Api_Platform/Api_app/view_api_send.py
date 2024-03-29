import pymysql
from django.shortcuts import render
from Api_app.models import *
import time
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
import json
import logging
import re

import requests
import pymysql

logger = logging.getLogger('django')


# 生成身份证号码
def generate_ID():
    ...


# 多用途互联网邮件扩展类型
def get_MIME(filename):
    d = {
        'image/png': ['png'],
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['xlsx'],
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['pptx'],
        'application/pdf': ['pdf'],
        'image/jpeg': ['jpg', 'jpeg'],
        'application/zip': ['zip'],
        'text/plain': ['txt'],
        'video/mp4': ['mp4'],
        'application/msword': ['doc', 'dot'],
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['docx'],
        'application/vnd.openxmlformats-officedocument.wordprocessingml.template': ['dotx'],
        'application/vnd.ms-word.document.macroEnabled.12': ['docm'],
        'application/vnd.ms-word.template.macroEnabled.12': ['dotm'],
        'application/vnd.ms-excel': ['xls', 'xlt', 'xla'],
        'application/vnd.openxmlformats-officedocument.spreadsheetml.template': ['xltx'],
        'application/vnd.ms-excel.sheet.macroEnabled.12': ['xlsm'],
        'application/vnd.ms-excel.template.macroEnabled.12': ['xltm'],
        'application/vnd.ms-excel.addin.macroEnabled.12': ['xlam'],
        'application/vnd.ms-excel.sheet.binary.macroEnabled.12': ['xlsb'],
        'application/vnd.ms-powerpoint': ['ppt', 'pot', 'pps', 'ppa'],
        'application/vnd.openxmlformats-officedocument.presentationml.slideshow': ['ppsx'],
        'application/vnd.ms-powerpoint.addin.macroEnabled.12': ['ppam'],
        'application/vnd.ms-powerpoint.presentation.macroEnabled.12': ['pptm', 'potm'],
        'application/vnd.ms-powerpoint.slideshow.macroEnabled.12': ['ppsm'],
        'application/x-tar': ['tar'],
    }
    hz = filename.split('.')[-1]  # 后缀
    for key, value in d.items():
        if hz in value:
            return key
    return 'application/octet-stream'  # 一切未知类型


# 调用多个接口
# 第一个接口调用SENDAPI，传进来一个空字典TQ {}，提取的变量全部塞进这个字典TQ，返回这个有内容的字典TQ
# 第二个接口调用SENDAPI，传进来刚刚已经有内容的字典TQ {}，并把自己提取的变量也塞进这个字典TQ，然后再返回TQ
# 第三个接口调用SENDAPI，传进来刚刚已经有内容的字典TQ {}，并把自己提取的变量也塞进这个字典TQ，然后再返回TQ
# --------------------------------------文件作用：发送接口请求
class SENDAPI():
    def __init__(self, api, TQ, children):
        self.children = children
        self.api = api
        # print(api)
        self.make_header()
        self.make_method()
        self.TQ = TQ  # 设置传入的提取TQ作为类变量
        # self.CR = []
        self.send_real = True
        self.api['payload_method'] = self.api['payload_method'].lower()
        self.api['payload_raw_method'] = self.api['payload_raw_method'].lower()
        self.REPORT = {}
        self.REPORT['label'] = self.api['label']
        self.REPORT['result'] = True
        self.REPORT['method'] = self.api['method']

    # 替换提取的变量
    def TQ_replace(self):
        # headers
        for key in self.headers.keys():
            tqs = re.findall(r'{%(.*?)%}', self.headers[key])
            for tq in tqs:
                try:
                    self.headers[key] = self.headers[key].replace('{%' + tq + '%}', str(self.TQ[tq]))
                except:
                    self.headers[key] = self.headers[key]
        self.REPORT['request_headers'] = self.headers

        # params
        for i in range(len(self.api['params'])):
            tqs = re.findall(r'{%(.*?)%}', self.api['params'][i]['value'])
            for tq in tqs:
                try:
                    self.api['params'][i]['value'] = self.api['params'][i]['value'].replace('{%' + tq + '%}',
                                                                                        str(self.TQ[tq]))
                except:
                    self.api['params'][i]['value'] = self.api['params'][i]['value']
            host = self.api['host']
            path = self.api['path']
            params = self.api['params']
            self.REPORT['url'] = host + path + '?' + '&'.join(["%s=%s" % (i['key'], i['value']) for i in params if i])  # 过滤空行


        # print(self.api['params'])
        # payload_fd
        for i in range(len(self.api['payload_fd'])):
            tqs = re.findall(r'{%(.*?)%}', self.api['payload_fd'][i]['value'])
            for tq in tqs:
                self.api['payload_fd'][i]['value'] = self.api['payload_fd'][i]['value'].replace('{%' + tq + '%}',
                                                                                                str(self.TQ[tq]))
        # print(self.api['payload_fd'])
        # payload_xwfu
        for i in range(len(self.api['payload_xwfu'])):
            tqs = re.findall(r'{%(.*?)%}', self.api['payload_xwfu'][i]['value'])
            for tq in tqs:
                self.api['payload_xwfu'][i]['value'] = self.api['payload_xwfu'][i]['value'].replace('{%' + tq + '%}',
                                                                                                    str(self.TQ[tq]))
        # print(self.api['payload_xwfu'])

        # payload_raw
        # print(self.api['payload_raw'])
        tqs = re.findall(r'{%(.*?)%}', self.api['payload_raw'])
        for tq in tqs:
            self.api['payload_raw'] = self.api['payload_raw'].replace('{%' + tq + '%}', str(self.TQ[tq]))
        # print(self.api['payload_raw'])

        # # payload_GQL_q
        # print(self.api['payload_GQL_q'])
        tqs = re.findall(r'{%(.*?)%}', self.api['payload_GQL_q'])
        for tq in tqs:
            self.api['payload_GQL_q'] = self.api['payload_GQL_q'].replace('{%' + tq + '%}', str(self.TQ[tq]))
        # print(self.api['payload_GQL_q'])

        # payload_GQL_g
        tqs = re.findall(r'{%(.*?)%}', self.api['payload_GQL_g'])
        for tq in tqs:
            self.api['payload_GQL_g'] = self.api['payload_GQL_g'].replace('{%' + tq + '%}', str(self.TQ[tq]))
        # print(self.api['payload_GQL_g'])

    def get_sql(self, sql):
        project_id = self.api['project_id']
        project = DB_project_list.objects.filter(id=int(project_id))[0]
        sql_host = project.sql_host
        sql_port = project.sql_port
        sql_user = project.sql_user
        sql_pwd = project.sql_pwd
        sql_db = project.sql_db
        try:
            connect = pymysql.Connect(host=sql_host, port=int(sql_port), user=sql_user, password=sql_pwd,
                                      database=sql_db, charset='utf8')
            cursor = connect.cursor()
            cursor.execute(sql)
            cursor.commit()
            res = cursor.fetchall()
        except:
            res = ()
        finally:
            try:
                cursor.close()
            except:
                pass
        return res

    def make_url(self):
        """拼接url"""
        host = self.api['host']
        path = self.api['path']
        params = self.api['params']
        # 列表推导式------高级用法
        self.url = host + path + '?' + '&'.join(["%s=%s" % (i['key'], i['value']) for i in params if i])  # 过滤空行
        # print(self.url)

    def make_header(self):
        """请求头"""
        self.headers = {}
        for i in self.api['headers']:
            if i['key']:  # 去掉空值
                self.headers[i['key']] = i['value']
        # print(self.headers)

    def make_method(self):
        """整理成标准的请求头格式"""
        self.method = self.api['method']

    def make_RD(self):
        """生成返回头、返回码等数据"""
        self.RD = ''
        self.RD += '\n[%s]:%s\n' % ('status_code', self.response.status_code)
        self.RD += '\n[%s]:%s\n' % ('header', self.response.headers)
        self.REPORT['status_code'] = self.response.status_code
        self.REPORT['response_header'] = str(self.response.headers)
        if int(self.REPORT['status_code']) > 399:
            self.REPORT['result'] = False

    def do_configure(self, configure):
        """执行配置函数"""
        if configure['method'] == "断言":
            if configure['select'] == "全值检索":
                if configure['value'] in self.R:
                    return True
            elif configure['select'] == "正则匹配":
                left = configure['value'].split('==')[0].strip()
                right = configure['value'].split('==')[1].strip()
                # print(left, right)
                if re.findall(left, self.R) == [right]:
                    return True
            elif configure['select'] == "路径匹配":
                left = configure['value'].split('==')[0].strip()
                right = configure['value'].split('==')[1].strip()
                try:
                    if eval(self.R + left) == eval(right):
                        return True
                except:
                    return False
            elif configure['select'] == "SQL断言":
                left = configure['value'].split(';')[0].strip() + ';'
                right = configure['value'].split(';')[-1].split('==')[-1].strip()
                res = self.get_sql(left)
                if right:
                    right = eval(right)
                    try:
                        if res[0][0] == right:
                            return True
                    except:
                        self.REPORT['result'] = False
                        return False
                else:
                    if res:
                        return True
        elif configure['method'] == "提取":
            if configure['select'] == "路径提取":
                left = configure['value'].split('=')[0].strip()
                right = configure['value'].split('=')[1].strip()
                try:
                    S = locals()
                    exec('s=json.loads(self.R)' + right)
                    self.TQ[left] = S['s']
                    return True
                except:
                    self.REPORT['result'] = False
                    return False
            elif configure['select'] == "正则提取":
                left = configure['value'].split('=')[0].strip()
                right = configure['value'].split('=')[1].strip()
                try:
                    self.TQ[left] = re.findall(right, self.R)[0]
                    return True
                except:
                    self.REPORT['result'] = False
                    return False
            elif configure['select'] == "sql提取":
                left = configure['value'].split('=')[0].strip()
                right = '='.join(configure['value'].split('=')[1:]).strip()
                res = self.get_sql(right)
                if res:
                    self.TQ[left] = res[0][0]
                    return True
        elif configure['method'] == "SQL增删改":
            res = self.get_sql(configure['value'])
            return True
        elif configure['method'] == "随机变量":
            left = configure['value'].split('=')[0].strip()
            right = configure['value'].split('=')[1].strip()
            self.TQ[left] = eval(right)
            # print(self.TQ)
            return True
        elif configure['method'] == "mock":
            if configure['select'] == "写死返回值":
                self.R = configure['value']
                self.send_real = False  # 设置开关，不执行发送mock接口
            elif configure['select'] == "第三方接口":  # 不运行接口，只修改请求数据
                self.url = configure['value'].split('\n')[0]
                self.method = configure['value'].split('\n')[1]
                self.headers = json.loads(configure['value'].split('\n')[2])
                if 'raw' in configure['value'].split['\n'][3]:
                    self.api['payload_method'] = 'raw'
                    self.api['payload_raw_method'] = configure['value'].split('\n')[3].split('-')[1]
                else:
                    self.api['payload_method'] = configure['value'].split('\n')[3]
                self.api['payload_fd'] = configure['value'].split('\n')[4]
                self.api['payload_xwfu'] = configure['value'].split('\n')[4]
                self.api['payload_raw'] = configure['value'].split('\n')[4]
            return True
        elif configure['method'] == "插入参数":
            left = configure['value'].split('=')[0].strip()
            right = eval('='.join(configure['value'].split('=')[1:]).strip())  # 对字符串中有多个=的处理
            if configure['select'] == 'request_header':
                self.headers[left] = right
            elif configure['select'] == 'params':
                self.url += '&' + left + '=' + str(right)
            elif configure['select'] == 'request_body':
                if self.api['payload_method'] == 'form-data'.lower():
                    self.api['payload_fd'].append({"key": left, "value": right})
                elif self.api['payload_method'] == 'x-www-form-urlencoded':
                    self.api['payload_xwfu'].append({"key": left, "value": right})
                elif self.api['payload_method'] == 'raw' and self.api['payload_method'].lower() == 'json'.lower():
                    s = self.api['payload_raw']
                    s.json.loads(s)
                    s[left] = right
                    self.api['payload_raw'] = json.dumps(s)
            return True
        elif configure['method'] == "加密算法":
            left = configure['value'].split('=')[0].strip()
            right = eval('='.join(configure['value'].split('=')[1:]).strip())  # 对字符串中有多个=的处理
            if configure['select'] == 'request_header':
                self.headers[left] = right
            elif configure['select'] == 'params':
                self.url += '&' + left + '=' + str(right)
            return True
        self.REPORT['result'] = False
        return False

    def send(self):
        """执行接口"""
        self.REPORT['url'] = self.url
        self.REPORT['request_headers'] = self.headers
        self.REPORT['payload_method'] = self.api['payload_method']
        self.REPORT['payload_raw_method'] = self.api['payload_raw_method']
        self.REPORT['payload'] = json.dumps({
            "payload_fd": self.api['payload_fd'],
            "payload_xwfu": self.api['payload_xwfu'],
            "payload_raw": self.api['payload_raw'],
            "payload_GQL_q": self.api['payload_GQL_q'],
            "payload_GQL_g": self.api['payload_GQL_g'],
        })

        if self.api['payload_method'] == 'none':
            self.response = requests.request(self.method, self.url, headers=self.headers, data={})
        elif self.api['payload_method'] == 'form-data':  # {"a":1,"b":2}
            files = []
            payload = {}
            for i in self.api['payload_fd']:
                if '*FILE*' in i['value']:  # 是文件参数
                    file_name = i['value'].split('*FILE*')[1]
                    files.append(
                        (i['key'], (file_name, open('Api_app/static/tmp/' + file_name, 'rb'), get_MIME(file_name))))
                else:
                    payload[i['key']] = i['value']
            self.response = requests.request(self.method, self.url, headers=self.headers, data=payload, files=files)
        elif self.api['payload_method'] == 'x-www-form-urlencoded':  # a=1&b=2
            # payload = ''
            # for i in self.api['payload_xwfu']:
            #     payload += '%s=%s&' % (i['key'], i['value'])
            payload = '&'.join([('%s=%s' % (i['key'], i['value'])) for i in self.api['payload_xwfu']])
            self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
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
            file_name = self.api['payload_binary']
            payload = open('Api_app/static/tmp/' + file_name, 'rb')
            self.headers['Content-Type'] = get_MIME(file_name)  # MIME文件格式
            self.response = requests.request(self.method, self.url, headers=self.headers, data=payload)
        elif self.api['payload_method'] == 'GraphQL':
            self.headers['Content-Type'] = 'application/json'
            payload = json.dumps({"query": self.api['payload_GQL_q'], "variables": eval(self.api['payload_GQL_g'])})
            self.response = requests.request(self.method, self.url, headers=self.headers, data=payload)
        else:
            self.response = requests.request(self.method, self.url, headers=self.headers, data={})
        try:
            # 优先用字典接收，如果不是则用text接收
            self.R = json.dumps(self.response.json(), ensure_ascii=False)  # 防止中文乱码
        except:
            # 如果返回是字典，用text接受就会乱码
            self.R = self.response.text

    def index(self):
        """入口函数"""

        try:
            self.TQ_replace()
        except Exception as e:
            # print(e)
            self.REPORT['result'] = False
            return {"R": '执行失败，存在未定义变量', "RD": '', "CR": '', "TQ": self.TQ, "REPORT": str(self.REPORT)}

        self.make_url()
        self.CR = []
        # print(children)
        for i in self.children:
            if i['do_time'] == 'before':
                self.CR.append('【%s】 = %s' % (i['label'], self.do_configure(i)))
                self.children.remove(i)
        if self.send_real == True:
            try:
                self.send()
            except Exception as e:
                # print(e)
                self.REPORT['result'] = False
                return {"R": '执行失败，接口请求失败', "RD": '', "CR": '', "TQ": self.TQ, "REPORT": str(self.REPORT)}
        for i in self.children:
            self.CR.append('【%s】 = %s' % (i['label'], self.do_configure(i)))
        self.make_RD()
        self.CR = '\n'.join(self.CR)
        return self.response_data()

    def response_data(self):
        """获取返回结果"""""
        self.REPORT["R"] = self.R
        self.REPORT["CR"] = self.CR
        self.REPORT["TQ"] = self.TQ
        r = {"R": self.R, "RD": self.RD, "CR": self.CR, "TQ": self.TQ, "REPORT": str(self.REPORT)}
        return r
