from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadDetail
import datetime

def read_statistics_read_once(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = f'{ct.model}_{obj.pk}_read'
    
    # 如果查找的这个 Cookie 不存在
    if not request.COOKIES.get(key):
        # 1. 处理总记录
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        # 计数 +1 并保存
        readnum.read_num += 1
        readnum.save()

        # 2. 处理当天记录
        date = timezone.now().date()
        read_detail, createed = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        # 当天阅读数 +1 并保存
        read_detail.read_num += 1
        read_detail.save()

    return key

def get_seven_days_read_data(content_type):
    '''
        获取前七天 以及当天 的阅读数据
    '''
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, -1, -1):  # 取 [7, 0]
        # 得到前 i 天的日期
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        # 可能会有多条数据，需要加总
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        # 聚合计算，这里对 read_num 字段求和 
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        # 如果 result['read_num_sum'] 为 None 就取 0
        read_nums.append(result['read_num_sum'] or 0)

    return read_nums, dates

def get_today_hot_data(content_type):
    '''
        获取当天热门数据
    '''
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')  # 由大到小排序
    return read_details[:7]  # 最多显示前 7篇，不然太多

def get_yesterday_hot_data(content_type):
    '''
        获取昨日热门数据
    '''
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)  # 获取昨天的日期
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')  # 由大到小排序
    return read_details[:7]