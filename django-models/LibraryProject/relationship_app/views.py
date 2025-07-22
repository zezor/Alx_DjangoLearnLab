from msilib.schema import ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from django.contrib.auth.decorators import permission_required
from .forms import BookForm  # You need a form for adding/editing books
from django.views.generic import UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login


def home(request):
    return render(request, 'relationship_app/home.html')

class HomeView(TemplateView):
    template_name = 'relationship_app/home.html'

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
            return redirect('allbooks')  # Redirect to any page after login
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


###Create Role-Based Views

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'




@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

## Update Views to Enforce Permissions
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allbooks')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Add'})


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('allbooks')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Edit'})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('allbooks')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})



class BookUpdateView(LoginRequiredMixin,UpdateView):
    model = Book
    fields = ['title', 'author', 'published_date', 'isbn']
    template_name = 'relationship_app/book_form.html'
    success_url = reverse_lazy('allbooks')

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'relationship_app/book_confirm_delete.html'
    success_url = reverse_lazy('allbooks')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Book deleted successfully.")
        return super().delete(request, *args, **kwargs)



class LibraryDeleteView(DeleteView):
    model = Library
    template_name = 'relationship_app/library_confirm_delete.html'
    success_url = reverse_lazy('library-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Library deleted successfully.")
        messages.success(request, "Welcome to the dashboard!")
        return super().delete(request, *args, **kwargs)


# class BookListView(ListView):
#     model = Book
#     template_name = 'relationship_app/list_books.html'
#     context_object_name = 'all_books'

