import os
import django
from django.template.defaultfilters import title

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from models import Author, Book, Library, Librarian

# Query all books by a specific author
author = Author.objects.get(name="")
books_by_author = Book.objects.filter(author=author)
print(f"Books by {author.name}: {[book.title for book in books_by_author]}")

book = Book.objects.get(title="")
list_all_books = book.books.all()


# List all books in a library
library = Library.objects.get(name="library_name")
books_in_library = library.books.all()
print(f"Books in {library.name}: {[book.title for book in books_in_library]}")

# Retrieve the librarian for a library
librarian = library.librarian
print(f"Librarian for {library.name}: {librarian.name}")
