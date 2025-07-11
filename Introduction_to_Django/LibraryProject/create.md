# Open the Django shell:
# python manage.py shell

from bookshelf.models import Book

# Create a Book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Expected Output: A Book object created successfully
print(book)
# Output: 1984 by George Orwell (1949)
