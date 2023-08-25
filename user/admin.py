from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from typing import Any

# 修改后台管理属性，在任何一个 admin.py 文件中添加都行
admin.site.site_title = '后台管理'
admin.site.site_header = '后台管理'

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("nickname", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    
    list_display = ('username', 'email', 'nickname', 'is_staff', 'is_active', 'is_superuser')