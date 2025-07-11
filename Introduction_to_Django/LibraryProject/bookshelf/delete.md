# Open the Django shell:
# python manage.py shell

from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
book.delete()

# Expected Output: Book instance deleted successfully
# (No output unless printed manually — can verify via Book.objects.all())
print(Book.objects.all())
# Output: <QuerySet []>
