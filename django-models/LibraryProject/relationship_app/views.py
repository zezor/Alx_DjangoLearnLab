from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book, Library

# Create your views here.
def all_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'all_books':books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'