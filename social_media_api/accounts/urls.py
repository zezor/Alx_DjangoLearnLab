from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
    # urls.py
    path('profile/', ProfileView.as_view(), name='profile'),

]
