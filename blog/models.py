from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation  # 用于反向关联
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail

# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(verbose_name='博客类型', max_length=15)

    def __str__(self) -> str:
        return self.type_name
    

class Blog(models.Model, ReadNumExpandMethod):
    blog_type = models.ForeignKey(verbose_name='博客类型', to=BlogType, on_delete=models.CASCADE) 
    title = models.CharField(verbose_name='标题', max_length=50)
    # 富文本编辑
    # content = RichTextField(verbose_name='内容')
    # 添加上传图片
    content = RichTextUploadingField(verbose_name='内容')
    author = models.ForeignKey(verbose_name='作者', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 反向关联到模型
    read_details = GenericRelation(ReadDetail)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_update_time = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)

    def __str__(self) -> str:
        return f'<Blog: {self.title}>'

    class Meta:
        ordering = ['-create_time']