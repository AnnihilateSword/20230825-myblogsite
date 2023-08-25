from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from .models import BlogType, Blog
from read_statistics.utils import read_statistics_read_once
# from user.forms import LoginForm
from user.models import User


# 这里获取下面方法的公共部分，返回公共的 context
def get_blog_list_common_data(request, blogs_all_list):
    # 分页器功能 -----------------------
    blogs = blogs_all_list
    paginator = Paginator(blogs, settings.EACH_PAGE_BLOG_NUMBER)  # 每 settings.EACH_PAGE_BLOG_NUMBER 篇进行分页
    page_num = request.GET.get('page', 1)  # 是否有 page 关键字，没有默认给 1
    # 这里请求默认是传入的字符串，要做一些处理
    # paginator.page(int(page_num))  # 但是这样做不太好，比如用户传入字符串，
    # 不是数字或者超出范围（这里测试了超出范围默认是最后一页，不填数字就是第一页），就会出错
    # 但是 django 提供了一些解决方法
    page_of_blogs = paginator.get_page(page_num)  # Return a valid page, even if the page argument isn't a number or isn't in range.
    
    # 1. 控制页码显示范围
    cpn = page_of_blogs.number  # 当前页码
    show_bound = 2  # 左右显示范围
    page_range = list(range(max(cpn - show_bound, 1), cpn)) + \
                    list(range(cpn, min(cpn + show_bound, paginator.num_pages) + 1))  # 页码显示的范围

    # 2. 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 3. 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # ---------------------------------

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('create_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year, 
                            create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    # 获取博客分类的对应博客数量
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range  # 1. 页码显示的范围
    context['blog_dates'] = blog_dates_dict  # 这里是字典
    return context

# Create your views here.
# 这里因为 request 没有提示，需要加约束，并且导入 from django.http import HttpRequest
def blog_list(request: HttpRequest):
    context = get_blog_list_common_data(request, Blog.objects.all())
    return render(request, 'blog/blog_list.html', context=context)

def blog_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context = get_blog_list_common_data(request, Blog.objects.filter(blog_type=blog_type))

    # add context key
    context['blog_type'] = blog_type
    return render(request, 'blog/blog_with_type.html', context=context)

def blog_with_date(request, year, month):
    context = get_blog_list_common_data(request, Blog.objects.filter(create_time__year=year, create_time__month=month))

    # add context key
    context['date_of_blog'] = f'{year}年-{month}月'  # 日期
    return render(request, 'blog/blog_with_date.html', context=context)

def blog_detail(request: HttpRequest, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_read_once(request, blog)

    context = {}
    # context['blog'] = get_object_or_404(Blog, id=blog_pk)
    context['blog'] = blog
    # 上一篇博客（ 与当前博客创建时间比较，获取大于该值的所有博客中的最后一篇作为上一篇 ）
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    # 下一篇博客（同理）
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    # request 中有 user 字段，当前登录的用户，这里不传也有！（已经试过了）所以就不传了，这是 django 的机制
    # context['user'] = request.user
    # context['login_form'] = LoginForm()

    response = render(request, 'blog/blog_detail.html', context=context)
    # 用 Cookie 保存一些数据，注意：Cookie 会有一个有效期，过一段时间会失效，单位是 (s)
    # 如果不设置有效期，浏览器退出 Cookie 才会失效
    response.set_cookie(read_cookie_key, 'true')  # 阅读 cookie 标记
    return response
