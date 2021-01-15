from django import template
from django.db.models import Count
from django.utils.safestring import  mark_safe
import markdown
register = template.Library()

from ..models import Post

@register.simple_tag
def total_posts():
    return Post.my_manager.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts=Post.my_manager.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.simple_tag
def  get_most_commented(count=5):
    return Post.my_manager.annotate(total=Count('comments'))\
            .order_by('-total')[:count]

@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

