from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('login_for_modal/', views.login_for_modal, name='login_for_modal'),  # 登录模态表单
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),  # 登出
    path('user_info/', views.user_info, name='user_info'),  # 个人资料
    path('change_nickname/', views.change_nickname, name='change_nickname'),  # 修改昵称
]