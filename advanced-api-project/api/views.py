from django.shortcuts import render

# Create your views here.
# api/views.py
from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for Author:
    - list, retrieve, create, update, delete
    - Nested books are returned read-only inside AuthorSerializer
    """
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for Book:
    - standard CRUD for Book instances
    - BookSerializer performs publication_year validation
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
