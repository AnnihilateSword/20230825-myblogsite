from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from .models import LikeCount, LikeRecord

    
def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data=data)    

def SuccessResonse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data=data)

def like_change(request: HttpRequest):
    # 获取数据
    user = request.user
    if not user.is_authenticated:  # 验证
        return ErrorResponse(400, 'you were not login')

    content_type = request.GET.get('content_type')  # 这里拿到的是字符串，所以下面还要处理
    object_id = int(request.GET.get('object_id'))  # 注意类型转换

    # 验证模型
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, 'object not exist')  # 模型不存在
    is_like = request.GET.get('is_like')

    # 处理数据
    # 5 种情况指的是两种正常情况，两种后端不信任前端发送信息（后面有讲），1种后端两模型的数据描述的效果不统一
    if is_like == 'true':
        # 点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 1.
            # 未点赞过，进行点赞【成功】
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return SuccessResonse(like_count.liked_num)
        else:
            # 已点赞过，不能重复点赞
            return ErrorResponse(402, 'you were liked')
    else:
        # 取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 2.
            # 有点赞过，取消点赞【成功】
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            # 点赞总数 -1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return SuccessResonse(like_count.liked_num)
            else:
                # 数据错误
                return ErrorResponse(404, 'data error')
        else:
            # 没有点赞过，不能取消
            pass
