from django.urls import  path
from .views import all_books, LibraryDetailView, register
from django.contrib.auth import views as auth_views
from .views import list_books
from .views import admin_view, librarian_view, member_view
from . import views


urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    # Your other views
  
    path('allbooks', all_books, name='all_books'),  # list_books
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # LibraryDetailView
    
    ###Role-Based Views
    path('admin-panel/', admin_view, name='admin_view'),
    path('librarian-panel/', librarian_view, name='librarian_view'),
    path('member-panel/', member_view, name='member_view'),
    
    # permission actions
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
]
