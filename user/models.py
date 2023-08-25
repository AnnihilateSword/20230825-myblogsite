from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(verbose_name='昵称', max_length=20, default='')

    class Meta(AbstractUser.Meta):
        pass


def get_nickname(self: User):
    if User.objects.filter(username=self.username).exists():
        user = User.objects.get(username=self.username)
        if user.nickname == '':
            return 'DEFAULT'
        else:
            return user.nickname
    else:
        return ''
    
def has_nickname(self: User):
    if User.objects.filter(username=self.username).exists():
        user = User.objects.get(username=self.username)
        if user.nickname == '':
            return False
        else:
            return True
    else:
        return False
    
def get_nickname_or_username(self: User):
    '''
        有昵称获取昵称，没有就获取用户名
    '''
    if User.objects.filter(username=self.username).exists():
        user = User.objects.get(username=self.username)
        if user.nickname == '':
            return user.username
        else:
            return user.nickname
    else:
        return '用户不存在，数据有误'

User.get_nickname = get_nickname
User.has_nickname = has_nickname
User.get_nickname_or_username = get_nickname_or_username