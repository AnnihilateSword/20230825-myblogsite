from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Comment


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)  # 隐藏显示
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'), error_messages={'required':'评论内容不能为空。'})  # 多行文本
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'reply_comment_id'}))

    def __init__(self, *args, **kwargs):
        # 获取 'comment/views.py' 中传过来的 user 用于用户验证！！！
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
        
        # 评论对象验证
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            # 这里得到 blog 的 contenttype，通过 model_class 得到 Return the model class for this type of content.
            model_class = ContentType.objects.get(model=content_type).model_class()
            # 就是在博客中找某一篇具体博客，这种方法就变得相当的通用
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj  # 保存模型对象
        except ObjectDoesNotExist as e:
            raise forms.ValidationError('评论对象不存在')

        return self.cleaned_data
    
    # 验证
    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError('回复出错')
        elif reply_comment_id == 0:
            # 顶级回复
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
             self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError('回复出错')
        
        return self.cleaned_data