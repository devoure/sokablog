from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator,EmptyPage,\
    PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib import messages
from taggit.models import Tag
from django.db.models import Count

# Create your views here.
#view for retrieving all the post
def post_list(request, tag_slug=None):
    object_list=Post.my_manager.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator=Paginator(object_list, 1)#1 posts in each page
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
                   'posts':posts,
                   'tag':tag})


#view for displacing a single post
def post_detail(request, year, month, day, post, tag_slug=None):
    post = get_object_or_404(Post, slug=post,
                             status='p',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            #created an instance with saved content but dont save to database just yet
            new_comment.post = post
            #updated the post field in model Comment
            #linked the comment to a post
            new_comment.save()
            #saved the comment to database now
            messages.add_message(request, messages.INFO, 'Comment posted successfully')
            return HttpResponseRedirect('')
    else:
        comment_form = CommentForm()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag, slug=tag_slug)
        objects=Post.my_manager.all()
        objects=objects.filter(tags__in=[tag])
    post_tags_ids = post.tags.values_list('id', flat=True)
    #flat=true will not return a tuple([1,2]) rather a flat list[1,2]
    similar_posts =Post.my_manager.filter(tags__in=post_tags_ids)\
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags', '-publish')[:4]
    return render(request,'blog/post/detail.html',{'post':post,
                                                   'comments':comments,
                                                   'comment_form':comment_form,
                                                   'similar_posts':similar_posts,
                                                   'tag':tag})

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

