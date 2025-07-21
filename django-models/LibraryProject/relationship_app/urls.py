from django.urls import  path
from .views import list_books, LibraryDetailView
from . import views


path('allbooks', views.all_books, name='all_books')
path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),