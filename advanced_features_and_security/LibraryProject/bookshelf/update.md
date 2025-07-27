# Open the Django shell:
# python manage.py shell

from bookshelf.models import Book

# Retrieve the existing book
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Expected Output: Updated title reflected in the object
print(book)
# Output: Nineteen Eighty-Four by George Orwell (1949)
