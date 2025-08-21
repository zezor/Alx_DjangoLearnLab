from django.contrib import admin
from .models import CustomUser, Post, Comment

# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'updated_at')
    search_fields = ('content',)
    ordering = ('-created_at',)

admin.site.register(Comment, CommentAdmin)
