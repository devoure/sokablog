from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

#defines a class that inherits from models to create our custom manager
class CustomManager(models.Manager):
    def get_queryset(self):
        return super(CustomManager, self).get_queryset()\
            .filter(status='d')

class Post(models.Model):
    STATUS_CHOICES =[
    ('d', 'Draft'),
    ('p', 'Published'),
    ]
    title = models.CharField(max_length = 250)
    #slug will help in urls
    #unique_for_date will prevent multiple posts from having the same slug
    #..for the same date
    slug = models.SlugField(max_length = 250,unique_for_date='publish')
    #related_name will represent the manager function that returns a queryset
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    #auto_now_add updates field on creation only
    created = models.DateTimeField(auto_now_add=True)
    #auto_now takes precedence as it updates field each time
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='d')
    #The default manager
    objects = models.Manager()
    #the custom manager
    my_manager = CustomManager()
    #meta class defines anything that is not a field
    class Meta:
        #ordering =tells django to sort the results by the publish field
        #..when we query the database
        #the '-' orders in descending order,'?' orders randomly
        ordering = ['-publish',]
    #__str__will be called when you call str() on a object
    def __str__(self):
        return self.title

