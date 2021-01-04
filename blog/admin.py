from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    #fields to be displayed on the admin post list page
    list_display = ('title', 'slug', 'author', 'publish',
                    'status')
    #populates a right sidebar for filter the results
    list_filter = ('status', 'created', 'publish', 'author')
    #populates a search bar with defined fields
    search_fields = ('title', 'body')
    #prepopulates the slug field with the title input
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    #a bar to navigate quickly through a date hierachy
    date_hierachy = 'publish'
    ordering = ['status', 'publish']
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

# Register your models here.

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
