# api/urls.py
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookList  # BookList is your earlier ListAPIView

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),  # includes all CRUD routes for BookViewSet
    path('auth-token/', obtain_auth_token, name='api_token_auth'),
]
