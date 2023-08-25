from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm


register = template.Library()

# 注册为简单的模板标签
@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    # 返回评论数
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()

@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={'content_type':content_type.model, 'object_id':obj.pk, 'reply_comment_id':0})
    # 返回表单
    return form

@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    # 找到该博客的评论对象，parent=None 先不显示回复
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    # 返回评论列表
    return comments.order_by('-comment_time')