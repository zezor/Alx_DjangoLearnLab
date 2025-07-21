from django.urls import  path
from .views import all_books, LibraryDetailView, register
from django.contrib.auth import views as auth_views
from .views import list_books
from . import views


urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    # Your other views
  
    path('allbooks', all_books, name='all_books'),  # list_books
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # LibraryDetailView
]
