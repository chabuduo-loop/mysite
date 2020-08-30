from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read

def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, 7)
    # 获取到url传过来的page
    page_num = request.GET.get('page' , 1)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number
    # 获取当前页码前后各两页的前后范围
    page_range = [x for x in range(current_page_num - 3 , current_page_num + 4) if x in paginator.page_range]


    # 加上省略的页码标记来加强体验
    if page_range[0] - 1 >= 2:
        page_range.insert(0 ,'...')
    if paginator.num_pages - page_range[-1]>=2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] !=paginator.num_pages:
        page_range.append(paginator.num_pages)

    #
    # 获取博客分类的对应博客数量
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = blog_types_list
    context['blog_dates'] = Blog.objects.dates('created_time','month' ,order = 'DESC')
    return context



def blog_list(request):
    blogs_all_list = Blog.objects.all().order_by()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render_to_response('blog/blog_list.html', context)

def blogs_with_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type = blog_type).order_by()
    


    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    
    return render_to_response('blog/blogs_with_type.html', context)

def blogs_with_date(request, year , month):
   
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' %(year , month)

    return render_to_response('blog/blogs_with_date.html', context)

def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request , blog)
    

    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt= blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt= blog.created_time).first()
    context['blog'] = blog
    response = render_to_response('blog/blog_detail.html' , context)
    response.set_cookie(read_cookie_key , 'true')
    return response
 