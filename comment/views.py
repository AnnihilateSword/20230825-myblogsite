from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm

# Create your views here.
def update_comment(request: HttpRequest):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)

    # 返回数据
    data = {}
    
    if comment_form.is_valid():
        # 检查通过
        # 新建 Comment 对象，并保存
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        # 添加回复数据
        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user

        comment.save()

        # return redirect(referer)
        # 返回数据
        data['status'] = 'SUCCESS'
        # data['username'] = comment.user.username
        data['username'] = comment.user.get_nickname_or_username()
        # data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        #
        data['content_type'] = ContentType.objects.get_for_model(comment).model

        if not parent is None:
            # data['reply_to'] = comment.reply_to.username
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''

    else:
        # return render(request, 'error.html', { 'message':comment_form.errors, 'redirect_to':referer })
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
        
    return JsonResponse(data=data)

def del_comment(request: HttpRequest):
    data = {}
    reply_comment_id = request.POST['reply_comment_id']
    if Comment.objects.filter(pk=reply_comment_id).exists():
        comment = Comment.objects.get(pk=reply_comment_id)
        data['status'] = 'SUCCESS'
        data['reply_comment_id'] = reply_comment_id
        data['comment_text'] = comment.text
        # 删除评论
        comment.delete()
    else:
        data['status'] = 'ERROR'
        data['reply_comment_id'] = reply_comment_id

    return JsonResponse(data=data)