from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.

from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns to show in the admin list view
    search_fields = ('title', 'author')                     # Enable search by title and author
    list_filter = ('publication_year',)                     # Add a filter by publication year
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email','username', 'is_staff')