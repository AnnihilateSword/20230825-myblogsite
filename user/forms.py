from django import forms
from django.contrib import auth
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    '''
        登录表单
    '''
    # required = True 是默认的
    username = forms.CharField(label='用户名', required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    # 变为 password 类型
    password = forms.CharField(label='密码', required=True, widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'请输入密码'}))

    # 当使用 Form.is_valid() 方法时就会执行该方法【验证功能】
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        # 这里验证的时候可以不需要 request 参数
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
            
        return self.cleaned_data
    

class RegisterForm(forms.Form):
    '''
        注册表单
    '''
    username = forms.CharField(label='用户名', max_length=30, min_length=3, 
                               required=True, 
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入3-30位的用户名'}))
    email = forms.EmailField(label='邮箱',
                             required=True, 
                             widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
    password = forms.CharField(label='密码', min_length=6, max_length=16,
                               required=True, 
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    password_again = forms.CharField(label='密码', min_length=6, max_length=16,
                            required=True, 
                            widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请再输入一次密码'}))
    
    # clean 后面加下划线跟字段名可以针对某一字段进行验证
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email
    
    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again
    

class ChangeNicknameForm(forms.Form):
    '''
        修改昵称表单
    '''
    # required = True 是默认的
    nickname_new = forms.CharField(label='新的昵称', max_length=20, required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'请输入新的昵称'}))

    def __init__(self, *args, **kwargs):
        # 获取 'user/views.py' 中传过来的 user 用于用户验证！！！
        # 返回值的同时并删除，用 pop 代替 get
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    # 验证
    def clean(self):
        # 判断用户是否登录，虽然前端已经判断是否登录了，但是我们遵循 “ 前端不可信原则 ”
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    # 当使用 Form.is_valid() 方法时就会执行该方法【验证功能】
    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError('新的昵称不能为空')
        return nickname_new
