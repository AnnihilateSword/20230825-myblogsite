from django.shortcuts import render, redirect
from django.contrib import auth
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import Group
from .forms import LoginForm, RegisterForm, ChangeNicknameForm
from .models import User


# User = get_user_model()


def login(request: HttpRequest):
    '''
        登录
    '''
    if request.method == 'POST':  # 一定要大写
        # 提交表单页面
        login_form = LoginForm(request.POST)
        if login_form.is_valid():  # 只要是验证操作就放到 Form 里面，这样就更加简洁明了了
            user = login_form.cleaned_data['user']  # 获取 user
            # 登录用户
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    # 返回给前端
    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context=context)

def login_for_modal(request: HttpRequest):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():  # 只要是验证操作就放到 Form 里面，这样就更加简洁明了了
        user = login_form.cleaned_data['user']  # 获取 user
        # 登录用户
        auth.login(request, user)
        # 返回数据
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data=data)

def register(request: HttpRequest):
    '''
        注册
    '''
    if request.method == 'POST':
        # 提交表单页面
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():  # 验证
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            # 创建用户
            user: User = User.objects.create_user(username, email, password)
            user.is_staff = True
            # 给用户权限（现在不给了）
            # group = Group.objects.get(name='ptyh')
            # user.groups.add(group)
            user.save()

            # 这一种方法也可以
            # user = User()
            # user.username = username
            # user.email = email
            # user.set_password = password
            # user.save()

            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

    else:
        register_form = RegisterForm()

    # 返回给前端
    context = {}
    context['register_form'] = register_form
    return render(request, 'user/register.html', context=context)

def logout(request: HttpRequest):
    '''
        登出
    '''
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))

def user_info(request: HttpRequest):
    '''
        个人资料
    '''
    context = {}
    return render(request, 'user/user_info.html', context=context)

def change_nickname(request: HttpRequest):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':  # 一定要大写
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            user, created = User.objects.get_or_create(username=request.user.username)
            user.nickname = nickname_new
            user.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()
    
    context = {}
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context=context)