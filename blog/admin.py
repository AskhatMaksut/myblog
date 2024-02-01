from django.contrib import admin
from .models import Blog, Comment


# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", 'content', 'image')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("username", 'comment', 'created_at')


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentsAdmin)
