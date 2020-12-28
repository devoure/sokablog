from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator,EmptyPage,\
    PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail

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

def post_share (request, post_id):
    #retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='p')
    sent = False

    if request.method =='POST':
        #form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{} ({}) recommends you reading "{}"'.format(cd['name'], cd
                                                                 ['email'], post.title)
            message='Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url,
                                                                   cd['name'], cd['comments'])
            send_mail(subject, message, 'disguisedsandwich@gmail.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
        #submit an empty form when form is initially loaded
    return render(request, 'blog/post/share.html', {'post':post,
                                                'form':form,'sent':sent})

