from django.shortcuts import render

# Create your views here.
# LibraryProject/bookshelf/views.py

from django.shortcuts import render, redirect
from .forms import ExampleForm
from django.contrib.auth.decorators import permission_required

@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book-list')
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/add_book.html', {'form': form})
