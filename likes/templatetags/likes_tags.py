from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount, LikeRecord


register = template.Library()

# 注册为简单的模板标签
@register.simple_tag
def get_like_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    # 参考文档：https://docs.djangoproject.com/zh-hans/4.2/ref/models/querysets/#get-or-create
    like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    # 返回点赞数
    return like_count.liked_num

@register.simple_tag(takes_context=True)
def get_like_status(context, obj):  # 加上 context 可以获取到改模板所在的页面所使用的模板变量，因为Django有自动加上这个 user 变量，是可以获取到的
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if LikeRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''

@register.simple_tag()
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model