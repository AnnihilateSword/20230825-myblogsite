from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.cache import cache
from django.db.models import Sum
from blog.models import Blog
import datetime
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data


def get_7_days_hot_blogs():
    '''
        获取前7天的热门博客（不包括今天）
    '''
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)  # 获取7天前的日期
    # 获取范围内的博客
    blogs = Blog.objects\
        .filter(read_details__date__lt=today, read_details__date__gte=date)\
        .values('id', 'title')\
        .annotate(read_num_sum=Sum('read_details__read_num'))\
        .order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums, dates = get_seven_days_read_data(blog_content_type)
    
    # 获取前7天热门博客的缓存数据
    hot_blogs_of_7_days = cache.get('hot_blogs_of_7_days')
    if hot_blogs_of_7_days is None:
        hot_blogs_of_7_days = get_7_days_hot_blogs()
        # 写到缓存，有效期这里设置 3分钟
        cache.set('hot_blogs_of_7_days', hot_blogs_of_7_days, 180)
        # 用于测试，打印一些东西
        print('calc')
    else:
        # 用于测试，打印一些东西
        print('use cache!')

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type)  # 当天热门数据
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)  # 昨日热门数据
    context['hot_blogs_of_7_days'] = hot_blogs_of_7_days  # 前7天热门数据博客
    return render(request, 'home.html', context=context)

def about(request):
    context = {}
    return render(request, 'about.html', context=context)