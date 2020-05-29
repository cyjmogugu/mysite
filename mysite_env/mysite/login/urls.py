#-*- codeing=uft-8 -*-
#@Time: 2020/5/18 16:38
#@Author:陈怡婧
#@File ：urls.py
#@Software:PyCharm


from django.urls import path,include,re_path
from . import views

app_name='login'
urlpatterns = [
    path('',views.homepage,name='主页'), #视窗来处理相应
    path('login/',views.log_in,name='登录'), #视窗来处理相应
    path('logout/',views.log_out,name='退出'), #视窗来处理相应
    path('register/',views.register,name='注册'), #视窗来处理相应
    re_path('user_center/$',views.user_center,name='个人中心'), #视窗来处理相应
    re_path('user_center/edit_profile/$',views.edit_profile,name='编辑个人信息'), #视窗来处理相应
    path('user_center/change_password', views.change_password, name='修改密码'),  # 视窗来处理相应
    re_path('ticket/$', views.ticket_information, name='车票信息'),  # 视窗来处理相应
    path('base/', views.base, name='首页'),  # 视窗来处理相应
    re_path('buy/$', views.buy_information, name='购买车票'),  # 视窗来处理相应
    re_path('bought/$', views.bought_information, name='已购车票'),  # 视窗来处理相应
    re_path('ticket_change/$', views.ticket_change, name='票务修改'),  # 视窗来处理相应
    re_path('ticket_detail_change/$', views.ticket_detail_change, name='车票详细信息修改'),  # 视窗来处理相应
    re_path('ticket_create/$', views.ticket_create, name='新增车票'),  # 视窗来处理相应
    re_path('ticket_delete/$', views.ticket_delete, name='删除车票'),  # 视窗来处理相应
    path('code/', views.code_confirm, name='短信验证码'),  # 视窗来处理相应
    re_path('modify_detail/$', views.modify_detail, name='记录查询'),  # 视窗来处理相应
]