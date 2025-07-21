from django.urls import  path
from .views import all_books, LibraryDetailView, register_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', register_view, name='register'),

    # Your other views
  
    path('allbooks', all_books, name='all_books'),  # list_books
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # LibraryDetailView
]
