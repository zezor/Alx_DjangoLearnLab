from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
    # urls.py
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile_detail'),
    
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),    
    
    
    path('followers/', FollowersListView.as_view(), name='my-followers'),
    path('followers/<int:user_id>/', FollowersListView.as_view(), name='user-followers'),

    path('following/', FollowingListView.as_view(), name='my-following'),
    path('following/<int:user_id>/', FollowingListView.as_view(), name='user-following'),
    
]
