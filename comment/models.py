from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.auth.models import User
from django.conf import settings


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name='评论内容')
    comment_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    user = models.ForeignKey(verbose_name='用户', to=settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)

    # 可以通过这个获取一条评论下面的所有评论
    root = models.ForeignKey('self', null=True, related_name='root_comment', on_delete=models.CASCADE)
    # 新建外键，关联自己，设置可以为空
    parent = models.ForeignKey('self', null=True, related_name='parentcomment', on_delete=models.CASCADE)
    # 在添加一个字段，方便获取信息（回复谁）一条评论不一定有回复，可以为 null，related_name 解决冲突
    reply_to = models.ForeignKey(verbose_name='回复谁', to=settings.AUTH_USER_MODEL, related_name='replies', null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.text

    class Meta:
        ordering = ['comment_time']  # 升序