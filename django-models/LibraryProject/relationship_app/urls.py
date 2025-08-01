from django.urls import  path
from .views import all_books, LibraryDetailView, register
from django.contrib.auth import views as auth_views
from . import views
from .views import *   #admin_view, librarian_view, member_view,



urlpatterns = [
    path('home/', home, name='home'),  # This is your homepage
    path('home/', HomeView.as_view(), name='home'),
    # path('books/', BookListView.as_view(), name='book-list'),

    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    # Your other views
  
  
    path('allbooks', all_books, name='allbooks'),  # list_books
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # LibraryDetailView
    
    ###Role-Based Views
    path('admin-panel/', admin_view, name='admin_view'),
    path('librarian-panel/', librarian_view, name='librarian_view'),
    path('member-panel/', member_view, name='member_view'),
    
    # permission actions
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete_books/<int:pk>/', views.delete_book, name='delete_book'),


path('book/<int:pk>/edit/', BookUpdateView.as_view(), name='book-update'),
path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
