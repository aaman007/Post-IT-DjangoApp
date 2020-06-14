from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'date_published', 'status']
    list_filter = ['status']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
