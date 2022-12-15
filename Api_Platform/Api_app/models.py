from django.db import models


# Create your models here.


class DB_notice(models.Model):
    content = models.CharField(max_length=100, null=True, blank=True, default='')
    date = models.CharField(max_length=50, null=True, default='_')

    def __str__(self):
        return str(self.content)


class DB_news(models.Model):
    from_user_id = models.IntegerField(default=0)
    to_user_id = models.IntegerField(default=0)
    content = models.CharField(max_length=50, null=True, default='')
    date = models.CharField(max_length=50, null=True, default='_')

    def __str__(self):
        return self.content[:20] + '...'


class DB_project_list(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, default='-')
    desc = models.CharField(max_length=100, null=True, blank=True, default='-')
    creator = models.IntegerField(default=0)
    # mock = models.CharField(max_length=50, null=True, blank=True, default='mock_data')  # mock_data or redirect
    priviate = models.BooleanField(default=True)  # 私密项目
    # power = models.CharField(max_length=50, null=True, blank=True, default='[]')  # 权限：自己、同事、领导、所有人
    bus_type = models.CharField(max_length=50, null=True, blank=True, default='')  # 业务线:app,web
    # P_data = models.CharField(max_length=500, null=True, blank=True, default='_')  # 公共变量
    # L_data = models.CharField(max_length=500, null=True, blank=True, default='_')  # 登录状态变量
    # sign = models.CharField(max_length=500, null=True, blank=True, default='_')  # 加密算法
    email = models.CharField(max_length=500, null=True, blank=True, default='[]')  # 邮箱设置,默认列表，方便后续eval进行列表操作
    sql_host = models.CharField(max_length=50, null=True, blank=True, default='')  # 数据库设置
    sql_port = models.IntegerField(default=0)  # 数据库设置
    sql_user = models.CharField(max_length=50, null=True, blank=True, default='')  # 数据库设置
    sql_pwd = models.CharField(max_length=50, null=True, blank=True, default='')  # 数据库设置
    sql_db = models.CharField(max_length=50, null=True, blank=True, default='')  # 库名
    doing_api = models.CharField(max_length=50, null=True, blank=True, default='')  # 执行中的接口
    end_result = models.TextField(default='')  # 结果
    dck = models.CharField(max_length=500, null=True, blank=True, default='')  # 选中的
    deleted = models.BooleanField(default=False)  # 假删除
    catch_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class DB_env_list(models.Model):
    host = models.CharField(max_length=20, null=True, blank=True, default="http://")
    type = models.CharField(max_length=20, null=True, blank=True, default="")
    des = models.CharField(max_length=20, null=True, blank=True, default="")

    def __str__(self):
        return self.host


class DB_api_shop_list(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True, default='新接口')
    type = models.CharField(max_length=10, null=True, blank=True, default='api')
    children = models.CharField(max_length=5000, null=True, blank=True, default='[]')
    des = models.CharField(max_length=300, null=True, blank=True, default='')
    host = models.CharField(max_length=300, null=True, blank=True, default='')
    path = models.CharField(max_length=300, null=True, blank=True, default='')
    method = models.CharField(max_length=30, null=True, blank=True, default='')
    params = models.CharField(max_length=3000, null=True, blank=True, default='[]')
    headers = models.CharField(max_length=3000, null=True, blank=True, default='[]')
    payload_method = models.CharField(max_length=30, null=True, blank=True, default='')
    payload_fd = models.CharField(max_length=3000, null=True, blank=True, default='[]')
    payload_xwfu = models.CharField(max_length=3000, null=True, blank=True, default='[]')
    payload_raw_method = models.CharField(max_length=300, null=True, blank=True, default='')
    payload_raw = models.CharField(max_length=3000, null=True, blank=True, default='')
    payload_GQL_q = models.CharField(max_length=3000, null=True, blank=True, default='')
    payload_GQL_g = models.CharField(max_length=3000, null=True, blank=True, default='')
    payload_binary = models.CharField(max_length=100, null=True, blank=True, default='')

    def __str__(self):
        return self.name


class DB_power_list(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, default="")  # 名字
    users = models.CharField(max_length=500, null=True, blank=True, default='[]')  # 所拥有权限的用户
    path = models.CharField(max_length=100, null=True, blank=True, default='')

    def __str__(self):
        return self.name


class DB_apis(models.Model):
    project_id = models.IntegerField(default=0)
    label = models.CharField(max_length=100, null=True, blank=True, default='新接口')
    type = models.CharField(max_length=10, null=True, blank=True, default='api')
    children = models.CharField(max_length=5000, null=True, blank=True, default='[]')

    des = models.CharField(max_length=300, null=True, blank=True, default='')
    host = models.CharField(max_length=300, null=True, blank=True, default='')
    path = models.CharField(max_length=300, null=True, blank=True, default='')
    method = models.CharField(max_length=30, null=True, blank=True, default='')
    params = models.CharField(max_length=3000, null=True, blank=True, default='[]')
    headers = models.CharField(max_length=3000, null=True, blank=True, default='[]')
    payload_method = models.CharField(max_length=30, null=True, blank=True, default='')
    payload_fd = models.CharField(max_length=3000, null=True, blank=True, default='[]')
    payload_xwfu = models.CharField(max_length=3000, null=True, blank=True, default='[]')
    payload_raw_method = models.CharField(max_length=300, null=True, blank=True, default='')
    payload_raw = models.CharField(max_length=3000, null=True, blank=True, default='')
    payload_GQL_q = models.CharField(max_length=3000, null=True, blank=True, default='')
    payload_GQL_g = models.CharField(max_length=3000, null=True, blank=True, default='')
    payload_binary = models.CharField(max_length=100, null=True, blank=True, default='')

    def __str__(self):
        return self.label


class DB_report(models.Model):
    project_id = models.CharField(max_length=10, null=True, blank=True, default='')
    ctime = models.CharField(max_length=10, null=True, blank=True, default='')
    all_result = models.BooleanField(default=True)  # 最终结果
    api_result = models.TextField(default='[]')  # 详细接口数据

    def __str__(self):
        return self.ctime


class DB_monitor(models.Model):
    label = models.CharField(max_length=100, default='', null=True, blank=True)
    project_id = models.CharField(max_length=10, default='', null=True, blank=True)
    method = models.CharField(max_length=10, default='', null=True, blank=True)  # 间隔时间，每日定时，接口触发
    value = models.CharField(max_length=100, default='', null=True, blank=True)
    status = models.BooleanField(default=False)  # 开关
    next = models.CharField(max_length=100, default='', null=True, blank=True)
    email = models.CharField(max_length=100, default='', null=True, blank=True)
    robot = models.CharField(max_length=100, default='', null=True, blank=True)  # 机器人接口、钉钉、企业微信、飞书

    def __str__(self):
        return self.label
