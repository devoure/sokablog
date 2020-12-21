from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
#view for retrieving all the post
def post_list(request):
    posts=Post.my_manager.all()
    return render(request, 'blog/post/list.html', {'posts':posts})


#view for displacing a single post
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='p',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,'blog/post/detail.html',{'post':post})


