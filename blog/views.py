from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator,EmptyPage,\
    PageNotAnInteger

# Create your views here.
#view for retrieving all the post
def post_list(request):
    object_list=Post.my_manager.all()
    paginator=Paginator(object_list, 1)#3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        #If page id out of range  deliver the last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'page':page,
                  'posts':posts})


#view for displacing a single post
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='p',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,'blog/post/detail.html',{'post':post})


