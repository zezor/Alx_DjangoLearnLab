from datetime import date
from django.contrib.auth.models import User
from django.db import models

class Author(models.Model):
    author_name = models.CharField(max_length=100)
    def __str__(self):
        return self.author_name

# class Book(models.Model):
#     objects = None
#     title = models.CharField(max_length=200)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

#     def __str__(self):
#         return self.title
    
##Extend the Book Model with Custom Permissions
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField(default=date(2000, 1, 1))
    isbn = models.CharField(max_length=13, default='0000')


    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]

    def __str__(self):
        return self.title

class Library(models.Model):
    library_name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries',null=True)

    def __str__(self):
        return self.library_name


class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name
    
### CREATING USER PROFILE
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user} - {self.role}"
    
    

