from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, ProfileView,PostViewSet,CommentViewSet

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
    # urls.py
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile_detail'),
    path('posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list'),
    path('posts/<int:pk>/', PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='post-detail'),
    path('comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    path('comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='comment-detail'),

]
