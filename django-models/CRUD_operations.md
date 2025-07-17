Python 3.12.6 (tags/v3.12.6:a4a2d2b, Sep  6 2024, 20:11:23) [MSC v.1940 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> # Open the Django shell:
>>> # python manage.py shell
>>>
>>> from bookshelf.models import Book
>>> 
>>> # Create a Book instance
>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
>>> 
>>> # Expected Output: A Book object created successfully
>>> print(book)
1984 by George Orwell (1949)
>>> # Output: 1984 by George Orwell (1949)
>>> from bookshelf.models import Book
>>> book = Book.objects.get(title="1984")
>>> print(f"Title: {book.title}")
Title: 1984
>>> print(f"Author: {book.author}")
Author: George Orwell
>>> print(f"Publication Year: {book.publication_year}")
Publication Year: 1949
>>> from bookshelf.models import Book
>>> book = Book.objects.get(title="1984")
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> print(book)
Nineteen Eighty-Four by George Orwell (1949)
>>> from bookshelf.models import Book
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()
(1, {'bookshelf.Book': 1})
>>> print(Book.objects.all()
...
