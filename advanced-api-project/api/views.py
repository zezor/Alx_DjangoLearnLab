# api/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import filters  # for SearchFilter & OrderingFilter




# =======================
#  Generic Views for Book
# =======================

class BookListView(generics.ListAPIView):
    """
    Retrieves a list of all books.
    Accessible to all users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Public read, auth required for writes
    
    # # Enable backends
    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filtering options (exact matches)
    filterset_fields = ['title', 'author', 'publication_year']

    # Search options (partial matches)
    search_fields = ['title', 'author__name']

    # Ordering options
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering
    
class MyModelListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.OrderingFilter]
    search_fields = [filters.SearchFilter]
    ordering_fields = ['name', 'created_at']
    ordering = ['name']  # default ordering



class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves details of a single book by ID.
    Accessible to all users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    Creates a new book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    Updates an existing book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    Deletes a book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]











# from django.shortcuts import render

# # Create your views here.
# # api/views.py
# from rest_framework import viewsets, generics, permissions
# from .models import Author, Book
# from .serializers import AuthorSerializer, BookSerializer

# class AuthorViewSet(viewsets.ModelViewSet):
#     """
#     ModelViewSet for Author:
#     - list, retrieve, create, update, delete
#     - Nested books are returned read-only inside AuthorSerializer
#     """
#     queryset = Author.objects.all().order_by('id')
#     serializer_class = AuthorSerializer


# class BookViewSet(viewsets.ModelViewSet):
#     """
#     ModelViewSet for Book:
#     - standard CRUD for Book instances
#     - BookSerializer performs publication_year validation
#     """
#     queryset = Book.objects.all().order_by('id')
#     serializer_class = BookSerializer


# class BookListView(generics.ListAPIView):
#     """
#     Retrieves a list of all books.
#     Accessible to all users (no authentication required).
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [permissions.AllowAny]  # Read-only for everyone


# class BookDetailView(generics.RetrieveAPIView):
#     """
#     Retrieves details of a single book by ID.
#     Accessible to all users (no authentication required).
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [permissions.AllowAny]


# class BookCreateView(generics.CreateAPIView):
#     """
#     Creates a new book.
#     Restricted to authenticated users only.
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         """
#         Optionally customize save logic here.
#         For now, we just save the book normally.
#         """
#         serializer.save()


# class BookUpdateView(generics.UpdateAPIView):
#     """
#     Updates an existing book.
#     Restricted to authenticated users only.
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_update(self, serializer):
#         """
#         Optionally modify save logic before update.
#         """
#         serializer.save()


# class BookDeleteView(generics.DestroyAPIView):
#     """
#     Deletes a book.
#     Restricted to authenticated users only.
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [permissions.IsAuthenticated]
