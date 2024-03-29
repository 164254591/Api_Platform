"""Api_Platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from Api_app.views import *
from django.views.generic import TemplateView
from Api_app.views_api import *

urlpatterns = [
    # ------------------------------------------权限系统无法管理的--------------------------------------------------------
    path('admin/', admin.site.urls),
    path('', login),
    path('accounts/login/', login),
    path('login_action/', login_action),
    path('register_action/', register_action),
    # path('index/', TemplateView.as_view(template_name='index.html')),
    path('index/', index),
    path('logout/', logout),
    path('get_apis/', get_apis),
    path('get_dck/', get_dck),
    path('set_dck/', set_dck),
    path('add_apis/', add_apis),
    path('remove_ac/', remove_ac),
    path('add_configure/', add_configure),
    path('save_configure/', save_configure),
    path('up_configure/', up_configure),
    path('down_configure/', down_configure),
    path('up_api/', up_api),
    path('down_api/', down_api),
    path('save_api/', save_api),
    path('send_api/', send_api),

    path('upload_binary_file/', upload_binary_file),
    path('upload_fd_file/', upload_fd_file),
    path('get_userable_par/', get_userable_par),  # 获取可用变量
    path('doing_api/', doing_api),  # 获取正在执行的接口名称
    path('run/', run),  # 执行大用例
    path('test_a/', test_a),
    path('test_b/', test_b),
    path('clear_all_reports/', clear_all_reports),
    path('get_all_reports/', get_all_reports),

    path('get_monitor_list/', get_monitor_list),
    path('add_monitor/', add_monitor),
    path('change_monitor_status/', change_monitor_status),
    path('delete_monitor/', delete_monitor),
    path('save_monitor/', save_monitor),
    path('jx_apiDoc/', jx_apiDoc),
    path('import_api_ad/', import_api_ad),
    path('upload_postman_file/', upload_postman_file),
    path('import_api_postman/', import_api_postman),

    path('change_catch_status/', change_catch_status),

    path('upload_img_file/',upload_img_file),
    path('jx_img/',jx_img),

    # -----------------------------------------权限系统可以管理的，但不一定监管（接口path只有一级，且path和函数名必须相同）---------
    re_path('(?P<path>.+)/', diy_power),

    # path('help/', help),
    # path('get_tj_datas/', get_tj_datas),
    # path('get_real_time_datas/', get_real_time_datas),
    #
    # path('get_project_list/', get_project_list),
    # path('add_project/', add_project),
    # path('delete_project/', delete_project),
    # path('get_project_detail/', get_project_detail),
    # path('save_project/', save_project),
    #
    # path('get_env_list/', get_env_list),
    # path('add_env/', add_env),
    # path('delete_env/', delete_env),
    #
    # path('get_api_shop_list/', get_api_shop_list),
    # path('save_api_shop/', save_api_shop),
    # path('delete_api_shop/', delete_api_shop),
    #
    # path('get_user_list/', get_user_list),
    # path('save_user_detail/', save_user_detail),
    # path('upload_user_avatar/', upload_user_avatar),
    #
    # path('get_to_user_list/', get_to_user_list),
    # path('send_news/', send_news),
    # path('send_notice/', send_notice),
    #
    # path('look_log/', look_log),
    #
    # path('get_power_list/', get_power_list),
    # path('add_power/', add_power),
    # path('delete_power/', delete_power),
    # path('save_power/', save_power),

]
