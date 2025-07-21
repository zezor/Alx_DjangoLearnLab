from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from .views import list_books

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

# Create your views here.
def all_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'all_books':books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('list_books')  # Redirect to any page after login
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})
