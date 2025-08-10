# api/models.py
from django.db import models

class Author(models.Model):
    """
    Author model.
    - name: stores the author's full name.
    An Author can have many Book instances (one-to-many relationship).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model.
    - title: the book's title.
    - publication_year: integer year when the book was published.
    - author: ForeignKey to Author establishing a one-to-many
      relationship (Author -> Book).
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    # on_delete=models.CASCADE means if Author is deleted, its books are deleted.
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
